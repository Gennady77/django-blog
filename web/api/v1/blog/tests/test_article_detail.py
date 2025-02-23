import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from .fb_factories import ArticleFactory

pytestmark = [pytest.mark.django_db]

def test_get_article_detail(client: Client):
    article = ArticleFactory.create()

    id = article.id

    url = reverse('api:v1:blog:detail', args=( id, ))

    response = client.get(url)

    assert response.status_code == status.HTTP_200_OK
    assert response.data['id'] == id
