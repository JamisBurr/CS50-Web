# Generated by Django 5.1.3 on 2024-12-07 04:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portfolio_content', '0003_course_certificate_alter_course_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='course',
            name='technologies',
            field=models.CharField(blank=True, default='', max_length=200, null=True),
        ),
    ]
