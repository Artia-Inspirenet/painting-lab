from django.db import models
from django.contrib.auth.models import User

# Parameter's name, like 'instance', 'filename' is defined @ Django Document 2.0.
# Do not rename these.
def scene_save_path(instance, filename):
    try :
        save_path = 'scene/{}/{}'.format(instance.uploaded_by.username, filename)

    except AttributeError:
        save_path = 'scene/{}/{}'.format('anonymous', filename)

    return save_path

class SceneUploadAnonymous(models.Model):
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scene_img = models.FileField(upload_to=scene_save_path )
    description = models.CharField(max_length=255, blank=True)

class SceneUpload(SceneUploadAnonymous):
    uploaded_by = models.ForeignKey(User, on_delete = models.CASCADE)

