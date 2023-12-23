from django.db import models
from django.contrib.auth.models import User
import uuid

# Create your models here.

class Idea(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    chat_element = models.URLField()
    created_projects = models.ManyToManyField('Project', related_name='creators')
    favorite_projects = models.ManyToManyField('Project', related_name='favorites')
    saved_ideas = models.ManyToManyField(Idea, related_name='savers')

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    chat_element = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    resources = models.ManyToManyField('Resource', related_name='projects')
    tasks = models.ManyToManyField('Task', related_name='projects')
    news = models.ManyToManyField('News', related_name='project')
    ideas = models.ManyToManyField(Idea, related_name='projects')
    likes = models.IntegerField(default=0)
    favorited_by = models.ManyToManyField(User, related_name='favorite_projects')

    def toggle_favorite(self, user):
        if self.favorited_by.filter(id=user.id).exists():
            self.favorited_by.remove(user)
            self.likes -= 1
        else:
            self.favorited_by.add(user)
            self.likes += 1
        self.save()

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    risk_level = models.CharField(max_length=20)
    activity_sphere = models.CharField(max_length=20)
    user_results = models.FileField(upload_to='task_results/', blank=True, null=True)

class Resource(models.Model):
    name = models.CharField(max_length=100)

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)