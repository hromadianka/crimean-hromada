from . import views
from django.urls import path, re_path, include

urlpatterns = [
    path('wiki', views.wiki, name='wiki'),
]