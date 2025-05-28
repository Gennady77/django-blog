import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db]

PROFILE_URL = reverse('api:v1:profile:profile')

def test_profile_success(authenticated_client: Client, user):
    response = authenticated_client.get(PROFILE_URL)

    expected_data = {
        'id': user.id,
        'full_name': user.full_name,
        'email': user.email
    }

    assert response.status_code == status.HTTP_200_OK
    assert response.data == expected_data
