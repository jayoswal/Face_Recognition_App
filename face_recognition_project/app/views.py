from django.shortcuts import render
from django.http import HttpResponse
from app.forms import FaceRecognitionForm
from app.machine_learning import pipeline_model
from django.conf import settings
from app.models import FaceRecognition
import os

## new here
from django.shortcuts import render
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.storage import default_storage

# Create your views here.

def camera_photo(request):
    if request.method == 'POST':
        result = None
        # delete imahe
        try:
            os.remove(img_save_path)
        except:
            pass
        image_path = request.POST["src"]
        image = NamedTemporaryFile()
        urlopen(image_path).read()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg'  # store image in jpeg format
        image.name = name
        with open('image.txt', 'w+') as file:
            file.write(str(name))
        img_save_path = os.path.join(settings.MEDIA_ROOT, "images/new_camera.jpg")
        default_storage.save(img_save_path, ContentFile(urlopen(image_path).read()))
        image, result = pipeline_model(img_save_path)

        return render(request, 'result.html', {'result':result})
    return render(request, 'camera_photo.html')

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
            
            # apply ML on the image with path
            results = pipeline_model(file_path)
            
            # update face name(s) after detection
            detected_face_name = results['face_name'] if len(results['face_name']) > 0 else "No Faces Detected."
            other_details_updated = FaceRecognition.objects.filter(id=primary_key).update(face_name=detected_face_name)
            print("Other details Updated - " + str(other_details_updated))
            print(results['face_name'])
            
            # print for reference
            print("[info] app - views - index, upload = True, with results")
            
            
            # return statement
            return render(request, 'index.html', {'form' : form, 'upload' : True, 'results' : results})
    
    print("[info] app - views - index, upload = False")
    return render(request, 'index.html', {'form' : form, 'upload' : False})