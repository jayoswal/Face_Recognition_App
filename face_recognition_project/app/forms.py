from django import forms
from app.models import FaceRecognition

class FaceRecognitionForm(forms.ModelForm):
    
    class Meta:
        model = FaceRecognition
        fields = ['image']