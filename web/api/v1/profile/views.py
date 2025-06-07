from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser
from sentry_sdk.integrations.beam import raise_exception

from . import serializers
from .services import AvatarService


class ProfileView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileSerializer

    def get(self,request):
        serializer = self.get_serializer(request.user)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

class ProfileAvatarView(GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProfileAvatarSerializer
    parser_classes = (MultiPartParser,)

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        service = AvatarService()

        service.save(request.user, serializer.validated_data['avatar'])

        return Response(status=status.HTTP_200_OK)
