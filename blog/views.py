from helpers.access import AccessEdit, IsSuperUser
from .models import Post
from .serializers import PostWriteSerializer, PostReadSerializer
from helpers.views import ReadWriteModelViewSet


class PostViewSet(ReadWriteModelViewSet):

    queryset = Post.objects.all()
    serializer_class_in = PostWriteSerializer
    serializer_class_out = PostReadSerializer
    serializer_class = serializer_class_out
    permission_classes = [IsSuperUser | AccessEdit]

