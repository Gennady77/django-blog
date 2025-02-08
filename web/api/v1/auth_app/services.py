from typing import TYPE_CHECKING, NamedTuple, Optional
from urllib.parse import urlencode, urljoin

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core import signing
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework import status
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from api.email_services import BaseEmailHandler

from main.decorators import except_shell
from main.tasks import send_information_email
from api.v1.auth_app.types import PasswordResetDTO

if TYPE_CHECKING:
    from main.models import UserType


User: 'UserType' = get_user_model()


class CreateUserData(NamedTuple):
    first_name: str
    last_name: str
    email: str
    password_1: str
    password_2: str


class ConfirmationEmailHandler(BaseEmailHandler):
    FRONTEND_URL = settings.FRONTEND_URL
    FRONTEND_PATH = '/confirm'
    TEMPLATE_NAME = 'emails/verify_email.html'

    def _get_activate_url(self) -> str:
        url = urljoin(self.FRONTEND_URL, self.FRONTEND_PATH)
        query_params: str = urlencode(
            {
                'key': self.user.confirmation_key,
            },
            safe=':+',
        )
        return f'{url}?{query_params}'

    def email_kwargs(self, **kwargs) -> dict:
        return {
            'subject': _('Register confirmation email'),
            'to_email': self.user.email,
            'context': {
                'user': self.user.full_name,
                'activate_url': self._get_activate_url(),
            },
        }


class AuthAppService:
    @staticmethod
    def is_user_exist(email: str) -> bool:
        return User.objects.filter(email=email).exists()

    @staticmethod
    @except_shell((User.DoesNotExist,))
    def get_user(email: str) -> User:
        return User.objects.get(email=email)

    @transaction.atomic()
    def create_user(self, validated_data: dict) -> 'User':
        data = CreateUserData(**validated_data)
        user = User.objects.create_user(
            email=data.email,
            first_name=data.first_name,
            last_name=data.last_name,
            password=data.password_1,
            is_active=False,
        )
        return user

    def confirm_email(self, key: str):
        try:
            user_id = signing.loads(key, max_age=settings.EMAIL_CONFIRMATION_EXPIRE_SECONDS)

            user = User.objects.get(id=user_id)

            if user.is_active is True:
                raise ValidationError({'error': 'user is already active'}, code='user_is_already_active')

        except (signing.BadSignature, signing.SignatureExpired):
            raise ValidationError({'key': 'confirm key is not valid or expired'}, code='invalid')
        except User.DoesNotExist:
            raise ValidationError({'error': 'user does not exist'}, code='user_does_not_exists')

        user.is_active = True

        user.save(update_fields=['is_active'])

    def get_confrim_url(self, user_id: int):
        confirm_key = signing.dumps(user_id)

        return f'{settings.FRONTEND_URL}/verify-email/?confirm_key={confirm_key}'

class PasswordResetGenerator:
    def __init__(self):
        self.token_generator = default_token_generator

    def encode(self, user: 'UserType') -> PasswordResetDTO:
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = self.token_generator.make_token(user)

        return PasswordResetDTO(uid=uid, token=token)

    def check_token(self, user: 'UserType', token: str):
        return self.token_generator.check_token(user, token)

    def get_user_by_uid(self, uid: str) -> Optional['UserType']:
        try:
            user_id = urlsafe_base64_decode(uid).decode()

            return User.objects.get(id=user_id)
        except (User.DoesNotExist, ValueError):
            return None

class PasswordResetService:
    def _get_reset_url(self, user: 'UserType'):
        generator = PasswordResetGenerator().encode(user)

        return f'{settings.FRONTEND_URL}/password-recovery/?uid={generator.uid}&token={generator.token}'

    def reset_password(self, email: str):
        user = User.objects.filter(email=email).first()

        if not user:
            raise NotFound('user does not exists', code='user_does_not_exists')

        send_information_email(
            subject='Reset password',
            template_name='emails/reset_password.html',
            context={'name': user.full_name, 'reset_password_url': self._get_reset_url(user)},
            to_email=user.email,
        )

    def reset_confirm(self, validated_data: dict):
        user = PasswordResetGenerator().get_user_by_uid(validated_data['uid'])

        if not user:
            raise NotFound('user does not exists', code='user_does_not_exists')

        token_valid = PasswordResetGenerator().check_token(user, validated_data['token'])

        if not token_valid:
            raise ValidationError('token is not valid', code='token_is_not_valid')

        user.set_password(validated_data['password_1'])

        user.save(update_fields=['password'])





def full_logout(request):
    response = Response({"detail": _("Successfully logged out.")}, status=status.HTTP_200_OK)
    auth_cookie_name = settings.REST_AUTH['JWT_AUTH_COOKIE']
    refresh_cookie_name = settings.REST_AUTH['JWT_AUTH_REFRESH_COOKIE']

    response.delete_cookie(auth_cookie_name)
    refresh_token = request.COOKIES.get(refresh_cookie_name)
    if refresh_cookie_name:
        response.delete_cookie(refresh_cookie_name)
    try:
        token = RefreshToken(refresh_token)
        token.blacklist()
    except KeyError:
        response.data = {"detail": _("Refresh token was not included in request data.")}
        response.status_code = status.HTTP_401_UNAUTHORIZED
    except (TokenError, AttributeError, TypeError) as error:
        if hasattr(error, 'args'):
            if 'Token is blacklisted' in error.args or 'Token is invalid or expired' in error.args:
                response.data = {"detail": _(error.args[0])}
                response.status_code = status.HTTP_401_UNAUTHORIZED
            else:
                response.data = {"detail": _("An error has occurred.")}
                response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

        else:
            response.data = {"detail": _("An error has occurred.")}
            response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

    else:
        message = _(
            "Neither cookies or blacklist are enabled, so the token "
            "has not been deleted server side. Please make sure the token is deleted client side."
        )
        response.data = {"detail": message}
        response.status_code = status.HTTP_200_OK
    return response
