from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, filters
from rest_framework.request import Request
from rest_framework.response import Response

from news.api.filters import PostFilter
from news.api.pagination import PostPagination
from news.api.serializers import PostSerializer
from news.models import Post


class PostFilterAPIView(generics.ListAPIView):
    serializer_class = PostSerializer
    pagination_class = PostPagination
    queryset = Post.objects.all()
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_class = PostFilter
    search_fields = ["title"]

    def get_queryset(self) -> list[Post]:
        return self.queryset.order_by("-created_at")


class PostDetailAPIView(generics.GenericAPIView):
    serializer_class = PostSerializer

    def get(self, request: Request, slug: str) -> Response:
        post = Post.objects.filter(slug=slug).first()
        if post is None:
            return Response("Post not found", status=status.HTTP_404_NOT_FOUND)
        serializer = self.serializer_class(post)
        return Response(serializer.data, status=status.HTTP_200_OK)
