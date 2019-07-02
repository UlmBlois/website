# Generated by Django 2.2.2 on 2019-07-01 16:52

from django.db import migrations, models
import django_countries.fields


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0027_auto_20190701_1026'),
    ]

    operations = [
        migrations.AddField(
            model_name='pilot',
            name='city',
            field=models.CharField(default='', max_length=64),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pilot',
            name='city_code',
            field=models.CharField(default='', max_length=32),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pilot',
            name='country',
            field=django_countries.fields.CountryField(default='FR', max_length=2),
        ),
        migrations.AddField(
            model_name='pilot',
            name='mail_complement',
            field=models.CharField(default='', help_text='str_mail_complement', max_length=128),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='pilot',
            name='street_name',
            field=models.CharField(default='', help_text='str_street_name', max_length=128),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='reservation',
            name='origin_field',
            field=models.CharField(blank=True, help_text='str_Airfield_OACI_code', max_length=32),
        ),
        migrations.AlterField(
            model_name='ulm',
            name='imatriculation_country',
            field=django_countries.fields.CountryField(default='FR', max_length=2),
        ),
    ]