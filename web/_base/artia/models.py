from django.db import models

class SceneUpload(models.Model):
#    uploaded_by = models.ForeignKey('auth.User', related_name='uploaded_scene')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scene = models.FileField(upload_to='scene')
    description = models.CharField(max_length=255, blank=True)
