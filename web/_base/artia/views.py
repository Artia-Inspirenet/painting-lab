from django.shortcuts import render, redirect, reverse
from django.views.generic import base
from django.views.generic.list import ListView

from .models import SceneUpload
from .forms import SceneUploadForm
#from .models import SceneUploadAnonymous
#from .forms import SceneUploadAnonymousForm

class HomeView(base.TemplateView):

    template_name = 'artia/home.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context

class SceneListView(ListView):

    model = SceneUpload
    template_name = 'artia/scene_list.html'
    context_object_name = 'scene_list'
    paginate_by = 50

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        #context['scene_list'] = model.objects.all()
#        return context

    def get_queryset(self):
        return SceneUpload.objects.filter(uploaded_by__username=self.request.user.username)


def scene_upload(request):
    if request.method == 'POST':

        form = SceneUploadForm(request.POST, request.FILES)

        if form.is_valid():
            scene = SceneUpload(scene_img = request.FILES['scene_img'])
            if request.user.is_authenticated:
                scene.uploaded_by = request.user
            scene.save()
            return redirect('artia:scene-list')

#        else :
#            form = SceneUploadAnonymousForm(request.POST, request.FILES)
#
#            if form.is_valid():
#                scene = SceneUploadAnonymous(scene_img = request.FILES['scene_img'])
#                scene.save()
#                return redirect('artia:scene-list')

    else:
        form = SceneUploadForm()

    context = {
        'form': form
    }

    return render(request, 'artia/scene_upload.html', context)
