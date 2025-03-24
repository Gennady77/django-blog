from unittest import mock
from unittest.mock import patch

import pytest
from django.test import Client
from django.urls import reverse_lazy
from rest_framework import status

from main.mixins import ReCaptchaMixin
from main.validators import validate_recaptcha

pytestmark = [pytest.mark.django_db]

LOGIN_URL = reverse_lazy('api:v1:auth_app:sign-in')

def test_login_success(client: Client, user, mock_recaptcha):
    data = {
        'email': 'harley.quinn@email.com',
        'password': 'some_p@ssword',
        'g_recaptcha_response': 'qwqwqwqwqwqwqwqw'
    }

    response = client.post(LOGIN_URL, data)

    assert response.status_code == status.HTTP_200_OK

def test_login_captcha_required(client: Client, user):
    data = {
        'email': 'harley.quinn@email.com',
        'password': 'some_p@ssword',
    }

    response = client.post(LOGIN_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['g_recaptcha_response'][0].code == 'required'

def test_login_wrong_captcha(client: Client, user, mock_recaptcha_fail):
    data = {
        'email': 'harley.quinn@email.com',
        'password': 'some_p@ssword',
        'g_recaptcha_response': 'qwqwqwqwqwqwqwqw'
    }

    response = client.post(LOGIN_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['g_recaptcha_response']['recaptcha'].code == 'wrong_recaptcha'

def test_wrong_credentials(client: Client, user, mock_recaptcha):
    data = {
        'email': 'harley.quinn@email.com',
        'password': 'some_fail_p@ssword',
        'g_recaptcha_response': 'qwqwqwqwqwqwqwqw'
    }

    response = client.post(LOGIN_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'][0].code == 'wrong_credentials'


def test_user_inactive(client: Client, inactive_user, mock_recaptcha):
    data = {
        'email': 'harley.quinn@email.com',
        'password': 'some_p@ssword',
        'g_recaptcha_response': 'qwqwqwqwqwqwqwqw'
    }

    response = client.post(LOGIN_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['email'][0].code == 'not_active'
