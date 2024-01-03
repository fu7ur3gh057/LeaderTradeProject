from django.urls import path, include
from products.api.views import (
    CategoryTreeAPIView,
    CategoryListAPIView,
    AncestorsCategoryListAPIView,
    ProductDetailAPIView,
    ProductFilterAPIView,
    ViewedProductListAPIView,
    PopularProductListAPIView,
    ProductBrandListAPIView,
)

urlpatterns = [
    path("category/tree/", CategoryTreeAPIView.as_view(), name="category-tree"),
    path(
        "category/ancestors/",
        AncestorsCategoryListAPIView.as_view(),
        name="category-ancestors",
    ),
    path("filter/", ProductFilterAPIView.as_view(), name="product-filter"),
    path("viewed/", ViewedProductListAPIView.as_view(), name="product-viewed"),
    path("popular/", PopularProductListAPIView.as_view(), name="product-popular"),
    path("brands/", ProductBrandListAPIView.as_view(), name="product-brands"),
    path("category/<slug>/", CategoryListAPIView.as_view(), name="category-list"),
    path("detail/<slug>/", ProductDetailAPIView.as_view(), name="product-detail"),
]
