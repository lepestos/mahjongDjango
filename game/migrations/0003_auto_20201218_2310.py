# Generated by Django 3.1.4 on 2020-12-18 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('game', '0002_auto_20201218_2147'),
    ]

    operations = [
        migrations.AddField(
            model_name='player',
            name='multiplicator',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='player',
            name='unmultiplied_round_score',
            field=models.IntegerField(default=0),
        ),
    ]
