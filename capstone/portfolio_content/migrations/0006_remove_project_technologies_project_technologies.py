# Generated by Django 5.1.3 on 2024-12-16 22:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_content', '0005_technology_remove_course_technologies_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='technologies',
        ),
        migrations.AddField(
            model_name='project',
            name='technologies',
            field=models.ManyToManyField(related_name='projects', to='portfolio_content.technology'),
        ),
    ]
