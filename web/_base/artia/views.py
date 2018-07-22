from django.shortcuts import render
from django.views.generic import base

class HomeView(base.TemplateView):

    template_name = 'artia/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

