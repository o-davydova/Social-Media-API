# Generated by Django 4.2.7 on 2023-11-22 18:16

from django.db import migrations, models
import post.models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0003_comment"),
    ]

    operations = [
        migrations.AlterField(
            model_name="post",
            name="image",
            field=models.ImageField(
                blank=True, null=True, upload_to=post.models.get_image_file_path
            ),
        ),
    ]
