from django.contrib import admin

from .models import SceneUpload, SceneUploadAnonymous

admin.site.register(SceneUpload)
admin.site.register(SceneUploadAnonymous)
