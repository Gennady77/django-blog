import re
import textwrap

from django.contrib.auth import get_user_model
from django.db.models import Count
from rest_framework import serializers

from api.v1.blog.services import ArticleQueryService
from blog.models import Article, Category, Comment

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'full_name', 'email')


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ('id', 'user', 'content', 'parent', 'created')


class CategorySerializer(serializers.ModelSerializer):
    slug = serializers.SlugField(read_only=True, allow_unicode=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug')

class ArticleListSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    category = CategorySerializer()
    short_content = serializers.SerializerMethodField(method_name='get_short_content')
    comments_count = serializers.IntegerField()

    def get_short_content(self, obj: Article):
        return textwrap.shorten(re.sub(r'<.*?>', '', obj.content), 200)

    class Meta:
        model = Article
        fields = ('id', 'author', 'title', 'image', 'created', 'category', 'updated', 'content', 'short_content', 'comments_count')



class CommentPostSerializer(serializers.Serializer):
    content = serializers.CharField(max_length=200, required=True)
    article = serializers.IntegerField(required=True)
    parent = serializers.IntegerField(required=False)

    def validate_article(self, article_id):
        if not ArticleQueryService.is_article_exists(article_id):
            raise serializers.ValidationError(code='article_not_found')

        return article_id

class CommentListSerializer(serializers.Serializer):
    article = serializers.IntegerField(required=True)

class CommentResponseSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    children = CommentSerializer(many=True)

    class Meta:
        model = Comment
        fields = ('id', 'content', 'user', 'created', 'parent', 'children')


# class ArticleSerializer(serializers.ModelSerializer):
#     url = serializers.CharField(source='get_absolute_url')
#     author = UserSerializer()
#     category = CategorySerializer()
#     comments_count = serializers.IntegerField()
#
#     class Meta:
#         model = Article
#         fields = ('title', 'url', 'author', 'category', 'created', 'updated', 'comments_count')
#
#
# class FullArticleSerializer(ArticleSerializer):
#     comments = CommentSerializer(source='comment_set', many=True)
#
#     class Meta(ArticleSerializer.Meta):
#         fields = ArticleSerializer.Meta.fields + (
#             'content',
#             'comments',
#         )
