from django.db import models
from django.contrib.auth.models import User
from webapp.models import Work, Cut

# Create your models here.
class PSDFile(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    datafile = models.FileField()
    w = models.IntegerField()
    h = models.IntegerField()

    def __str__(self):
        return self.datafile.name

class Cluster(models.Model):
    work = models.ForeignKey(Work,
                             models.SET_NULL,
                             null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Instance(models.Model):
    index = models.PositiveIntegerField(primary_key=True)
    cut = models.ForeignKey(Cut,
                            on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster,
                                on_delete=models.CASCADE)

    def __str__(self):
        return self.index


class KeyPoint(models.Model):
    KEYPOINT = (
        ('N','nose'),
        )
    index = models.PositiveIntegerField(primary_key=True)
    # nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder,
    # left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee,
    # right_knee, left_ankle, right_ankle
    # So, 0 to 16, zero: nose,  odd: left, even: right
    partnum = models.PositiveSmallIntegerField()
    x = models.IntegerField()
    y = models.IntegerField()
    # 0: null, 1: obscure, 2: see
    visible = models.NullBooleanField()

    def __str__(self):
        return self.index
