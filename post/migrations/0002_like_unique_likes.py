# Generated by Django 4.2.7 on 2023-11-25 15:00

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("post", "0001_initial"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="like",
            constraint=models.UniqueConstraint(
                fields=("post_id", "created_by_id"), name="unique_likes"
            ),
        ),
    ]
