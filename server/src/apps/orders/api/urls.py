from django.urls import path

from src.apps.orders.api.views import (
    BasketAPIView,
    FavoritesAPIView,
    add_favorites_api_view,
    increase_basket_api_view,
    decrease_basket_api_view,
    remove_favorites_api_view,
    GetDocumentListAPIView,
)

urlpatterns = [
    path("basket/", BasketAPIView.as_view(), name="basket"),
    path("favorites/", FavoritesAPIView.as_view(), name="favorites"),
    path("documents/", GetDocumentListAPIView.as_view(), name="documents"),
    path(
        "basket/increase/<product_id>/",
        increase_basket_api_view,
        name="increase-basket",
    ),
    path(
        "basket/decrease/<product_id>/",
        decrease_basket_api_view,
        name="decrease-basket",
    ),
    path(
        "favorites/add/<product_id>/",
        add_favorites_api_view,
        name="add-favorites",
    ),
    path(
        "favorites/remove/<product_id>/",
        remove_favorites_api_view,
        name="remove-favorites",
    ),
]
