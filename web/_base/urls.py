from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.shortcuts import redirect, reverse
from django.views.generic.base import RedirectView
from rest_framework import routers

from webapp import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^api/', RedirectView.as_view(url='/', permanent=True)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^psdfile/$', views.psdfile_handler),
    url(r'^keypoints/$', views.keypoint_finder),
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
