# Generated by Django 2.0.1 on 2018-01-19 03:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scoretable', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='zipfile',
            old_name='name',
            new_name='filename',
        ),
    ]
