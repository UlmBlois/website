# Generated by Django 2.2.3 on 2019-07-11 17:03

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name_en', models.CharField(max_length=200, verbose_name='str_Topic')),
                ('topic_name_fr', models.CharField(max_length=200, verbose_name='str_Topic')),
                ('number', models.PositiveIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'str_Topic',
                'verbose_name_plural': 'str_Topics',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_en', models.CharField(max_length=200, verbose_name='str_question')),
                ('question_fr', models.CharField(max_length=200, verbose_name='str_question')),
                ('answer_en', tinymce.models.HTMLField(verbose_name='str_answer')),
                ('answer_fr', tinymce.models.HTMLField(verbose_name='str_answer')),
                ('number', models.PositiveIntegerField()),
                ('topic', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='faq.Topic')),
            ],
            options={
                'verbose_name': 'str_Question',
                'verbose_name_plural': 'str_Questions',
                'ordering': ['number'],
                'unique_together': {('number', 'topic')},
            },
        ),
    ]
