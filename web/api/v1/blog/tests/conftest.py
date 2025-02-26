import pytest

from .fb_factories import ArticleFactory

@pytest.fixture()
def article_list():
    ArticleFactory.create_batch(12)
