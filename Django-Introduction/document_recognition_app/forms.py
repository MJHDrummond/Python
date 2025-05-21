from django import forms
from .models import FileReaderModel

class UploadFileForm(forms.Form):
    title = forms.CharField(max_length=50, required=False)
    file = forms.FileField()

class FileReaderForm(forms.ModelForm):
    class Meta:
        model = FileReaderModel
        fields = ['file'] # I want this file(button) to be styled