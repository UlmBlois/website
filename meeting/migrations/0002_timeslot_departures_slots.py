# Generated by Django 2.2.9 on 2020-04-19 11:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='timeslot',
            name='departures_slots',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]