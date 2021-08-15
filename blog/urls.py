from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .serializers import CategoryWriteSerializer, CategoryReadSerializer
from .views import PostViewSet, CategoryViewSet, AuthorViewSet


router = DefaultRouter()
router.register(r'posts', PostViewSet, basename='Post')
router.register(r'categories', CategoryViewSet, basename='Category')
router.register(r'authors', AuthorViewSet, basename='Author')

urlpatterns = [
    path('', include(router.urls)),
]

