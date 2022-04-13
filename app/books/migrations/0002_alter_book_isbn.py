# Generated by Django 4.0.4 on 2022-04-12 21:06

import books.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='ISBN',
            field=models.CharField(max_length=13, validators=[books.validators.validate_isbn]),
        ),
    ]
