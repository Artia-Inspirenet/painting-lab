from django import forms
from .models import Scene,Cut,Instance

class SceneForm(forms.ModelForm):
    scene_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Scene
        fields = ('scene_img', 'description', )

class CutForm(forms.ModelForm):
    cut_img = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple':True}))
    class Meta:
        model = Cut
        fields = ('cut_img', 'description', 'coordinates', )

