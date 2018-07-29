from django import forms
from .models import SceneUpload

class SceneUploadForm(forms.ModelForm):
    scene_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = SceneUpload
        fields = ('scene_img', 'description', )

