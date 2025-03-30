from numbers import Number

from django.db.models import Count, QuerySet

from blog.choices import ArticleStatus
from blog.models import Article, Category


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
        return Article.objects.get(id=id)
