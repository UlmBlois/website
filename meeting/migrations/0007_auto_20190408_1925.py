# Generated by Django 2.1.7 on 2019-04-08 17:25

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0006_auto_20190405_1854'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ulm',
            name='radio_id',
            field=models.CharField(max_length=6, validators=[django.core.validators.RegexValidator('^[0-9a-zA-Z]{1,2}-[0-9a-zA-Z]{3,4}$', 'Invalid format, ex: F-JAZ3 or OO-F3S')]),
        ),
    ]