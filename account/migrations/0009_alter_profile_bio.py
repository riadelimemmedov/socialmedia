# Generated by Django 3.2.4 on 2021-08-30 03:36

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0008_profile_doguldugu_il'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=ckeditor.fields.RichTextField(blank=True),
        ),
    ]
