# Generated by Django 3.2.9 on 2023-08-06 20:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'ordering': ['-updated_at']},
        ),
    ]
