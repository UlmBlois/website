# Generated by Django 2.1.7 on 2019-04-08 17:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0008_auto_20190408_1932'),
    ]

    operations = [
        migrations.AddField(
            model_name='meeting',
            name='confirmation_reminder_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]