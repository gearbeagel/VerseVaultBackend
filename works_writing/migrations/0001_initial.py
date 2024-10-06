# Generated by Django 5.1 on 2024-10-06 20:12

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('canonical', models.BooleanField(default=False)),
                ('tag_type', models.CharField(max_length=100)),
            ],
            options={
                'indexes': [models.Index(fields=['name'], name='works_writi_name_dcdc1a_idx'), models.Index(fields=['canonical'], name='works_writi_canonic_54b1c0_idx')],
            },
        ),
        migrations.CreateModel(
            name='Work',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('language', models.CharField(choices=[('en', 'English'), ('fr', 'French'), ('es', 'Spanish'), ('de', 'German'), ('uk', 'Ukrainian')], default='en', help_text='Language code', max_length=50)),
                ('summary', models.TextField(blank=True, null=True)),
                ('word_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('posted', models.BooleanField(default=False)),
                ('author', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('tags', models.ManyToManyField(blank=True, to='works_writing.tag')),
            ],
        ),
        migrations.CreateModel(
            name='Chapter',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, max_length=255, null=True)),
                ('content', models.TextField(null=True)),
                ('position', models.IntegerField(default=1)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('word_count', models.IntegerField(blank=True, editable=False, null=True)),
                ('work', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chapters', to='works_writing.work')),
            ],
        ),
        migrations.AddIndex(
            model_name='work',
            index=models.Index(fields=['language'], name='works_writi_languag_9bc989_idx'),
        ),
        migrations.AddIndex(
            model_name='work',
            index=models.Index(fields=['posted'], name='works_writi_posted_1526fd_idx'),
        ),
        migrations.AddIndex(
            model_name='chapter',
            index=models.Index(fields=['work'], name='works_writi_work_id_7de656_idx'),
        ),
    ]
