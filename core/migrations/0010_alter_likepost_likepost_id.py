# Generated by Django 4.2.6 on 2024-06-23 04:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0009_likepost_likepost_id_alter_likepost_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='likepost',
            name='likepost_id',
            field=models.IntegerField(auto_created=True),
        ),
    ]