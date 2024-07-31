from django.db import models
import uuid

# Create your models here.

class News(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)