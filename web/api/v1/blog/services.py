from numbers import Number

from django.db.models import Count, QuerySet, Prefetch
from typing_extensions import NamedTuple, Optional

from api.v1.blog.tests.conftest import article
from blog.choices import ArticleStatus
from blog.models import Article, Category, Comment
from main.models import User


class CreateCommentData(NamedTuple):
    user: Number
    article: Number
    content: str
    parent: Optional[int]


class BlogService:
    @staticmethod
    def category_queryset():
        return Category.objects.all()

    @staticmethod
    def get_active_articles():
        return Article.objects.filter(status=ArticleStatus.ACTIVE).annotate(comments_count=Count('comment_set'))

class ArticleQueryService:
    def article_list(self) -> QuerySet[Article]:
        return Article.objects.all().annotate(comments_count = Count('comment_set')).select_related('author', 'category')

    def article_detail(self, id: Number) -> QuerySet[Article]:
        return Article.objects.annotate(comments_count = Count('comment_set')).get(id=id)

    @staticmethod
    def is_article_exists(article_id: int) -> bool:
        return Article.objects.filter(id=article_id).exists()

class CommentService:
    def __init__(self, user: User):
        self.user = user

    def add_comment(self, validated_data: dict) -> Comment:
        if 'parent' not in validated_data:
            validated_data['parent'] = None

        data = CreateCommentData(**validated_data, user=self.user.id)

        inst = Comment.objects.create(user_id=data.user, article_id=data.article, parent_id=data.parent, content=data.content)

        return inst

    def comment_list(self, article_id) -> QuerySet[Comment]:
        return (Comment
                .objects.filter(article = article_id, parent__isnull=True)
                .select_related('user')
                .order_by('-created')
                .prefetch_related(
                    Prefetch('children', queryset=Comment.objects.all().select_related('user').order_by('-created')))
                )

    def comment_answer_list(self, article_id, parent_id) -> QuerySet[Comment]:
        return Comment.objects.filter(article = article_id, parent = parent_id).select_related('user').order_by('-created')


