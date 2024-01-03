from django.urls import path, include

from news.api.views import PostFilterAPIView, PostDetailAPIView

urlpatterns = [
    path("filter/", PostFilterAPIView.as_view(), name="post-filter"),
    path("<slug>/", PostDetailAPIView.as_view(), name="post-detail"),
]
