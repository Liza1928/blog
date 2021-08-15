from rest_framework import viewsets

from helpers.access import AccessEditAuthor, IsSuperUser, ReadOnly
from .models import Post, Category
from users.models import User
from .serializers import (
    PostWriteSerializer,
    PostReadSerializer,
    CategoryReadSerializer,
    CategoryWriteSerializer,
    AuthorReadSerializer,
)

from helpers.views import ReadWriteModelViewSet


class PostViewSet(ReadWriteModelViewSet):
    queryset = Post.objects.all()
    serializer_class_out = PostReadSerializer
    serializer_class_in = PostWriteSerializer
    serializer_class = serializer_class_out
    permission_classes = [IsSuperUser | AccessEditAuthor]


class CategoryViewSet(ReadWriteModelViewSet):
    queryset = Category.objects.all()
    serializer_class_out = CategoryReadSerializer
    serializer_class_in = CategoryWriteSerializer
    serializer_class = serializer_class_out
    permission_classes = [IsSuperUser | ReadOnly]


class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.get_author_queryset()
    serializer_class = AuthorReadSerializer
    permission_classes = [ReadOnly]
