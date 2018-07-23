from django.urls import path

from . import views

app_name = 'artia'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('scene', views.scene_upload, name='scene_upload'),
]
