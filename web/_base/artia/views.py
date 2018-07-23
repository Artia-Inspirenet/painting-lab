from django.shortcuts import render, redirect, reverse
from django.views.generic import base

from .forms import SceneUploadForm

class HomeView(base.TemplateView):

    template_name = 'artia/home.html'

#    def get_context_data(self, **kwargs):
#        context = super().get_context_data(**kwargs)
#        return context

def scene_upload(request):
    if request.method == 'POST':
        form = SceneUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
#            return redirect(reverse('artia:home'))
            return render(request, 'artia/scene_step_1.html')
    else:
        form = SceneUploadForm()

    context = {
        'form': form
    }

    return render(request, 'artia/scene_upload.html', context)
