from . import views
from django.urls import path, re_path, include

urlpatterns = [
    path('project/<str:project_id>/', views.project, name='project'),
    path('project/<str:project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<str:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<str:project_id>/add_resource/', views.add_resource_to_project, name='add_resource_to_project'),
    path('project/<str:project_id>/add_task/', views.add_task_to_project, name='add_task_to_project'),
    path('save_project/<str:project_id>/', views.save_project, name='save_project'),
    path('edit_resource', views.edit_resource, name='edit_resource'),
    path('delete_resource', views.delete_resource, name='delete_resource'),
    path('edit_task', views.edit_task, name='edit_task'),
    path('delete_task', views.delete_task, name='delete_task'),
]