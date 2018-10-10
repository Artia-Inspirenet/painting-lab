from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PSDFile, Work, Episode


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('title', 'detail')


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('title',)


class PSDFileUploadSerializer(serializers.Serializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    work_title = serializers.CharField()
    work_detail = serializers.CharField()
    episode = serializers.CharField()
    #work = serializers.SlugRelatedField(
    #    queryset=Work.objects.all(),
    #    slug_field='id')
    #episode = serializers.SlugRelatedField(
    #    queryset=Episode.objects.all(),
    #    slug_field='id')

    class Meta:
        model = PSDFile
        fields = ('uploaded', 'user', 'datafile', 'work_title', 'work_detail', 'episode')

    def create(self, validated_data):
        validated_data.pop('work')
        user_data = validated_data.pop('user')
        work_title = validated_data.pop('work_title')
        work_detail = validated_data.pop('work_detail')
        episode_data = validated_data.pop('episode')

        new_work = Work.objects.create(user=user_data,
                                       title=work_title,
                                       detail=work_detail)
        new_episode = Episode.objects.create(user=user_data,
                                             work=new_work,
                                             title=episode_data)
        psdfile = PSDFile.objects.create(user=user_data,
                                         work=new_work,
                                         episode=new_episode,
                                         **validated_data)

        return psdfile

    def update(self, instance, validated_data):
        pass
