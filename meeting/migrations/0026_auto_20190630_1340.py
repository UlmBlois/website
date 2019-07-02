# Generated by Django 2.2.2 on 2019-06-30 11:40

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0025_remove_reservation_origin_city_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='pilot',
            options={'permissions': (('reservation_validation', 'str_Reservation_Validation_Permission'),)},
        ),
        migrations.AlterField(
            model_name='meeting',
            name='name',
            field=models.CharField(max_length=128),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='fuel_reservation',
            field=models.PositiveIntegerField(default=0, validators=[django.core.validators.MaxValueValidator(100)]),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='origin_field',
            field=models.CharField(blank=True, help_text='str_Airfield_OACI_code', max_length=4),
        ),
        migrations.AlterField(
            model_name='ulm',
            name='type',
            field=models.CharField(choices=[('PA', 'str_Powered_Paraglider'), ('PE', 'str_Flex_Wing'), ('MU', 'str_Fixed_Wings'), ('AU', 'str_Rotor_Wings'), ('HE', 'str_Helicopters'), ('AE', 'str_Balloons_and_Airships')], max_length=2),
        ),
    ]