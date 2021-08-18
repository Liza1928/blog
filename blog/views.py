from rest_framework import viewsets

from helpers.access import AccessEditAuthor, IsSuperUser, ReadOnly
from helpers.swagger_decorator import swagger_auto_viewset
from .models import Post, Category
from users.models import User
from .serializers import (
    PostWriteSerializer,
    PostReadSerializer,
    CategoryReadSerializer,
    CategoryWriteSerializer,
    AuthorReadSerializer,
)

from drf_rw_serializers import viewsets


@swagger_auto_viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    read_serializer_class  = PostReadSerializer
    write_serializer_class  = PostWriteSerializer
    serializer_class = read_serializer_class
    permission_classes = [IsSuperUser | AccessEditAuthor]


@swagger_auto_viewset
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    read_serializer_class  = CategoryReadSerializer
    write_serializer_class  = CategoryWriteSerializer
    serializer_class = read_serializer_class
    permission_classes = [IsSuperUser | ReadOnly]


@swagger_auto_viewset
class AuthorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.get_author_queryset()
    serializer_class = AuthorReadSerializer
    permission_classes = [ReadOnly]
