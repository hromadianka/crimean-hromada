from django.contrib import admin
from users.models import Profile
from project.models import Project, Task, Resource
from idea.models import Idea
from news.models import News

# Register your models here.

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Idea)
admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(News)

