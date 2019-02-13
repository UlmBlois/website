# Generated by Django 2.1.4 on 2019-02-01 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20190201_0812'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='content_en',
            field=models.TextField(verbose_name='Content'),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='description_en',
            field=models.CharField(help_text='Short Description', max_length=64, verbose_name='Description'),
        ),
    ]