# Generated by Django 4.0.4 on 2022-04-13 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_alter_book_isbn'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='pages_count',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]