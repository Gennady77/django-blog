import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from api.v1.auth_app.services import PasswordResetGenerator

pytestmark = [pytest.mark.django_db]

RESET_CONFIRM_URL = reverse('api:v1:auth_app:reset-password-confirm')
LOGIN_URL = reverse('api:v1:auth_app:sign-in')


def test_reset_confirm_succeful(client: Client, user_uid_token):
    data = {
        'password_1': '123456789',
        'password_2': '123456789',
        'uid': user_uid_token['uid'],
        'token': user_uid_token['token'],
    }

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_200_OK

    login_response = client.post(LOGIN_URL, {'email': 'harley.quinn@email.com', 'password': '123456789'})

    assert login_response.status_code == status.HTTP_200_OK


def test_password_too_short(client, user_uid_token):
    data = {'password_1': '123', 'password_2': '123', 'uid': user_uid_token['uid'], 'token': user_uid_token['token']}

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['password_1'][0].code == 'min_length'


def test_password_too_long(client, user_uid_token):
    data = {
        'password_1': '123etqityqrtwerutrtywetryuwertuftsydftsyftyfyyrtywrtywrwryweurtweyurt',
        'password_2': '123etqityqrtwerutrtywetryuwertuftsydftsyftyfyyrtywrtywrwryweurtweyurt',
        'uid': user_uid_token['uid'],
        'token': user_uid_token['token'],
    }

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['password_1'][0].code == 'max_length'


def test_passwords_is_not_equal(client, user_uid_token):
    data = {
        'password_1': '322138123',
        'password_2': '856785464',
        'uid': user_uid_token['uid'],
        'token': user_uid_token['token'],
    }

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['password_2'][0].code == 'password_not_match'


def test_passwords_uid_required(client, user_uid_token):
    data = {'password_1': '322138123', 'password_2': '322138123', 'token': user_uid_token['token']}

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['uid'][0].code == 'required'


def test_passwords_invalid_uid(client, user_uid_token):
    data = {'password_1': '322138123', 'password_2': '322138123', 'uid': '22', 'token': user_uid_token['token']}

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['detail'].code == 'user_does_not_exists'


def test_passwords_token_required(client, user_uid_token):
    data = {
        'password_1': '322138123',
        'password_2': '322138123',
        'uid': user_uid_token['uid'],
    }

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['token'][0].code == 'required'


def test_passwords_token_invalid(client, user_uid_token):
    data = {'password_1': '322138123', 'password_2': '322138123', 'uid': user_uid_token['uid'], 'token': '123'}

    response = client.post(RESET_CONFIRM_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['token'].code == 'token_is_not_valid'
