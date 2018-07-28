from django.urls import path

from . import views

app_name = 'artia'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('scene/upload', views.scene_upload, name='scene-upload'),
    path('scene/list', views.SceneListView.as_view(), name='scene-list'),
]
