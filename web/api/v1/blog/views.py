import re
import textwrap

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet, GenericViewSet

from api.v1.blog.services import ArticleQueryService, CommentService
from main.pagination import BasePageNumberPagination, BaseLimitOffsetPagination, BaseCursorPagination
from . import serializers
from .serializers import CommentResponseSerializer


class ArticleListView(GenericViewSet):
    permission_classes = (AllowAny,)
    serializer_class = serializers.ArticleListSerializer
    pagination_class = BasePageNumberPagination

    def list(self, request):
        queryset = ArticleQueryService().article_list()

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)

        return self.get_paginated_response(serializer.data)


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

class CommentView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.CommentPostSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = CommentService(user=request.user)

        service.add_comment(serializer.data)

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )

class CommentListView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.CommentResponseSerializer

    def get(self, request, article_id):
        service = CommentService(user=request.user)

        queryset = service.comment_list(article_id)

        response_serializer = CommentResponseSerializer(queryset, many=True)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

class CommentAnswerListView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = serializers.CommentResponseSerializer

    def get(self, request, article_id, parent_id):
        service = CommentService(user=request.user)

        queryset = service.comment_answer_list(article_id, parent_id)

        response_serializer = CommentResponseSerializer(queryset, many=True)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )
