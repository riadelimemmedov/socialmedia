# Generated by Django 3.2.4 on 2021-08-31 04:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('article', '0002_auto_20210831_0851'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='category',
            field=models.ForeignKey(default=2, on_delete=django.db.models.deletion.CASCADE, related_name='kategoriyalarimiz', to='article.category'),
        ),
    ]
