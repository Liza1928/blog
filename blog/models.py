from django.db import models
from django.contrib.auth import get_user_model

from helpers.models import BaseModel


User = get_user_model()


def upload_to_images(instance, filename):
    return f'blog_images/{instance.id}/{filename}'


class Author(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField()

    def __str__(self):
        return self.user.username


class Category(BaseModel):

    name = models.CharField('Тема материала', max_length=64)

    def __str__(self):
        return self.name


class Post(BaseModel):

    title = models.CharField(
        'Заголовок поста', max_length=256, db_index=True, unique=True)
    image = models.ImageField(
        'Изображение поста',
        upload_to=upload_to_images,
        max_length=1024,
        null=True,
        blank=True
    )
    text = models.TextField('Текст поста', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


