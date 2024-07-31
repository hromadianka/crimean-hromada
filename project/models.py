from django.db import models
import uuid
from django.contrib.auth.models import User
from idea.models import Idea
from news.models import News


# Create your models here.

class Project(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=100)
    description = models.TextField()
    chat_element = models.URLField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    resources = models.ManyToManyField('Resource', related_name='projects')
    tasks = models.ManyToManyField('Task', related_name='projects')
    news = models.ManyToManyField('news.News', related_name='project')
    ideas = models.ManyToManyField(Idea, related_name='projects')
    likes = models.IntegerField(default=0)

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
    risk_level = models.CharField(max_length=20)
    activity_sphere = models.CharField(max_length=20)
    user_results = models.FileField(upload_to='task_results/', blank=True, null=True)

class Resource(models.Model):
    name = models.CharField(max_length=100)