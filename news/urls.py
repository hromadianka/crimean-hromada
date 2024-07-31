from . import views
from django.urls import path, re_path, include

urlpatterns = [
    path('project/<str:project_id>/news/<uuid:news_id>/', views.news_detail, name='news_detail'),
    path('project/<str:project_id>/news/<uuid:news_id>/edit/', views.edit_news, name='edit_news'),
    path('project/<str:project_id>/news/<uuid:news_id>/delete/', views.delete_news, name='delete_news'),
    path('project/<str:project_id>/add_news/', views.add_news, name='add_news'),
]