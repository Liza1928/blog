# Generated by Django 3.1.7 on 2021-03-18 06:34

from django.db import migrations, models
import users.models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_auto_20210317_0749'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='image',
            field=models.ImageField(blank=True, max_length=1024, null=True, upload_to=users.models.upload_to_images),
        ),
    ]
