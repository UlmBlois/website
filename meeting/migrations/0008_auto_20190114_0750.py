# Generated by Django 2.1.4 on 2019-01-14 06:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0007_meeting_fuel_aviable'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='arrival',
            field=models.DateTimeField(default=None, null=True),
        ),
    ]