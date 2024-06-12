from django.shortcuts import render
from Maize.firebase_admin import get_farmers_from_firestore
from .utils import get_lat_long

# Create your views here.
def advisories(request):
    return render(request, 'advisories.html')  

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
                'severity': farmer.get('severity', 'low')
            })

    context = {'farmers_with_location': farmers_with_location}
    return render(request, 'map.html', context)