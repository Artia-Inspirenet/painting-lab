from django.contrib import admin

# Register your models here.
from .models import PSDFile, Cluster, Instance, KeyPoint

admin.site.register(PSDFile)
admin.site.register(Cluster)
admin.site.register(Instance)
admin.site.register(KeyPoint)
