# Generated by Django 4.2.6 on 2024-06-23 04:42

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_rename_user_likepost_owner_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True),
        ),
    ]