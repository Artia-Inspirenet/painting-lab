from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.decorators import api_view
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

import pytoshop
from pytoshop.user import nested_layers as nl
import io

from .models import PSDFile, Work, Episode, Author
from .serializers import PSDFileUploadSerializer, WorkSerializer, EpisodeSerializer, AuthorSerializer



def home(request):
    return render(request, 'index.html')


class PSDFileUploadViewSet(ModelViewSet):
    """
    API endpoint that allows PSD file upload to be viewed or edited.
    """
    queryset = PSDFile.objects.all()
    serializer_class = PSDFileUploadSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)


    def perform_create(self, serializer):
        psdfiles = self.request.FILES.getlist('psdfile')
        for psdfile in psdfiles:
            psd = pytoshop.read(psdfile)
            layers = nl.psd_to_nested_layers(psd)
            print(nl.pprint_layers(layers))
            serializer.save(user=self.request.user,
                            datafile=psdfile,
                            author=self.request.data['author'],
                            work=self.request.data['work'],
                            episode=self.request.data['episode'])

