from helpers.access import AccessEditAuthor, IsSuperUser, ReadOnly
from .models import Post, Category
from users.models import User
from .serializers import (
    PostWriteSerializer, PostReadSerializer, CategorySerializer, AuthorReadSerializer)

from helpers.views import ReadWriteModelViewSet


class PostViewSet(ReadWriteModelViewSet):

    serializer_class_in = PostWriteSerializer
    serializer_class_out = PostReadSerializer
    serializer_class = serializer_class_out
    queryset = Post.objects.all()
    permission_classes = [IsSuperUser | AccessEditAuthor]


class CategoryViewSet(ReadWriteModelViewSet):
    queryset = Category.objects.all()
    serializer_class_out = CategorySerializer
    serializer_class_in = CategorySerializer
    serializer_class = serializer_class_out
    permission_classes = [IsSuperUser | ReadOnly]


class AuthorViewSet(ReadWriteModelViewSet):
    queryset = User.objects.get_author_queryset()
    serializer_class_out = AuthorReadSerializer
    serializer_class_in = AuthorReadSerializer
    serializer_class = serializer_class_out
    permission_classes = [IsSuperUser | ReadOnly]

