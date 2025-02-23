import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from .fb_factories import ArticleFactory

pytestmark = [pytest.mark.django_db]

GET_ARTICLES_URL = reverse('api:v1:blog:articles')

def test_article_list_success(client: Client):
    ARTICLE_COUNT = 12
    LIMIT = 7

    ArticleFactory.create_batch(ARTICLE_COUNT)

    response = client.get(GET_ARTICLES_URL, data={ 'limit': LIMIT })

    assert response.status_code == status.HTTP_200_OK
    assert response.data['count'] == ARTICLE_COUNT
    assert len(response.data['results']) == LIMIT
