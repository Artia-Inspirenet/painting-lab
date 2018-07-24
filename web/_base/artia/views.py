from django.shortcuts import render, redirect, reverse
from django.views.generic import base

from .models import SceneUpload, SceneUploadAnonymous
from .forms import SceneUploadForm, SceneUploadAnonymousForm

class HomeView(base.TemplateView):

    template_name = 'artia/home.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context

def scene_upload(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            form = SceneUploadForm(request.POST, request.FILES)
            if form.is_valid():
                scene = SceneUpload(scene_img = request.FILES['scene_img'])
                scene.uploaded_by = request.user
                scene.scene_img.upload_to = 'scene/%s' % request.user.username
                scene.save()
    #            return redirect(reverse('artia:home'))
                return render(request, 'artia/scene_step_1.html')
        else :
            form = SceneUploadAnonymousForm(request.POST, request.FILES)
            if form.is_valid():
                scene = SceneUploadAnonymous(scene_img = request.FILES['scene_img'])
                scene.save()
    #            return redirect(reverse('artia:home'))
                return render(request, 'artia/scene_step_1.html')
    else:
        if request.user.is_authenticated:
            form = SceneUploadForm()
        else :
            form = SceneUploadAnonymousForm()

    context = {
        'form': form
    }

    return render(request, 'artia/scene_upload.html', context)
