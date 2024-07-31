from . import views
from django.urls import path, re_path, include

urlpatterns = [
    path('idea/<str:idea_id>/', views.idea_detail, name='idea_detail'),
    path('idea/<str:idea_id>/publish-with-idea', views.publish_with_idea, name='publish_with_idea'),
    path('idea/<str:idea_id>/edit/', views.idea_edit, name='idea_edit'),
    path('idea/<str:idea_id>/delete/', views.idea_delete, name='idea_delete'),
    path('save_idea/<str:idea_id>/', views.save_idea, name='save_idea'),
]
