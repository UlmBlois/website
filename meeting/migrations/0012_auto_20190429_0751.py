# Generated by Django 2.1.7 on 2019-04-29 05:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0011_auto_20190422_1500'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='time_slot',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='arrivals', to='meeting.TimeSlot'),
        ),
    ]