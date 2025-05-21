from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
import convertapi
from pathlib import Path
from .forms import UploadFileForm

def index(request):
    template = loader.get_template('document_recognition/index.html')
    form = UploadFileForm()
    context = {'form': form}
    return HttpResponse(template.render(context, request))

def process_file(request):
    try:
        if request.method == "POST":
            form = UploadFileForm(request.POST, request.FILES)
            if form.is_valid():
                uploaded_file = form.cleaned_data['file']
                form.cleaned_data['title'] = uploaded_file.name
                convert_file(request.FILES["file"])
                return HttpResponse("File Converted")
        return HttpResponse(f"Request invalid {request.method}, {str(form.is_valid())}, {request.FILES["file"]}, {form.cleaned_data['file']}")
    except Exception as ex:
        return HttpResponse(f"File Conversation Failed: {ex}")

def convert_file(file):
    OUTPUT_DIR = Path(__file__).resolve() / 'converted_files'
    INPUT_DIR = Path(__file__).resolve() / 'input_files'

    file_bytes = file.read()
    convertapi.api_credentials = 'secret_xiMuhdduJr4jhfwH'
    convertapi.convert('txt', {
        'File': file_bytes,
        'OcrLanguage': 'en',
        'EnableOcr': 'true'
    }, from_format='pdf').save_files(OUTPUT_DIR)