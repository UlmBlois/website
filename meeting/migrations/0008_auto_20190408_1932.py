# Generated by Django 2.1.7 on 2019-04-08 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('meeting', '0007_auto_20190408_1925'),
    ]

    operations = [
        migrations.RenameField(
            model_name='reservation',
            old_name='to_sell',
            new_name='for_sale',
        ),
    ]
