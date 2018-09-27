from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PSDFile


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class PSDFileUploadSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PSDFile
        fields = ('uploaded', 'user', 'datafile', 'w', 'h')

    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='id'
    )
