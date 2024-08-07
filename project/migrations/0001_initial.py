# Generated by Django 4.2.4 on 2024-07-31 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('news', '0001_initial'),
        ('idea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('risk_level', models.CharField(max_length=20)),
                ('activity_sphere', models.CharField(max_length=20)),
                ('user_results', models.FileField(blank=True, null=True, upload_to='task_results/')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('chat_element', models.URLField()),
                ('likes', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('ideas', models.ManyToManyField(related_name='projects', to='idea.idea')),
                ('news', models.ManyToManyField(related_name='project', to='news.news')),
                ('resources', models.ManyToManyField(related_name='projects', to='project.resource')),
                ('tasks', models.ManyToManyField(related_name='projects', to='project.task')),
            ],
        ),
    ]
