from django.db import models
from django.contrib.auth.models import User

def scene_save_path(who, what):
    try :
        save_path = 'scene/{}/{}'.format(who.uploaded_by.username, what)

    except AttributeError:
        save_path = 'scene/{}/{}'.format('anonymous', what)

    return save_path

class SceneUpload(models.Model):
    uploaded_by = models.ForeignKey(User,
                                    blank = True,
                                    null = True,
                                    on_delete = models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scene_img = models.FileField(upload_to=scene_save_path)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{}'.format(self.scene_img.name.split('/')[-1])
