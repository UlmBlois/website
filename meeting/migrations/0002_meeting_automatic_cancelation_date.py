# Generated by Django 2.2.3 on 2019-07-14 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='automatic_cancelation_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]
