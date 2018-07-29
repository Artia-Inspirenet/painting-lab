from django.shortcuts import render, redirect, reverse, HttpResponse
from django.views.generic import base
from django.views.generic.list import ListView

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

        if self.request.user.is_authenticated:
            return Scene.objects.filter(whose__username=self.request.user.username)

        else:
            return Scene.objects.exclude(whose__isnull=False)

class CutListView(ListView):

    model = Cut
    template_name = 'artia/cut_list.html'
    context_object_name = 'cut_list'
    paginate_by = 50

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return Cut.objects.filter(whose__username=self.request.user.username)

        else:
            return Cut.objects.exclude(whose__isnull=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
#        for cut in context['cut_list']:
#            cut.cut_img.url = '/cut/instance' + cut.cut_img.url
        return context

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
#def scene_cut(request):
#
#    if request.method == 'POST':
#        # If request methed is POST, this occurs only when user try to change
#        # each frame's size.
#
#        pass
#
#    # If request method is GET, just like normal access,
#    # then web page showing image how it would be cut.
#    # This request is only occured when user access through scene list page.
#    context = {'scene':
#    return render(request, 'artia/scene_cut.html', context)

def cut_instance(request, id=None):

    if request.method == 'POST':
        coordinates = request.POST['coordinates']
        print(coordinates)
        for coordinate in coordinates:
            print(coordinate)

        return HttpResponse("<div>Seccess</div>")


        #Save added coordinates to DB
    cut_img_url = Cut.objects.get(pk=id).cut_img.url
    context = { 'cut_img_url': cut_img_url,
                'pk' : id }
    return render(request, 'artia/cut_instance.html', context)
