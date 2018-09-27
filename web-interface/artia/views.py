from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import base
from django.views.generic.list import ListView
import json
#from django.core.serializers.json import DjangoJSONEncoder as json

from .models import Scene, Cut
from .forms import SceneForm, CutForm

class HomeView(base.TemplateView):

    template_name = 'artia/home.html'


class SceneListView(ListView):

    model = Scene
    template_name = 'artia/scene_list.html'
    context_object_name = 'scene_list'
    paginate_by = 50

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Scene.objects.all()

        elif self.request.user.is_authenticated:
            return Scene.objects.filter(whose__username=self.request.user.username)

        elif self.request.user.is_anonymous:
            return Scene.objects.exclude(whose__isnull=False)


class CutListView(ListView):

    model = Cut
    template_name = 'artia/cut_list.html'
    context_object_name = 'cut_list'
    paginate_by = 50

    def get_queryset(self):

        if self.request.user.is_superuser:
            return Cut.objects.all()

        elif self.request.user.is_authenticated:
            return Cut.objects.filter(whose__username=self.request.user.username)

        elif self.request.user.is_anonymous:
            return Cut.objects.exclude(whose__isnull=False)



#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context

def scene_upload(request):
    if request.method == 'POST':

        form = SceneForm(request.POST, request.FILES)

        if form.is_valid():
            scenes = request.FILES.getlist('scene_img')
            for s in scenes:
                scene = Scene(scene_img = s)
                if request.user.is_authenticated:
                    scene.whose = request.user
                scene.save()
            return redirect('artia:scene-list')

    else:
        form = SceneForm()

    context = {
        'form': form
    }

    return render(request, 'artia/scene_upload.html', context)

def cut_upload(request):
    if request.method == 'POST':

        form = CutForm(request.POST, request.FILES)

        if form.is_valid():
            cuts = request.FILES.getlist('cut_img')
            for s in cuts:
                cut = Cut(cut_img = s)
                if request.user.is_authenticated:
                    cut.whose = request.user
                cut.save()
            return redirect('artia:cut-list')

    else:
        form = CutForm()

    context = {
        'form': form
    }

    return render(request, 'artia/cut_upload.html', context)

def cut_instance(request, id=None):

    if request.method == 'POST':
        coordinates = request.POST['coordinates']

        # DB part.

        # First, load Cut model's item based on primary key(or id, instead)
        cut = Cut.objects.get(pk=id)

        # Second, save coordinates on memory just received(not DB, yet).
        cut.coordinates = coordinates

        # Third, update DB
        cut.save()

        # Reload Cut model just saved.
        cut.refresh_from_db()

        return HttpResponse(cut.coordinates)


        #Save added coordinates to DB
    cut_img_url = Cut.objects.get(pk=id).cut_img.url
    context = { 'cut_img_url': cut_img_url,
                'pk' : id }
    return render(request, 'artia/cut_instance.html', context)
