from django.db import models
from django.contrib.auth.models import User

def scene_save_path(who, what):
    try :
        save_path = 'scene/{}/{}'.format(who.whose.username, what)

    except AttributeError:
        save_path = 'scene/{}/{}'.format('anonymous', what)

    return save_path


def cut_save_path(who, what):
    try :
        save_path = 'cut/{}/{}'.format(who.whose.username, what)

    except AttributeError:
        save_path = 'cut/{}/{}'.format('anonymous', what)

    return save_path


class Scene(models.Model):
    whose = models.ForeignKey(User,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    scene_img = models.FileField(upload_to=scene_save_path)
    description = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return '{}'.format(self.scene_img.name.split('/')[-1])


class Cut(models.Model):
    whose = models.ForeignKey(User,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE)
    scene = models.ForeignKey(Scene,
                              blank=True,
                              null=True,
                              on_delete=models.CASCADE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    cut_img = models.FileField(upload_to=cut_save_path)
    description = models.CharField(max_length=255,
                                   blank=True)
    coordinates = models.TextField(null=True,
                                   blank=True)


class Instance(models.Model):
    whose = models.ForeignKey(User,
                              blank=True,
                              null=True,
                              on_delete = models.CASCADE)
    cut = models.ForeignKey(Cut,
                            blank=True,
                            null=True,
                            on_delete=models.CASCADE)
    coordinates = models.TextField(null=True,
                                   blank=True)
    tags = models.CharField(max_length=255)


