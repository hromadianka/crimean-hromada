from django.contrib import admin
from .models import Profile, Project, Idea, Task, Resource, News

# Register your models here.

admin.site.register(Profile)
admin.site.register(Project)
admin.site.register(Idea)
admin.site.register(Task)
admin.site.register(Resource)
admin.site.register(News)

