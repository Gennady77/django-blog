from django.conf import settings
from django.urls import reverse_lazy
from django.core import signing
from datetime import datetime, timedelta
from rest_framework import status
import pytest

from django.test import Client

pytestmark = [pytest.mark.django_db]

VERIFY_EMAIL_URL = reverse_lazy('api:v1:auth_app:sign-up-verify')

def test_success_verify(client: Client, inactive_user):
	data = {
		'key': signing.dumps(inactive_user.id)
	}

	response = client.post(VERIFY_EMAIL_URL, data)

	assert response.status_code == status.HTTP_200_OK

	inactive_user.refresh_from_db()
	assert inactive_user.is_active is True

def test_unsuccess_verify(client: Client):
	data = {
		'key': 'qwqwq'
	}

	response = client.post(VERIFY_EMAIL_URL, data)

	assert response.status_code == status.HTTP_400_BAD_REQUEST

def test_expired_key(client: Client, freezer, inactive_user):
	key = signing.dumps(inactive_user.id)

	now = datetime.now()
	new_now = now + timedelta(hours=2, seconds=settings.EMAIL_CONFIRMATION_EXPIRE_SECONDS)

	freezer.move_to(new_now)

	response = client.post(VERIFY_EMAIL_URL, { 'key': key })

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.data['key'].code == 'invalid'

def test_user_exists(client, inactive_user):
	key = signing.dumps(inactive_user.id)

	inactive_user.delete()

	response = client.post(VERIFY_EMAIL_URL, { 'key': key })

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.data['error'].code == 'user_does_not_exists'

def test_user_active_already(client, user):
	key = signing.dumps(user.id)

	response = client.post(VERIFY_EMAIL_URL, { 'key': key })

	assert response.status_code == status.HTTP_400_BAD_REQUEST
	assert response.data['error'].code == 'user_is_already_active'
