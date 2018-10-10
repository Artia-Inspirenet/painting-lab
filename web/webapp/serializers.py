from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PSDFile, Work, Episode


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ('url', 'username', 'email', 'groups')
# 
# 
# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Group
#         fields = ('url', 'name')


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('title', 'detail')


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('title')


class PSDFileUploadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    work = WorkSerializer()
    episode = EpisodeSerializer()
    #work = serializers.SlugRelatedField(
    #    queryset=Work.objects.all(),
    #    slug_field='id')
    #episode = serializers.SlugRelatedField(
    #    queryset=Episode.objects.all(),
    #    slug_field='id')

    class Meta:
        model = PSDFile
        fields = ('uploaded', 'user', 'datafile', 'work', 'episode')

    def create(self, validated_data):
        user_data = validated_data['user']
        work_data = validated_data['work']
        episode_data = validated_data['episode']

        new_work = Work.objects.create(user=user_data,
                                       **work_data)
        new_episode = Episode.objects.create(user=user_data,
                                             work=new_work,
                                             **episode_data)
        psdfile = PSDFile.objects.create(**validated_data)

        return psdfile

    def update(self, instance, validated_data):
        pass
