from django.db import models

class SceneUpload(models.Model):
    scene = models.FileField(upload_to='scene')
    description = models.CharField(max_length=255, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
