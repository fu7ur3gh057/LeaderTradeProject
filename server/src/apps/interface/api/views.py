from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, permissions
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.interface.api.serializers import BannerSerializer
from src.apps.interface.models import Banner


class BannerListAPIView(generics.GenericAPIView):
    serializer_class = BannerSerializer

    def get(self, request: Request) -> Response:
        banners = Banner.objects.all()
        serializer_list = self.serializer_class(banners, many=True)
        return Response(serializer_list.data, status=status.HTTP_200_OK)
