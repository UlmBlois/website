# Generated by Django 2.1.7 on 2019-03-25 17:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='origin_field',
            field=models.CharField(blank=True, help_text='Airfield OACI code', max_length=4),
        ),
    ]