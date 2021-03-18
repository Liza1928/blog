from django.db import models

from helpers.models import BaseModel


def upload_to_images(instance, filename):
    return f'blog_images/{instance.id}/{filename}'


class Category(BaseModel):

    name = models.CharField('Тема материала', max_length=64, unique=True)

    def __str__(self):
        return self.name


class Post(BaseModel):

    title = models.CharField('Заголовок поста', max_length=256, db_index=True)
    image = models.ImageField(
        'Изображение поста',
        upload_to=upload_to_images,
        max_length=1024,
        null=True,
        blank=True
    )
    text = models.TextField('Текст поста', null=True, blank=True)
    categories = models.ManyToManyField(Category)
    author = models.ForeignKey("users.User", on_delete=models.PROTECT)

    def __str__(self):
        return self.title



