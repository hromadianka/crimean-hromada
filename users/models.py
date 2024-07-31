from django.db import models
from django.contrib.auth.models import User
import uuid
from project.models import Project
from idea.models import Idea

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    chat_element = models.URLField()
    created_projects = models.ManyToManyField('Project', related_name='creators')
    favorite_projects = models.ManyToManyField('Project', related_name='favorites')
    saved_ideas = models.ManyToManyField(Idea, related_name='savers')