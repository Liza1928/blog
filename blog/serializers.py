from rest_framework import serializers
from .models import Post


class PostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'text')
        model = Post


class PostReadSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'author', 'title', 'text', 'created',)
        model = Post
