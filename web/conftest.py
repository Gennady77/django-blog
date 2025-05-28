from typing import NamedTuple

import pytest
from dj_rest_auth.app_settings import api_settings
from dj_rest_auth.utils import jwt_encode
from django.contrib.auth import get_user_model
from django.http import SimpleCookie
from django.urls import reverse

from main.models import UserType
from django.test import Client

pyteststmark = [pytest.mark.django_db]
User: UserType = get_user_model()

LOGIN_URL = reverse('api:v1:auth_app:sign-in')

class UserToken(NamedTuple):
    access_token: str
    refresh_token: str


@pytest.fixture()
def user() -> User:
    user = User.objects.create_user(
        email='harley.quinn@email.com',
        password='some_p@ssword',
        first_name='Margot',
        last_name='Robbie',
    )
    return user

@pytest.fixture()
def jwt_cookie(user):
    access_token, refresh_token = jwt_encode(user)

    return SimpleCookie({
        api_settings.JWT_AUTH_COOKIE: access_token,
        api_settings.JWT_AUTH_REFRESH_COOKIE: refresh_token
    })

@pytest.fixture()
def authenticated_client(client: Client, jwt_cookie) -> Client:
    client.cookies = jwt_cookie

    return client
