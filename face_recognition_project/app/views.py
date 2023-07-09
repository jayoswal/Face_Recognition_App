from django.shortcuts import render
from app.forms import *
from app.machine_learning import pipeline_model
import os

## new here
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.temp import NamedTemporaryFile
from urllib.request import urlopen
from django.core.files.storage import default_storage
from pytz import timezone 
from datetime import datetime
import gspread
from django.contrib.auth.decorators import login_required
# Create your views here.

global worksheet_month
def get_worksheet_month():
    try:
        # Load google service account
        gc = gspread.service_account(filename=os.path.join(settings.TOKEN_DIR,"employee-attendance-face-token-service.json"))
        
        # Read Google Sheet - 
        spreadsheet = gc.open('Employee_Attendance_Face')
        
        # Read WorkSheet of month
        cur_month = datetime.now(timezone("Asia/Kolkata")).strftime('%B')
        worksheet_month = spreadsheet.worksheet(cur_month)
    except:
        return render(request, 'custom_error.html', {'custom_error_message':"GSheet Error Check"})

    
    
    return worksheet_month
worksheet_month = get_worksheet_month()

# dictnary for storing properties
global properties_dict
properties_dict = dict()

@login_required(login_url='accounts/login')
def camera_photo(request):
    form = MarkAttendanceForm()
    # delete image
    img_save_path = os.path.join(settings.BASE_DIR, settings.SCANNED_IMG_TEMP_DATA,"new_camera.jpg")
    
    try:
        os.remove(img_save_path)
    except:
        pass
    result = None
    if request.method == 'POST':
        # TODO - Reduce call to Google Sheet API
        # TODO - Get all sheets operations in try except block
        # TODO - Check for all errors on client side, e.g- no webcamera/video feed
        # FIXME - DB Cred
        # FIXME - use token for api
        # FIXME - tel:
        # FIXME - check for Railway & video - https://www.youtube.com/watch?v=aVpFgp63PX4
        
        image_path = request.POST["src"]
        image = NamedTemporaryFile()
        urlopen(image_path).read()
        image.write(urlopen(image_path).read())
        image.flush()
        image = File(image)
        name = str(image.name).split('\\')[-1]
        name += '.jpg'  # store image in jpeg format
        image.name = name
        image_txt_path = os.path.join(settings.BASE_DIR, settings.SCANNED_IMG_TEMP_DATA, "image.txt")
        with open(image_txt_path, 'w+') as file:
            file.write(str(name))
        default_storage.save(img_save_path, ContentFile(urlopen(image_path).read()))
        image, result = pipeline_model(img_save_path)
        if len(result['count']) > 0:
            #  dynamic shift dynamic
            # if time is less then 15:15 i.e. 3:15 pm, Its Morning Slot,
            # Check if Morning_In is not None:
            #       shift = Morning_Out
            #       else: shift = Morning_In
            # if current time is after 15:15 i.e. 3:15 pm, Its Evening Slot,
            # Check if Evening_In is not None:
            #       shift = Evening_Out
            #       else: shift = Evening_In
            
            mark_date = datetime.now(timezone("Asia/Kolkata")).strftime('%d-%B-%Y')
            row  = worksheet_month.find(mark_date).row
            properties_dict['row'] = row
            try:
                col = worksheet_month.find(result['face_name'][0]).col
            except:
                error_message = "Ensure attendance sheet has column with your name."
                return render(request, 'custom_error.html', {'custom_error_message':error_message})

            properties_dict['col'] = col
            # default shift
            shift = "Morning_In"
            if int(datetime.now(timezone("Asia/Kolkata")).strftime('%H%M')) < 1515:
                # for morning shift, col == In, col+1 == Out
                if worksheet_month.cell(row, col).value is not None:
                     shift = "Morning_Out"
                else:
                    shift = "Morning_In"
            else:
                # for Evening shift, col+2 == In, col+3 == Out
                if worksheet_month.cell(row, col+2).value is not None:
                     shift = "Evening_Out"
                else:
                    shift = "Evening_In"
            properties_dict['shift'] = shift
                
            initial_dict = {
                'employee_name': result['face_name'][0],
                'mark_time':datetime.now(timezone("Asia/Kolkata")).strftime('%H:%M:%S'),
                'shift':shift
            }
            form = MarkAttendanceForm(initial = initial_dict)
            return render(request, 'result.html', {'result':result, 'form':form, 'has_face':True})
        else:
            return render(request, 'result.html', {'result':result, 'form':form, 'has_face':False})
            
    return render(request, 'camera_photo.html', {'result':"No Face"})

@login_required(login_url='accounts/login')
def save_atten(request):
    
    if request.method == "POST":
        form = MarkAttendanceForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            emp_mark_time=request.POST.get('mark_time')
            emp_shift=properties_dict['shift']
            row = properties_dict['row']
            col = properties_dict['col']
            if emp_shift == "Morning_Out":
                col += 1
            elif emp_shift == "Evening_In":
                col += 2
            elif emp_shift == "Evening_Out":
                col += 3
            try:
                data = worksheet_month.update_cell(row, col, emp_mark_time)
            except:
                return render(request, 'result.html', {'error_saving':True})            
            # After it has been written to sheet , Good to go ahead
            return render(request, 'success.html')
    
    return render(request, 'result.html', {'error_saving':True})
    
@login_required(login_url='accounts/login')
def index(request):
    return render(request, 'index.html')