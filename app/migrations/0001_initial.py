# Generated by Django 4.2.4 on 2023-12-23 22:21

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Idea',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='News',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('content', models.TextField()),
                ('image', models.ImageField(blank=True, null=True, upload_to='news_images/')),
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
                ('favorited_by', models.ManyToManyField(related_name='favorite_projects', to=settings.AUTH_USER_MODEL)),
                ('ideas', models.ManyToManyField(related_name='projects', to='app.idea')),
                ('news', models.ManyToManyField(related_name='project', to='app.news')),
            ],
        ),
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
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.project')),
            ],
        ),
        migrations.AddField(
            model_name='project',
            name='resources',
            field=models.ManyToManyField(related_name='projects', to='app.resource'),
        ),
        migrations.AddField(
            model_name='project',
            name='tasks',
            field=models.ManyToManyField(related_name='projects', to='app.task'),
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('chat_element', models.URLField()),
                ('created_projects', models.ManyToManyField(related_name='creators', to='app.project')),
                ('favorite_projects', models.ManyToManyField(related_name='favorites', to='app.project')),
                ('saved_ideas', models.ManyToManyField(related_name='savers', to='app.idea')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
