from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Services.forms import *
from Services.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from datetime import datetime, timedelta
from django.utils import timezone
from Services.serializers import *
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from django.contrib import messages
from rest_framework import viewsets
from .serializers import FarmerSerializer
from ssms_project.firebase_admin import get_farmers_from_firestore
from .utils import get_lat_long


def map(request):
    farmers = get_farmers_from_firestore()

    farmers_with_location = []
    for farmer in farmers:
        lat, lng = get_lat_long(farmer['farmLocation'])
        if lat is not None and lng is not None:
            print(f"Location: {farmer['farmLocation']} -> Latitude: {lat}, Longitude: {lng}")  # Print coordinates
            farmers_with_location.append({
                'username': farmer['username'],
                'farmLocation': farmer['farmLocation'],
                'latitude': lat,
                'longitude': lng,
            })

    context = {'farmers_with_location': farmers_with_location}
    return render(request, 'pages/map.html', context)

def get_active_menu(active_page):
    return {'dashboard': ("active" if active_page == "dashboard" else "")
    , 'registered_farmers': ("active" if active_page == "registered_farmers" else "")
    , 'map': ("active" if active_page == "map" else "")
     ,'advisories': ("active" if active_page == "advisories" else "")
   }


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            pwd="ServiceSystem@2023"
            hashed_password = make_password(pwd)
            user.password = hashed_password

            user.save()
            return redirect('users') 
        else:
            return render(request, 'pages/register.html', {'form': form})
    
    else:
        form = RegistrationForm()
        return render(request, 'pages/register.html', {'form': form})


def advisories(request):
    return render(request, 'pages/advisories.html')

def login_view(request):
    
    if request.method == 'POST':
        form =  LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                # Redirect to a success page or dashboard
                return redirect('index')
            else:
                error_message = "Wrong credentials, Try using a different password !!!"
                return render(request, 'pages/login.html', {'form': form, 'error_message': error_message})
                 
        else:
            # Authentication failed, show an error message
            error_message = "Invalid username or password."
            return render(request, 'pages/login.html', {'form': form, 'error_message': error_message})

    if request.method == 'GET':
        error_message = None 
        form =  LoginForm()       
        return render(request, 'pages/login.html', {'form': form, 'error_message': error_message})

def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def index_view(request):
    registered_farmers_count = Farmer.objects.count()
    
    threshold_date = timezone.now() + timedelta(days=90)
    current_datetime = timezone.now()
    
   
        # Check if the user is logged in
    if request.user.is_authenticated:
        # Get the logged-in user's username
        user = request.user.username
    else:
        # If the user is not logged in, you can provide a default value
        user = "Guest"  # Replace with your desired default value

    context = {
        'registered_farmers_count': registered_farmers_count,
        
        'user': user,
        "menuclass": get_active_menu("dashboard") # pass active class

    }

    return render(request, 'pages/index.html', context)

@xframe_options_exempt
@login_required
def registered_farmers(request):
    if request.method == 'POST':
        # Handling form submission if needed
        pass
        
    if request.method == 'GET':
        # Fetch registered farmers from Firestore
        # Assume get_farmers_from_firestore is a function that retrieves farmers from Firestore
        firestore_farmers = get_farmers_from_firestore()

        # Pass the Firestore farmers data to the template context
        context = {'firestore_farmers': firestore_farmers, "menuclass": get_active_menu("registered_farmers")}
        
        return render(request, 'pages/registered_farmers.html', context)

# ***************************************Farmer endpoint************************************************************

class FarmerViewSet(viewsets.ModelViewSet):
    queryset = Farmer.objects.all()
    serializer_class = FarmerSerializer
# ***************************************Farmer endpoint************************************************************

    
@login_required
def users(request):
    # Retrieve active users from the User model (or your custom user model)
    users = CustomUser.objects.filter(is_active=True)

    context = {
        'users': users, 
        "menuclass": get_active_menu("users")
    }

    return render(request, 'pages/users.html', context)








def users(request):
    # Retrieve active users from the User model (or your custom user model)
    users = CustomUser.objects.all()
    form = RegistrationForm()

    context = {
        'users': users,
        'form': form,
       
        "menuclass": get_active_menu("users")
    }


    return render(request, 'pages/users.html', context)


@login_required
def blank_view(request):
    return render(request, 'pages/blank.html')

@login_required
def buttons(request):
    return render(request, 'pages/buttons.html')

@login_required
def cards(request):
    return render(request, 'pages/cards.html')

@login_required
def charts(request):
    return render(request, 'pages/charts.html')

def forgot_password_view(request):
    return render(request, 'pages/forgot-password.html')

def tables(request):
    return render(request, 'pages/tables.html')





@login_required
def utilities_anim_view(request):
    return render(request, 'pages/utilities-animation.html')

@login_required
def utilites_border_view(request):
    return render(request, 'pages/utilities-border.html')

@login_required
def utilities_color_view(request):
    return render(request, 'pages/utilities-color.html')

@login_required
def utilities_other_view(request):
    return render(request, 'pages/utilities-other.html')

def handle_404(request, exception):
    return render(request, 'pages/404.html', status=404)

def user_profile_view(request):
    # Get the user object of the logged-in user
    user = request.user

    # Create a context dictionary with user data
    context = {
        'user': user,  # Pass the user object to the template
    }
    return render(request, 'pages/user_profile.html', context)

def update_user(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        new_data = {
            'country': request.POST.get('country'),
            'department': request.POST.get('department'),
        }

        try:
            user = CustomUser.objects.get(pk=user_id)
            for key, value in new_data.items():
                setattr(user, key, value)
            user.save()
            return JsonResponse({'success': True})
        except CustomUser.DoesNotExist:
            return JsonResponse({'success': False, 'error': 'User not found'})

    return JsonResponse({'success': False, 'error': 'Invalid request method'})


def change_user_activity_status(request):
    if request.method == 'POST':
        api_response = {"error": True, "error_message": "API error"}
        user_id = request.POST.get('user_id')
        user = CustomUser.objects.filter(pk=user_id).first()
        if user:
            user.is_active = not user.is_active
            if user.is_active == True:
                status = "Active"
            else:
                status = "Deactivated"
            user.save()
            api_response["error"] = False
            api_response["error_message"] = f"{user.username}'s activity status has been updated to {status} successfully!"
        else:
            messages.error(request, "Invalid request!")
            api_response["error"] = True
            api_response["error_message"] = "Invalid Request"

        return JsonResponse(api_response)
    
    if request.method == 'GET':
        messages.error(request, f"Invalid request!")
        return redirect('users')
        

# class ExpiryNotificationsAPI(APIView):
#     def get(self, request):
#         current_date = timezone.now().date()
#         three_months_from_now = current_date + timedelta(days=90)
#         one_month_from_now = current_date + timedelta(days=30)

#         insurances_to_notify = InsuranceService.objects.filter(
#             expiry_date__range=[one_month_from_now, three_months_from_now]
#         )
#         serializer = InsuranceServiceSerializer(insurances_to_notify, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

                
def upload_temp_file(myfile, suggested_file_name):
    response = {"error": True, "error_msg": "Failed to upload"}
    try:
        # remove quites from file name
        from ssms_project.settings import MEDIA_ROOT
        import os
        saved_filename = os.path.join(MEDIA_ROOT, 'temp', suggested_file_name)
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(saved_filename, myfile)
        uploaded_file_url = fs.url(filename)
        response["error"] = False
        response["error_msg"] = "Success"
        response["uploaded_file_url"] = filename
        response["uploaded_file_name"] = filename[filename.rfind("/")+1:]
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to save file error:"+str(x)
    return response


def copy_file(source_file_url, destination_file_url):
    response = {"error": True, "error_msg": "Failed to upload"}
    try:
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.save(destination_file_url, fs.open(source_file_url))
        # from shutil import copy
        # uploaded_file_url = copy(source_file_url, destination_file_url)
        response["error"] = False
        response["error_msg"] = "Success"
        response["uploaded_file_url"] = filename
        response["uploaded_file_name"] = filename[filename.rfind("/")+1:]
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to save file error:"+str(x)
    return response

def delete_file(source_file_url):
    response = {"error": True, "error_msg": "Failed to delete"}
    try:
        from django.core.files.storage import FileSystemStorage
        fs = FileSystemStorage()
        filename = fs.delete(source_file_url)
        response["error"] = False
        response["error_msg"] = "Success"
    except Exception as x:
        response["error"] = True
        response["error_msg"] = "Failed to save file error:"+str(x)
    return response

@csrf_exempt  # disable token for now
@xframe_options_exempt #disable Xframe limit error
def upload_file(request):
    html = """"""
    control_id = 'unknown'
    file_name = ''
    exceed_size_limit = False
    if request.method == 'POST' and request.FILES.__sizeof__() > 0:
        for file in request.FILES:
            control_id = str(file).replace("_uploader","")
            myfile = request.FILES[file]
            # file should exceed maximu allowed size
            file_size_mbs = round(myfile.size / 1000000, 1)
            # use random file name everytime to avoid errors in spaces in filename
            ret = upload_temp_file(myfile, myfile.name)
            if ret["error"] is False:
                file_name = ret["uploaded_file_name"]  # save actual file_name

    #  tell iframe to do the need full
    file_preview_html = ""
    html = """
    <script>
    //set filename
    console.log('temp_file_saved','""" + control_id + """','""" + file_name + """');
    //check if single or multi upload
    //overwrite existing filename for single upload
    parent.document.getElementById('uploaded_file_for_""" + control_id + """').value = '""" + file_name + """';

    </script>
    """
    return HttpResponse(html)
    
