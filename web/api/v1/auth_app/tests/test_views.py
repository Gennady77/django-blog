from django.core import mail
from django.test import Client, TestCase
from django.urls import reverse
from rest_framework import status

from main.models import User

SIGN_UP_URL = reverse('api:v1:auth_app:sign-up')


class ViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def check_required(self, required_key):
        correctPostData = {
            'first_name': 'TestName',
            'last_name': 'TestLastName',
            'email': 'test.email@asd.com',
            'password_1': '12345',
            'password_2': '12345',
        }

        del correctPostData[required_key]

        response = self.client.post(SIGN_UP_URL, correctPostData, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data[required_key][0].code, 'required')

    def test_with_correct_data(self):
        correctPostData = {
            'first_name': 'TestName',
            'last_name': 'TestLastName',
            'email': 'test.email@asd.com',
            'password_1': '12345',
            'password_2': '12345',
        }

        response = self.client.post(
            reverse('api:v1:auth_app:sign-up'), correctPostData, content_type='application/json'
        )

        testUser = User.objects.get(email='test.email@asd.com')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(testUser.full_name, 'TestName TestLastName')

    def test_first_name_required(self):
        self.check_required('first_name')

    def test_last_name_required(self):
        self.check_required('last_name')

    def test_email_required(self):
        self.check_required('email')

    def test_password_1_required(self):
        self.check_required('password_1')

    def test_password_2_required(self):
        self.check_required('password_1')

    def test_unique_email(self):
        User.objects.create_user(email='test.email@asd.com', password=None)

        correctPostData = {
            'first_name': 'TestName',
            'last_name': 'TestLastName',
            'email': 'test.email@asd.com',
            'password_1': '12345',
            'password_2': '12345',
        }

        response = self.client.post(
            reverse('api:v1:auth_app:sign-up'), correctPostData, content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['email'][0].code, 'invalid')

    def test_pass1_pass2(self):
        correctPostData = {
            'first_name': 'TestName',
            'last_name': 'TestLastName',
            'email': 'test.email@asd.com',
            'password_1': '12345',
            'password_2': '67890',
        }

        response = self.client.post(
            reverse('api:v1:auth_app:sign-up'), correctPostData, content_type='application/json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['password_2'][0].code, 'invalid')
