from django import forms
from .models import SceneUpload

class SceneUploadForm(forms.ModelForm):
    class Meta:
        model = SceneUpload
        fields = ('scene', 'description', )
