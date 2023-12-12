from django.urls import path

from src.apps.interface.api.views import BannerListAPIView

urlpatterns = [
    path("banners/", BannerListAPIView.as_view(), name="banner-list"),
]
