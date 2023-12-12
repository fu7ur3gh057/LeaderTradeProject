from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.profiles.api.serializers import (
    ProfileSerializer,
    LegalCardSerializer,
    ProfileUpdateSerializer,
    LegalCardUpdateSerializer,
)


class ProfileAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = ProfileSerializer

    def get(self, request: Request) -> Response:
        user = request.user
        profile = user.profile
        serializer = self.serializer_class(profile)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateProfileAPIView(generics.GenericAPIView):
    serializer_class = ProfileUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = (JSONParser, MultiPartParser)

    @swagger_auto_schema(request_body=ProfileUpdateSerializer)
    def patch(self, request: Request) -> Response:
        data = request.data
        profile = request.user.profile
        serializer = self.serializer_class(profile, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)


class LegalCardAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = LegalCardSerializer

    def get(self, request: Request) -> Response:
        user = request.user
        profile = user.profile
        if not profile.is_legal:
            return Response("Profile not legal", status=status.HTTP_200_OK)
        legal_card = profile.card
        serializer = self.serializer_class(legal_card)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LegalCardUpdateAPIView(generics.GenericAPIView):
    permissions_classes = [permissions.IsAuthenticated]
    serializer_class = LegalCardUpdateSerializer

    @swagger_auto_schema(request_body=LegalCardUpdateSerializer)
    def patch(self, request: Request) -> Response:
        data = request.data
        legal_card = request.user.profile.card
        serializer = self.serializer_class(legal_card, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
