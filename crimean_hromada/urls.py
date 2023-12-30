"""
URL configuration for crimean_hromada project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf.urls.static import static
from crimean_hromada import settings
from app import views
from django.urls import path, re_path, include
from django.conf.urls.i18n import i18n_patterns

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('map', views.map, name='map'),
    path('search', views.search, name='search'),
    path('publish', views.publish, name='publish'),
    path('wiki', views.wiki, name='wiki'),
    path('self-government', views.self_government, name='self-government'),
    path('publish', views.publish, name='publish'),
    path('publish/<uuid:idea_id>/', views.publish_with_idea, name='publish_with_idea'),
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('register', views.custom_register, name='register'),
    path('account/<uuid:user_id>/', views.account, name='account'),
    path('account/<uuid:user_id>/edit/', views.edit_profile, name='edit_profile'),
    path('project/<uuid:project_id>/', views.project, name='project'),
    path('project/<uuid:project_id>/edit/', views.edit_project, name='edit_project'),
    path('project/<uuid:project_id>/delete/', views.delete_project, name='delete_project'),
    path('project/<uuid:project_id>/news/<uuid:news_id>/', views.news_detail, name='news_detail'),
    path('project/<uuid:project_id>/news/<uuid:news_id>/edit/', views.edit_news, name='edit_news'),
    path('project/<uuid:project_id>/news/<uuid:news_id>/delete/', views.delete_news, name='delete_news'),
    path('project/<uuid:project_id>/add_news/', views.add_news, name='add_news'),
    path('project/<uuid:project_id>/add_resource/', views.add_resource_to_project, name='add_resource_to_project'),
    path('idea/<uuid:idea_id>/', views.idea_detail, name='idea_detail'),
    path('idea/<uuid:idea_id>/edit/', views.idea_edit, name='idea_edit'),
    path('idea/<uuid:idea_id>/delete/', views.idea_delete, name='idea_delete'),
    path('toggle_favorite/<uuid:project_id>/', views.toggle_favorite, name='toggle_favorite'),
    path('save_idea/<uuid:idea_id>/', views.save_idea, name='save_idea'),


]

