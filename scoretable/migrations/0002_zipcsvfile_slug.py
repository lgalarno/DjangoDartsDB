# Generated by Django 2.0.1 on 2018-01-24 05:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('scoretable', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='zipcsvfile',
            name='slug',
            field=models.SlugField(default=1, max_length=32),
            preserve_default=False,
        ),
    ]
