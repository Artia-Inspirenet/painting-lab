from django import forms
from .models import SceneUpload
#from .models import SceneUploadAnonymous

class SceneUploadForm(forms.ModelForm):
    class Meta:
        model = SceneUpload
        fields = ('scene_img', 'description', )

#class SceneUploadAnonymousForm(forms.ModelForm):
#    class Meta:
#        model = SceneUploadAnonymous
#        fields = ('scene_img', 'description', )

