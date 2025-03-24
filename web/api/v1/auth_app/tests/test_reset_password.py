import pytest
from django.core import mail
from django.test import Client
from django.urls import reverse_lazy
from rest_framework import status

from api.v1.auth_app.services import PasswordResetGenerator

pytestmark = [pytest.mark.django_db]

PASSWORD_RESET_URL = reverse_lazy('api:v1:auth_app:reset-password')


def test_password_reset_success(client: Client, user, mock_recaptcha):
    data = {
        'email': 'harley.quinn@email.com',
        'g_recaptcha_response': 'qwqwqwqwqwqwqwqw',
    }

    response = client.post(PASSWORD_RESET_URL, data)

    assert response.status_code == status.HTTP_200_OK
    assert len(mail.outbox) > 0


def test_password_reset_incorrect_email(client: Client):
    data = {'email': 'asdfg'}

    response = client.post(PASSWORD_RESET_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert len(mail.outbox) == 0


def test_password_reset_nonexistent_email(client: Client, mock_recaptcha):
    data = {
        'email': 'bob.marley@email.com',
        'g_recaptcha_response': 'qwqwqwqwqwqwqwqw',
    }

    response = client.post(PASSWORD_RESET_URL, data)

    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert len(mail.outbox) == 0
