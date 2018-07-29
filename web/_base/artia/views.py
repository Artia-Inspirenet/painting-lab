from django.shortcuts import render, redirect, reverse
from django.views.generic import base
from django.views.generic.list import ListView

from .models import SceneUpload
from .forms import SceneUploadForm

class HomeView(base.TemplateView):

    template_name = 'artia/home.html'


class SceneListView(ListView):

    model = SceneUpload
    template_name = 'artia/scene_list.html'
    context_object_name = 'scene_list'
    paginate_by = 50

    def get_queryset(self):

        if self.request.user.is_authenticated:
            return SceneUpload.objects.filter(uploaded_by__username=self.request.user.username)

        else:
            return SceneUpload.objects.exclude(uploaded_by__isnull=False)


def scene_upload(request):
    if request.method == 'POST':

        form = SceneUploadForm(request.POST, request.FILES)

        if form.is_valid():
#            scenes = SceneUpload(scene_img = request.FILES.getlist('scene_img'))
            scenes = request.FILES.getlist('scene_img')
            for s in scenes:
                scene = SceneUpload(scene_img = s)
                if request.user.is_authenticated:
                    scene.uploaded_by = request.user
                scene.save()
            return redirect('artia:scene-list')

    else:
        form = SceneUploadForm()

    context = {
        'form': form
    }

    return render(request, 'artia/scene_upload.html', context)
