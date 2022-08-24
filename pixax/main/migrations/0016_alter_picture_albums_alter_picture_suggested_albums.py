# Generated by Django 4.0.6 on 2022-08-24 00:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_alter_picture_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='albums',
            field=models.ManyToManyField(blank=True, null=True, related_name='pictures', to='main.album'),
        ),
        migrations.AlterField(
            model_name='picture',
            name='suggested_albums',
            field=models.ManyToManyField(blank=True, null=True, related_name='potential_pictures', to='main.album'),
        ),
    ]