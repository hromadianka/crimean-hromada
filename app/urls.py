from . import views
from django.urls import path, re_path, include

urlpatterns = [
    path('map', views.map, name='map'),
    path('publish', views.publish, name='publish'),
    path('self-government', views.self_government, name='self-government'),
    path('publish', views.publish, name='publish'),
    path('publish/<int:idea_id>/', views.publish_with_idea, name='publish_with_idea'),
]
