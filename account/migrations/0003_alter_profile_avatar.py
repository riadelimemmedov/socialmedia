# Generated by Django 3.2.4 on 2021-08-27 04:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_alter_profile_avatar'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='users/amk.jpg', upload_to='users'),
        ),
    ]
