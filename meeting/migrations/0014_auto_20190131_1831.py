# Generated by Django 2.1.4 on 2019-01-31 17:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0013_auto_20190131_1830'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ulm',
            name='imatriculation',
            field=models.CharField(max_length=6),
        ),
        migrations.AlterField(
            model_name='ulm',
            name='radio_id',
            field=models.CharField(max_length=6),
        ),
    ]