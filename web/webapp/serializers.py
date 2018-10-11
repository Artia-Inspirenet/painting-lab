from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PSDFile, Work, Episode, Author


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('title', )


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('title', )


class PSDFileUploadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username')
    author = serializers.CharField()
    work = serializers.CharField()
    episode = serializers.CharField()
    #work = serializers.SlugRelatedField(
    #    queryset=Work.objects.all(),
    #    slug_field='id')
    #episode = serializers.SlugRelatedField(
    #    queryset=Episode.objects.all(),
    #    slug_field='id')

    class Meta:
        model = PSDFile
        fields = ('uploaded', 'user', 'datafile', 'author', 'work', 'episode')

    def create(self, validated_data):
        user_data = validated_data.pop('user')
        new_author = Author.objects.create(user=user_data,
                                           name=validated_data['author'])
        new_work = Work.objects.create(user=user_data,
                                       author=new_author,
                                       title=validated_data['work'])
        new_episode = Episode.objects.create(user=user_data,
                                             work=new_work,
                                             title=validated_data['episode'])
        psdfile = PSDFile.objects.create(user=user_data,
                                         author=new_author,
                                         work=new_work,
                                         episode=new_episode,
                                         datafile=validated_data['datafile'])

        return psdfile

    def update(self, instance, validated_data):
        pass
