# Generated by Django 2.0.1 on 2018-01-17 21:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gamescoring', '0002_auto_20180117_2146'),
    ]

    operations = [
        migrations.AlterField(
            model_name='participant',
            name='score',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
