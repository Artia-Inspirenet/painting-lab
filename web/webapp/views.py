from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

import pytoshop
from pytoshop.user import nested_layers as nl
from pytoshop.enums import *
import numpy as np
from PIL import Image

from .models import PSDFile, Work, Episode, Author
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
                serializer.save(user=request.user,
                                datafile=psdfile,
                                author=request.data['author'],
                                work=request.data['work'],
                                episode=request.data['episode'])
        return Response({'status':'success'})
