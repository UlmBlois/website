# Generated by Django 2.1.7 on 2019-05-03 16:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0014_auto_20190430_1955'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilot',
            name='modification_date',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='modification_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
