from geopy.geocoders import Nominatim
from geopy.exc import GeocoderTimedOut, GeocoderUnavailable
import time

geolocator = Nominatim(user_agent="msbds")

def get_lat_long(location, retries=3, timeout=30):
    for attempt in range(retries):
        try:
            location = geolocator.geocode(location, timeout=timeout)
            if location:
                return location.latitude, location.longitude
        except (GeocoderTimedOut, GeocoderUnavailable) as e:
            print(f"Attempt {attempt+1} failed with error: {e}")
            time.sleep(2)  # Wait a bit before retrying
    raise GeocoderUnavailable(f"Geocoding service is unavailable after {retries} retries.")
