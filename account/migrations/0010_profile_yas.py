# Generated by Django 3.2.4 on 2021-08-31 03:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0009_alter_profile_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='yas',
            field=models.CharField(default=1, max_length=255),
            preserve_default=False,
        ),
    ]
