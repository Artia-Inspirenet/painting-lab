from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.core.files import File
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from .module import module1 as m1
import os

from .models import PSDFile, Work, Episode, Author, Cut
from .serializers import PSDFileUploadSerializer, WorkSerializer, EpisodeSerializer, AuthorSerializer


@api_view(['GET', 'POST'])
def psdfile_handler(request):

    if request.method == 'GET':
        # Author, Work, Episode Dropdown menu
        # Not working yet
        psdfile_list = PSDFile.objects.all()
        serializer = PSDFileUploadSerializer(psdfile_list, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        psdfiles = request.FILES.getlist('psdfile')
        for psdfile in psdfiles:
            serializer = PSDFileUploadSerializer(data=request.data)
            if serializer.is_valid() :
                
                file = serializer.save(user=request.user,
                                        datafile=psdfile,
                                        author=request.data['author'],
                                        work=request.data['work'],
                                        episode=request.data['episode'])

                psd_path = file.psdfile.name
                input_path = psd_path.split('/')[0]
                psd_name = psd_path.split('/')[1]
                file_path = os.path.join(settings.MEDIA_ROOT, input_path)
                cut_info = m1.run(file_path, psd_name)

                for cut in cut_info:
                    Cut(episode = file.episode,
                        img_file = file_path + '/' + cut['name'],
                        x = cut['x'],
                        y = cut['y']).save()


        return Response({'status':'success'})

# Just for example, this view function makes cut again and agian when request income.
@api_view(['GET', 'POST'])
def keypoint_finder(request):
    if request.method == 'GET':

        with open(settings.MEDIA_ROOT+'/sample/humanlogo.png', 'rb') as fd:
            init = { 'img_file':File(fd),
                     'x':0,
                     'y':0,
                     'w':300,
                     'h':335 }

            cutimg = Cut.objects.create(**init)

        cut_url = os.path.join(settings.MEDIA_URL, cutimg.img_file.name[len(settings.MEDIA_ROOT)+1:])
        keypoints = [{ 'x': x*random.random(), 'y': x*random.random() } for x  in range(100,900,10)]
        keypoints.append({ 'x': 145,
                           'y': 245 })
        data = dict({ 'cutimg_url': cut_url,
                      'keypoints': keypoints })
        return Response(data=data)