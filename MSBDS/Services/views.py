from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from Services.forms import *
from Services.models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.http import JsonResponse, HttpResponse

from datetime import datetime, timedelta
from django.utils import timezone

from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.clickjacking import xframe_options_exempt
import json
from django.contrib import messages


from ssms_project.firebase_admin import get_farmers_from_firestore, get_captured_images
from .utils import get_lat_long
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from geopy.distance import geodesic
import openai

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
                'severity_level': farmer.get('severity_level', 'low')
            })

    context = {'farmers_with_location': farmers_with_location}
    return render(request, 'pages/map.html', context)

# ********************************************************************************************************


def send_notifications():
    farmers = get_farmers_from_firestore()

    for farmer in farmers:
        severity_level = farmer.get('severity_level', 'low')

        if severity_level == 'high':
            send_notification(farmer['token'], "Take precautionary measures and spray!")

        neighboring_farms = get_neighboring_farms(farmer)  # Function to get neighboring farms
        for neighbor in neighboring_farms:
            if neighbor.get('severity_level', 'low') == 'high':
                send_notification(neighbor['token'], "Take precautionary measures!")

# ********************************************************************************************************


@csrf_exempt
def chatbot_response(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        question = data.get('question')

        if question:
            try:
                response = openai.Completion.create(
                    engine="text-davinci-004",
                    prompt=question,
                    max_tokens=150
                )
                answer = response.choices[0].text.strip()
                return JsonResponse({'response': answer})
            except Exception as e:
                return JsonResponse({'response': 'Sorry, there was an error processing your request.'}, status=500)
        else:
            return JsonResponse({'response': 'No question provided.'}, status=400)

    return JsonResponse({'response': 'Invalid request method.'}, status=405)


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
            print("Form is valid")  # Debug output
            user = form.save()
            print("User saved:", user.username)  # Debug output
            return redirect('login')
        else:
            print("Form is not valid:", form.errors)  # Debug output
    else:
        form = RegistrationForm()
    return render(request, 'pages/register.html', {'form': form})


def advisories(request):
    return render(request, 'pages/advisories.html')

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            print(f"Attempting to authenticate user: {username}")  # Debug output
            user = authenticate(request, username=username, password=password)
            if user is not None:
                print("Authentication successful")  # Debug output
                login(request, user)
                return redirect('index')  # Redirect to the dashboard or home page after successful login
            else:
                error_message = "Invalid username or password."
                print("Authentication failed")  # Debug output
        else:
            error_message = "Invalid username or password."
    else:
        form = LoginForm()
        error_message = None
    return render(request, 'pages/login.html', {'form': form, 'error_message': error_message})


def logout_user(request):
    logout(request)
    return redirect('login')

@login_required
def index_view(request):
    registered_farmers_count = Farmer.objects.count()
    users_count = CustomUser.objects.count()
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
        
        'users_count': users_count,
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

@xframe_options_exempt
@login_required
def images(request):
    if request.method == 'POST':
        # Handling form submission if needed
        pass
        
    if request.method == 'GET':
        # Fetch registered farmers from Firestore
        # Assume get_farmers_from_firestore is a function that retrieves farmers from Firestore
        firestore_images = get_captured_images()

        # Pass the Firestore farmers data to the template context
        context = {'firestore_images': firestore_images, "menuclass": get_active_menu("images")}
        
        return render(request, 'pages/images.html', context)



# ***************************************Farmer endpoint************************************************************


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

                





    
