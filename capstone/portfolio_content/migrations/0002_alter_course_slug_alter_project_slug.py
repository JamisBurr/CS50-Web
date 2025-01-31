# Generated by Django 5.1.3 on 2024-12-04 19:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_content', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
