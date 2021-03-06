# Generated by Django 4.0.4 on 2022-04-12 10:43

import books.validators
import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=90)),
                ('author', models.CharField(max_length=90)),
                ('published_date', models.DateField()),
                ('ISBN', models.IntegerField(validators=[books.validators.validate_isbn])),
                ('pages_count', models.IntegerField()),
                ('cover_link', models.URLField(blank=True, max_length=255, validators=[django.core.validators.URLValidator])),
                ('language', models.CharField(max_length=90)),
            ],
        ),
    ]
