# Generated by Django 4.0.6 on 2022-08-10 20:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_slide_delete_slideshowslide'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Slide',
            new_name='SlideshowSlide',
        ),
    ]