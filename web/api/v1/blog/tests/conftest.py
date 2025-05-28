import pytest

from blog.choices import ArticleStatus
from blog.models import Article, Category, Comment
from .fb_factories import ArticleFactory, CommentFactory


@pytest.fixture()
def article_list():
    ArticleFactory.create_batch(12)

@pytest.fixture()
def category() -> Category:
    category = Category(name='marketplace')

    category.save()

    return category

@pytest.fixture()
def article(category, user) -> Article:
    article = Article(
        category=category,
        title='article test',
        content='some article content',
        author = user,
        status = ArticleStatus.ACTIVE
    )

    article.save()

    return article

@pytest.fixture()
def comment_list() -> Article:
    article_inst = ArticleFactory()
    CommentFactory.create_batch(5, article=article_inst)

    return article_inst

@pytest.fixture()
def comment_answer_list() -> (Article, Comment):
    article_inst = ArticleFactory.create()

    comment_inst = CommentFactory.create(article=article_inst)

    CommentFactory.create_batch(5, article=article_inst, parent=comment_inst)

    return article_inst, comment_inst

