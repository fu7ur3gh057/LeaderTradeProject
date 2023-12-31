from django.contrib.auth.models import AnonymousUser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters, permissions
from rest_framework.request import Request
from rest_framework.response import Response

from products.api.filters import ProductFilter
from products.api.pagination import ProductPagination
from products.api.serializers import (
    CategoryTreeSerializer,
    ProductSerializer,
    CategorySerializer,
    ProductDetailSerializer,
    ProductBrandSerializer,
)
from products.models import Category, Product
from src.services.redis.deps import redis_connection


class CategoryTreeAPIView(generics.ListAPIView):
    serializer_class = CategoryTreeSerializer
    queryset = Category.objects.all()

    def get_queryset(self) -> list[Category]:
        return self.queryset.filter(parent__isnull=True)


class CategoryListAPIView(generics.GenericAPIView):
    serializer_class = CategoryTreeSerializer

    def get(self, request: Request, slug: str) -> Response:
        category = Category.objects.filter(slug=slug).first()
        if not category:
            return Response("Category not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(category)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AncestorsCategoryListAPIView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request: Request) -> Response:
        category_list = Category.objects.filter(parent__isnull=True)
        serializer_list = self.serializer_class(category_list, many=True)
        return Response(serializer_list.data, status=status.HTTP_200_OK)


class ProductFilterAPIView(generics.ListAPIView):
    serializer_class = ProductSerializer
    pagination_class = ProductPagination
    queryset = Product.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = ProductFilter
    search_fields = [
        "type",
        "min_price",
        "max_price",
        "color",
    ]

    def get_queryset(self) -> list[Product]:
        return self.queryset.filter(rest__gt=0).order_by("-created_at")


class ProductDetailAPIView(generics.GenericAPIView):
    serializer_class = ProductDetailSerializer

    def get(self, request: Request, slug: str) -> Response:
        product = Product.objects.all().filter(slug=slug).first()
        if not product:
            return Response("Product not found", status=status.HTTP_404_NOT_FOUND)
        product.add_view()
        user = request.user
        # save as viewed product to Redis
        if user is not AnonymousUser:
            redis_client = redis_connection()
            redis_client.cache_product(user_id=user.id, product_id=product.pk_id)
        serializer = self.serializer_class(product)
        return Response(serializer.data)


class ProductBrandListAPIView(generics.GenericAPIView):
    serializer_class = ProductBrandSerializer

    def get(self, request: Request) -> Response:
        products = Product.objects.all()
        brands = [product.brand for product in products if product.brand is not None]
        serializer_list = self.serializer_class(brands, many=True)
        return Response(serializer_list.data, status=status.HTTP_200_OK)


class PopularProductListAPIView(generics.GenericAPIView):
    serializer_class = ProductSerializer

    def get(self, request: Request) -> Response:
        products = Product.objects.order_by("-views")[:16]
        serializer_list = self.serializer_class(products, many=True)
        return Response(serializer_list.data, status=status.HTTP_200_OK)


class ViewedProductListAPIView(generics.GenericAPIView):
    serializer_class = ProductSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request: Request) -> Response:
        user = request.user
        redis_client = redis_connection()
        product_id_list = redis_client.get_cached_products(user_id=user.id)
        products = [
            Product.objects.get(pk_id=product_id)
            for product_id in product_id_list
            if Product.objects.filter(pk_id=product_id).exists()
        ]
        serializer_list = self.serializer_class(products[:16], many=True)
        return Response(serializer_list.data, status=status.HTTP_200_OK)
