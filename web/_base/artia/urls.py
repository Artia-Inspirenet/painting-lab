from django.urls import path

from . import views

app_name = 'artia'
urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('scene/upload/', views.scene_upload, name='scene-upload'),
    path('scene/list/', views.SceneListView.as_view(), name='scene-list'),
    path('cut/upload/', views.cut_upload, name='cut-upload'),
    path('cut/list/', views.CutListView.as_view(), name='cut-list'),
    path('cut/instance/<int:id>/', views.cut_instance, name='cut-instance'),
#    path('scene/cut', views.scene_cut, name='scene-cut'),
]
