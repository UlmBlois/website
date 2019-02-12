# Generated by Django 2.1.4 on 2019-02-08 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0005_auto_20190208_1947'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='answer_text_en',
            new_name='answer_en',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='answer_text_fr',
            new_name='answer_fr',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text_en',
            new_name='question_en',
        ),
        migrations.RenameField(
            model_name='question',
            old_name='text_fr',
            new_name='question_fr',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='text_en',
            new_name='topic_name_en',
        ),
        migrations.RenameField(
            model_name='topic',
            old_name='text_fr',
            new_name='topic_name_fr',
        ),
    ]
