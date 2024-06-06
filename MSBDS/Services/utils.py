from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut

def get_lat_long(location):
    geolocator = Nominatim(user_agent="Services")
    try:
        location = geolocator.geocode(location)
        if location:
            return location.latitude, location.longitude
        else:
            return None, None
    except GeocoderTimedOut:
        return None, None
