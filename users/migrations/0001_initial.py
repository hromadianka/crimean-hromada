# Generated by Django 4.2.4 on 2024-07-31 05:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('project', '0001_initial'),
        ('idea', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('chat_element', models.URLField()),
                ('created_projects', models.ManyToManyField(related_name='creators', to='project.project')),
                ('favorite_projects', models.ManyToManyField(related_name='favorites', to='project.project')),
                ('saved_ideas', models.ManyToManyField(related_name='savers', to='idea.idea')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
