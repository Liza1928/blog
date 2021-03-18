from rest_framework import viewsets
from rest_framework.generics import ListAPIView, get_object_or_404

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

    serializer_class_in = PostWriteSerializer
    serializer_class_out = PostReadSerializer
    serializer_class = serializer_class_out
    queryset = Post.objects.all()
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
    #permission_classes = [ReadOnly]


# class ArticleView(viewsets.ViewSet):
#
#     queryset = User.objects.get_author_queryset()
#
#     def list(self, request):
#         serializer = ArticleSerializer(self.queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#
#         user = get_object_or_404(self.queryset, pk=pk)
#         serializer = ArticleSerializer(user)
#         return Response(serializer.data)