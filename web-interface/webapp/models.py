from django.db import models
from django.contrib.auth.models import User


class Work(models.Model):
    '''A model for each story'''
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    title = models.CharField(max_length=255)
    detail = models.TextField(blank=True)

    def __str__(self):
        return self.title


class Episode(models.Model):
    user = models.ForeignKey(User,
                             on_delete=models.SET_NULL,
                             null=True)
    work = models.ForeignKey(Work,
                             on_delete=models.SET_NULL,
                             null=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title


class Cut(models.Model):
    index = models.PositiveIntegerField(primary_key=True)
    episode = models.ForeignKey(Episode,
                                on_delete=models.CASCADE)
    # This field is for order
    pre_cut = models.OneToOneField('self',
                                   related_name='previous_cut',
                                   null=True,
                                   on_delete=None)
    x = models.IntegerField()
    y = models.IntegerField()
    w = models.IntegerField()
    h = models.IntegerField()

    def __str__(self):
        return self.index
