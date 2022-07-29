# Generated by Django 3.2.4 on 2021-06-23 05:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('playersmanagement', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='GameNumber',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gamenumber', models.IntegerField()),
                ('date', models.DateField()),
                ('time', models.TimeField()),
                ('category', models.CharField(choices=[('BB', 'Baseball'), ('501', '501')], max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='Participant',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('score', models.IntegerField(blank=True, null=True)),
                ('rank', models.IntegerField()),
                ('game', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gamescoring.gamenumber')),
                ('player', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='playersmanagement.player')),
            ],
        ),
    ]