# Generated by Django 2.1.7 on 2019-03-28 07:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0002_auto_20190325_1843'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pilot',
            name='insurance_company',
            field=models.CharField(max_length=64),
        ),
    ]