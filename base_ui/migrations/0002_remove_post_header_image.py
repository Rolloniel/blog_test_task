# Generated by Django 2.2.7 on 2019-11-17 19:38

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_ui', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='header_image',
        ),
    ]
