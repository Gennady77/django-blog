import pytest
from django.urls import reverse
from rest_framework import status

pytestmark = [pytest.mark.django_db]

def test_comment_list_success(client, comment_list):
    id = comment_list.id
    url =  reverse('api:v1:blog:comment_list', args=(id, ))

    request = client.get(url)

    assert request.status_code == status.HTTP_200_OK

def test_comment_list_with_answer(client, comment_answer_list):
    (article, comment) = comment_answer_list
    url = reverse('api:v1:blog:comment_list', args=(article.id,))

    request = client.get(url)

    assert request.status_code == status.HTTP_200_OK
    assert len(request.data) == 1
    assert len(request.data[0]['children']) == 5

def test_comment_list_wrong_article(client, comment_list):
    url = reverse('api:v1:blog:comment_list', args=(10000,))

    request = client.get(url)

    assert request.status_code == status.HTTP_200_OK
    assert len(request.data) == 0

def test_comment_answer_list_success(client, comment_answer_list):
    (article, comment) = comment_answer_list

    url = reverse('api:v1:blog:comment_answer_list', args=(article.id, comment.id))

    request = client.get(url)

    assert request.status_code == status.HTTP_200_OK
    assert len(request.data) == 5

