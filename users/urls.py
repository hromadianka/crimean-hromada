from . import views
from django.urls import path, re_path, include

urlpatterns = [
    path('login', views.custom_login, name='login'),
    path('logout', views.custom_logout, name='logout'),
    path('register', views.custom_register, name='register'),
    path('account/<int:user_id>/', views.account, name='account'),
    path('account/<int:user_id>/edit/', views.edit_profile, name='edit_profile'),
]