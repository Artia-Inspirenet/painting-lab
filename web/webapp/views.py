from django.shortcuts import render
from django.contrib.auth.models import User, Group
from rest_framework.viewsets import ModelViewSet
from rest_framework.parsers import FormParser, MultiPartParser

from .models import PSDFile
from .serializers import UserSerializer, GroupSerializer, PSDFileUploadSerializer


def home(request):
    return render(request, 'webapp/home.html')


class UserViewSet(ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class PSDFileUploadViewSet(ModelViewSet):
    """
    API endpoint that allows PSD file upload to be viewed or edited.
    """
    queryset = PSDFile.objects.all()
    serializer_class = PSDFileUploadSerializer
    parser_classes = (MultiPartParser, FormParser)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user,
                        datafile=self.request.data.get('datafile'))
