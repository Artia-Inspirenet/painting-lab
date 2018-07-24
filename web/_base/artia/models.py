from django.db import models
from django.contrib.auth.models import User

class SceneUpload(models.Model):
    uploaded_by = models.ForeignKey(User, on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scene_img = models.FileField(upload_to='scene')
    description = models.CharField(max_length=255, blank=True)
