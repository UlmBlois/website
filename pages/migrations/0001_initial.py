# Generated by Django 2.1.7 on 2019-03-20 18:49

from django.db import migrations, models
import django.db.models.deletion
import tinymce.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Chunk',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('key', models.CharField(help_text='A unique id for this chunk', max_length=255, unique=True, verbose_name='Key')),
                ('content_en', tinymce.models.HTMLField(verbose_name='Content')),
                ('content_fr', tinymce.models.HTMLField(blank=True, verbose_name='Content')),
                ('description_en', models.CharField(help_text='Short Description', max_length=64, verbose_name='Description')),
                ('description_fr', models.CharField(blank=True, help_text='Short Description', max_length=64, verbose_name='Description')),
            ],
            options={
                'verbose_name': 'chunk',
                'verbose_name_plural': 'chunks',
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_en', models.CharField(max_length=200, verbose_name='question')),
                ('question_fr', models.CharField(max_length=200, verbose_name='question')),
                ('answer_en', models.TextField(verbose_name='answer')),
                ('answer_fr', models.TextField(verbose_name='answer')),
                ('number', models.PositiveIntegerField()),
            ],
            options={
                'verbose_name': 'Question',
                'verbose_name_plural': 'Questions',
                'ordering': ['number'],
            },
        ),
        migrations.CreateModel(
            name='Topic',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('topic_name_en', models.CharField(max_length=200, verbose_name='topic')),
                ('topic_name_fr', models.CharField(max_length=200, verbose_name='topic')),
                ('number', models.PositiveIntegerField(unique=True)),
            ],
            options={
                'verbose_name': 'Topic',
                'verbose_name_plural': 'Topics',
                'ordering': ['number'],
            },
        ),
        migrations.AddField(
            model_name='question',
            name='topic',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='question', to='pages.Topic'),
        ),
        migrations.AlterUniqueTogether(
            name='question',
            unique_together={('number', 'topic')},
        ),
    ]
