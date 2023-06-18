from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionForm
from app.machine_learning import pipeline_model
from django.conf import settings
from app.models import FaceRecognition
import os

# Create your views here.

def index(request):
    form = FaceRecognitionForm()
    
    if request.method == "POST":
        form = FaceRecognitionForm(request.POST or None, request.FILES or None)
        
        if form.is_valid():
            save = form.save(commit=True)
            
            # extract image object from database
            primary_key = save.pk
            img_obj = FaceRecognition.objects.get(pk=primary_key)
            image_path_db = str(img_obj.image)
            file_path = os.path.join(settings.MEDIA_ROOT, image_path_db)
            results = pipeline_model(file_path)
            print(results)
            
            print("[info] app - views - index, upload = True, with results")
            return render(request, 'index.html', {'form' : form, 'upload' : True, 'results' : results})
    
    print("[info] app - views - index, upload = False")
    return render(request, 'index.html', {'form' : form, 'upload' : False})