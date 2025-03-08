import re
import textwrap

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from api.v1.blog.services import ArticleQueryService
from main.pagination import BasePageNumberPagination, BaseLimitOffsetPagination, BaseCursorPagination
from . import serializers


class ArticleListView(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ArticleListSerializer
    pagination_class = BasePageNumberPagination

    def list(self, request):
        queryset = ArticleQueryService().article_list()

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)

            for article in serializer.data:
                article['content'] = textwrap.shorten(re.sub(r'<.*?>', '', article['content']), 200)

            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


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
