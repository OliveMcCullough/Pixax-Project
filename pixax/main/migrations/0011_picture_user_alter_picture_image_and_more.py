# Generated by Django 4.0.6 on 2022-08-12 17:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0010_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='picture',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='picture',
            name='image',
            field=models.ImageField(upload_to='pictures/'),
        ),
        migrations.AlterField(
            model_name='slide',
            name='slideshow',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='slide', to='main.slideshow'),
        ),
    ]
