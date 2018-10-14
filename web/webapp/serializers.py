from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import PSDFile, Work, Episode, Author


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ('name', )


class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ('title', )


class EpisodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Episode
        fields = ('title', )


class PSDFileUploadSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(read_only=True,
                                        slug_field='username')
    author = serializers.CharField()
    work = serializers.CharField()
    episode = serializers.CharField()

    class Meta:
        model = PSDFile
        fields = ('user', 'psdfile', 'author', 'work', 'episode')

    def create(self, validated_data):
        new_author = Author.objects.create(user=validated_data['user'],
                                           name=validated_data['author'])
        new_work = Work.objects.create(user=validated_data['user'],
                                       author=new_author,
                                       title=validated_data['work'])
        new_episode = Episode.objects.create(user=validated_data['user'],
                                             work=new_work,
                                             title=validated_data['episode'])
        psdfile = PSDFile.objects.create(user=validated_data['user'],
                                         author=new_author,
                                         work=new_work,
                                         episode=new_episode,
                                         psdfile=validated_data['psdfile'])

        return psdfile

    def update(self, instance, validated_data):
        pass
