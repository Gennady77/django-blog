import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from blog.models import Comment

pytestmark = [pytest.mark.django_db]

COMMENT_URL = reverse('api:v1:blog:comment')
LOGIN_URL = reverse('api:v1:auth_app:sign-in')

def test_post_comment_success(authenticated_client: Client, article):
    data = {
        'content': 'test comment',
        'article': article.id
    }

    response = authenticated_client.post(COMMENT_URL, data)

    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_post_comment_answer_success(authenticated_client: Client, article, user):
    instComment = Comment.objects.create(user_id=user.id, article_id=article.id, content='test comment')

    data = {
        'content': 'test comment 111',
        'article': article.id,
        'parent': instComment.id
    }

    response = authenticated_client.post(COMMENT_URL, data)

    queryset = Comment.objects.get(content='test comment 111')

    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert queryset.parent_id == instComment.id

@pytest.mark.parametrize(
    ['data', 'field_error', 'code_error'],
    (
        ({'article': 1}, 'content', 'required'),
        ({'content': 'test comment'}, 'article', 'required'),
        ({'article': 1000, 'content': 'test comment'}, 'article', 'article_not_found')
    )
)
def test_invalid_comment_create(authenticated_client: Client, article, data, field_error, code_error):
    response = authenticated_client.post(COMMENT_URL, data)

    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data[field_error][0].code == code_error
