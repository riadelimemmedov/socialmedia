# Generated by Django 3.2.4 on 2021-09-20 04:06

import account.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0022_comment_sekil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='sekil',
            field=models.ImageField(upload_to='users', verbose_name=account.models.Profile),
        ),
    ]