# Generated by Django 4.0.6 on 2022-08-23 20:38

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_picture_date_uploaded'),
    ]

    operations = [
        migrations.AlterField(
            model_name='picture',
            name='rating',
            field=models.FloatField(default=None, null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(100)]),
        ),
    ]
