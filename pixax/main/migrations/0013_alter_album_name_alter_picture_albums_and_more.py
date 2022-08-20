# Generated by Django 4.0.6 on 2022-08-19 13:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0012_alter_slide_slideshow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='album',
            name='name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='picture',
            name='albums',
            field=models.ManyToManyField(blank=True, related_name='pictures', to='main.album'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='suggested_albums',
            field=models.ManyToManyField(blank=True, related_name='potential_pictures', to='main.album'),
        ),
    ]
