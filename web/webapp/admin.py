from django.contrib import admin
from .models import Work, Episode, Cut, PSDFile, Cluster, Instance, KeyPoint

admin.site.register(Work)
admin.site.register(Episode)
admin.site.register(Cut)
admin.site.register(PSDFile)
admin.site.register(Cluster)
admin.site.register(Instance)
admin.site.register(KeyPoint)
