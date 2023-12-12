from django.urls import path

from src.apps.actions.api.views import (
    CreateFormApplicationAPIView,
    CreateCallRequestAPIView,
    PortfolioListAPIView,
    PortfolioDetailAPIView,
    PortfolioListByMakeAPIView,
    ReviewListAPIView,
)

urlpatterns = [
    path(
        "create-form",
        CreateFormApplicationAPIView.as_view(),
        name="create-form-application",
    ),
    path(
        "create-call",
        CreateCallRequestAPIView.as_view(),
        name="create-call-request",
    ),
    path("reviews/", ReviewListAPIView.as_view(), name="reviews"),
    path("portfolios/", PortfolioListAPIView.as_view(), name="portfolios"),
    path(
        "portfolios/detail/<slug>/",
        PortfolioDetailAPIView.as_view(),
        name="portfolios-detail",
    ),
    path(
        "portfolios/make/<make_pk>/",
        PortfolioListByMakeAPIView.as_view(),
        name="portfolios-make",
    ),
]
