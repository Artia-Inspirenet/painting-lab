from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Work(models.Model):
    '''A model for each story'''
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    author = models.ForeignKey(Author,
                               on_delete=models.SET_NULL,
                               null=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Episode(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    author = models.ForeignKey(Author,
                               on_delete=models.SET_NULL,
                               null=True)
    work = models.ForeignKey(Work,
                             on_delete=models.SET_NULL,
                             null=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class PSDFile(models.Model):
    uploaded = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE)
    author = models.ForeignKey(Author,
                               on_delete=models.CASCADE,
                               null=True)
    work = models.ForeignKey(Work,
                             on_delete=models.CASCADE,
                             null=True)
    episode = models.ForeignKey(Episode,
                                on_delete=models.CASCADE,
                                null=True)
    psdfile = models.FileField()
    w = models.IntegerField(null=True)
    h = models.IntegerField(null=True)

    def __str__(self):
        return self.psdfile.name


class Cut(models.Model):
    episode = models.ForeignKey(Episode,
                                on_delete=models.CASCADE,
                                null=True)
    # This field is for order
    pre_cut = models.OneToOneField('self',
                                   related_name='previous_cut',
                                   null=True,
                                   on_delete=None)
    img_file = models.FileField()
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()

    def __str__(self):
        return self.img_file.name.split('/')[-1]


class Cluster(models.Model):
    work = models.ForeignKey(Work,
                             models.SET_NULL,
                             null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Instance(models.Model):
    KEYPOINT = (
        ('N','nose'),
        )
    index = models.PositiveIntegerField(primary_key=True)
    cut = models.ForeignKey(Cut,
                            on_delete=models.CASCADE)
    cluster = models.ForeignKey(Cluster,
                                on_delete=models.CASCADE)
    # nose, left_eye, right_eye, left_ear, right_ear, left_shoulder, right_shoulder,
    # left_elbow, right_elbow, left_wrist, right_wrist, left_hip, right_hip, left_knee,
    # right_knee, left_ankle, right_ankle
    # So, 0 to 16, zero: nose,  odd: left, even: right
    partnum = models.PositiveSmallIntegerField()

    def __str__(self):
        return self.index


class KeyPoint(models.Model):
    x = models.IntegerField()
    y = models.IntegerField()
    # 0: null, 1: obscure, 2: see
    visible = models.NullBooleanField()

    def __str__(self):
        return self.index
