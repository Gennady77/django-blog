from dj_rest_auth import views as auth_views
from django.contrib.auth import logout as django_logout
from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from . import serializers
from .services import AuthAppService, PasswordResetService, full_logout
from main.tasks import send_information_email


class SignUpView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.UserSignUpSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()
        user = service.create_user(serializer.validated_data)

        send_information_email(
            subject='Confirm your email',
            template_name='emails/confirmation.html',
            context={'name': user.full_name, 'confirm_url': service.get_confrim_url(user.id)},
            to_email=user.email,
        )

        return Response(
            {'detail': _('Confirmation email has been sent')},
            status=status.HTTP_201_CREATED,
        )


class LoginView(auth_views.LoginView):
    serializer_class = serializers.LoginSerializer


class LogoutView(auth_views.LogoutView):
    allowed_methods = ('POST', 'OPTIONS')

    def session_logout(self):
        django_logout(self.request)

    def logout(self, request):
        response = full_logout(request)
        return response


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = PasswordResetService()

        service.reset_password(email=serializer.validated_data['email'])

        return Response(
            {'detail': _('Password reset e-mail has been sent.')},
            status=status.HTTP_200_OK,
        )


class PasswordResetConfirmView(GenericAPIView):
    serializer_class = serializers.PasswordResetConfirmSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = PasswordResetService()

        service.reset_confirm(serializer.validated_data)

        return Response(
            {'detail': _('Password has been reset with the new password.')},
            status=status.HTTP_200_OK,
        )


class VerifyEmailView(GenericAPIView):
    serializer_class = serializers.VerifyEmailSerializer
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AuthAppService()

        service.confirm_email(serializer.validated_data['key'])

        return Response(
            {'detail': _('Email verified')},
            status=status.HTTP_200_OK,
        )
