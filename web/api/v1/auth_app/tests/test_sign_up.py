import re
from django.core import mail
from django.urls import reverse_lazy
import pytest

from django.test import Client

from main.models import User

pytestmark = [pytest.mark.django_db]

SIGN_UP_URL = reverse_lazy('api:v1:auth_app:sign-up')
VERIFY_EMAIL_URL = reverse_lazy('api:v1:auth_app:sign-up-verify')

def test_sign_up(client: Client):
	correctPostData = {
		'first_name': 'Jack',
		'last_name': 'Nicholson',
		'email': 'jack.nicholson@asd.com',
		'password_1': '12345',
		'password_2': '12345'
	}

	client.post(SIGN_UP_URL, correctPostData)

	m = re.findall(r'verify-email\/\?confirm_key=(.*?)\">', mail.outbox[0].message().as_string())

	data = {
		'key': m[0]
	}

	client.post(VERIFY_EMAIL_URL, data)

	user = User.objects.get(email='jack.nicholson@asd.com')

	assert(user.is_active, True)
