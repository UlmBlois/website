# Generated by Django 2.2.3 on 2019-07-26 06:01

from django.db import migrations, models
import tinymce.models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0003_auto_20190726_0748'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chunk',
            name='content_en',
            field=tinymce.models.HTMLField(blank=True, verbose_name='str_Content'),
        ),
        migrations.AlterField(
            model_name='chunk',
            name='description_en',
            field=models.CharField(blank=True, help_text='str_Short_description', max_length=64, verbose_name='str_Description'),
        ),
    ]
