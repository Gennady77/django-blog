from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet

from api.v1.blog.services import ArticleQueryService
from main.pagination import BasePageNumberPagination, BaseLimitOffsetPagination, BaseCursorPagination
from . import serializers


class ArticleListView(ModelViewSet):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ArticleListSerializer
    pagination_class = BaseLimitOffsetPagination
    queryset = ArticleQueryService().article_list()

class ArticleDetailView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ArticleListSerializer

    def get(self, request, id):
        queryset = ArticleQueryService().article_detail(id)
        serializer = serializers.ArticleListSerializer(queryset)

        return Response(
            serializer.data,
            status = status.HTTP_200_OK
        )
