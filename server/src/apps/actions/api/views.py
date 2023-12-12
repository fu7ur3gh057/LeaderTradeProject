from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.request import Request
from rest_framework.response import Response

from src.apps.actions.api.pagination import PortfolioPagination, ReviewPagination
from src.apps.actions.api.serializers import (
    PortfolioSerializer,
    PortfolioDetailSerializer,
    ReviewSerializer,
    FormApplicationSerializer,
    CallRequestSerializer,
)
from src.apps.actions.models import Portfolio, Review


class PortfolioListAPIView(generics.ListAPIView):
    serializer_class = PortfolioSerializer
    pagination_class = PortfolioPagination
    queryset = Portfolio.objects.all()

    def get_queryset(self) -> list[Portfolio]:
        return self.queryset


class PortfolioListByMakeAPIView(generics.GenericAPIView):
    serializer_class = PortfolioSerializer
    pagination_class = PortfolioPagination
    queryset = Portfolio.objects.all()
    lookup_url_kwarg = "make_pk"

    def get_queryset(self) -> list[Portfolio]:
        make_pk = self.kwargs.get(self.lookup_url_kwarg)
        return self.queryset.filter(make__pk_id=make_pk).order_by("-created_at")


class PortfolioDetailAPIView(generics.GenericAPIView):
    serializer_class = PortfolioDetailSerializer

    def get(self, request: Request, slug: str) -> Response:
        portfolio = Portfolio.objects.filter(slug=slug).first()
        if portfolio is None:
            return Response("Portfolio not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(portfolio)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    pagination_class = ReviewPagination
    queryset = Review.objects.all()

    def get_queryset(self) -> list[Review]:
        return self.queryset.order_by("-date")


class CreateFormApplicationAPIView(generics.GenericAPIView):
    serializer_class = FormApplicationSerializer

    @swagger_auto_schema(request_body=FormApplicationSerializer)
    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateCallRequestAPIView(generics.GenericAPIView):
    serializer_class = CallRequestSerializer

    @swagger_auto_schema(request_body=CallRequestSerializer)
    def post(self, request: Request) -> Response:
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
