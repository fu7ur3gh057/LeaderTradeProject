from django.urls import path, include

from src.apps.profiles.api.views import (
    ProfileAPIView,
    LegalCardAPIView,
    UpdateProfileAPIView,
    LegalCardUpdateAPIView,
)

urlpatterns = [
    path("me/", ProfileAPIView.as_view(), name="profile-me"),
    path("update/", UpdateProfileAPIView.as_view(), name="profile-update"),
    path("legal-card/", LegalCardAPIView.as_view(), name="legal-card"),
    path(
        "legal-card/update/", LegalCardUpdateAPIView.as_view(), name="legal-card-update"
    ),
]
