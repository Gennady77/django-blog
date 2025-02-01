from django.urls import reverse_lazy
from rest_framework import status

import pytest

from django.test import Client

pytestmark = [pytest.mark.django_db]

LOGIN_URL = reverse_lazy('api:v1:auth_app:sign-in')

def test_login_success(client: Client, user):
	data = {
		'email': 'harley.quinn@email.com',
		'password': 'some_p@ssword',
	}

	response = client.post(LOGIN_URL, data)

	assert response.status_code == status.HTTP_200_OK

def test_wrong_credentials(client: Client, user):
	data = {
		'email': 'harley.quinn@email.com',
		'password': 'some_fail_p@ssword',
	}

	response = client.post(LOGIN_URL, data)

	print(f'{response=}')

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.data['email'][0].code == 'wrong_credentials'

def test_user_inactive(client: Client, inactive_user):
	data = {
		'email': 'harley.quinn@email.com',
		'password': 'some_p@ssword',
	}

	response = client.post(LOGIN_URL, data)

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.data['email'][0].code == 'not_active'