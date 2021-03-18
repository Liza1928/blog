from rest_framework import serializers
from .models import Post, Category
from users.models import User


class PostWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('author', 'title', 'text')


class PostReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('id', 'author', 'title', 'text', 'created',)


class CategoryReadSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('id', 'name',)


class CategoryWriteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name',)


class AuthorReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('name', 'email', 'image')

