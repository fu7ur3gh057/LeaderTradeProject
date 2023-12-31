from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg import openapi
from drf_yasg.openapi import Parameter
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, status, permissions

from src.apps.orders.api.serializers import (
    BasketSerializer,
    FavoritesSerializer,
    DocumentSerializer,
)
from src.apps.orders.models import Order, Document
from products.models import Product


class BasketAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = BasketSerializer

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        basket = profile.basket
        serializer = self.serializer_class(basket)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def increase_basket_api_view(request: Request, product_id: str) -> Response:
    basket = request.user.profile.basket
    get_object_or_404(Product, pk_id=int(product_id))
    basket.increase_product(product_id=product_id)
    serializer = BasketSerializer(basket)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def decrease_basket_api_view(request: Request, product_id: str) -> Response:
    basket = request.user.profile.basket
    get_object_or_404(Product, pk_id=int(product_id))
    basket.decrease_product(product_id=product_id)
    serializer = BasketSerializer(basket)
    return Response(serializer.data, status=status.HTTP_200_OK)


class FavoritesAPIView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = FavoritesSerializer

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        favorites = profile.favorites
        serializer = self.serializer_class(favorites)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def add_favorites_api_view(request: Request, product_id: str) -> Response:
    favorites = request.user.profile.favorites
    product = get_object_or_404(Product, pk_id=int(product_id))
    favorites.add_product(product_id=product.pk_id)
    serializer = FavoritesSerializer(favorites)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def remove_favorites_api_view(request: Request, product_id: str) -> Response:
    favorites = request.user.profile.favorites
    product = get_object_or_404(Product, pk_id=int(product_id))
    favorites.remove_product(product_id=product.pk_id)
    serializer = FavoritesSerializer(favorites)
    return Response(serializer.data, status=status.HTTP_200_OK)


class GetDocumentListAPIView(generics.GenericAPIView):
    serializer_class = DocumentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        profile = request.user.profile
        documents = Document.objects.filter(order__profile=profile)
        serializer_list = self.serializer_class(documents, many=True)
        return Response(serializer_list.data, status=status.HTTP_200_OK)
