import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db]

AVATAR_URL = reverse('api:v1:profile:avatar');

def test_profile_avatar_success(authenticated_client: Client, image_content_file):
    data = {
        'avatar': image_content_file
    }

    response = authenticated_client.post(AVATAR_URL, data)

    assert response.status_code == status.HTTP_200_OK
