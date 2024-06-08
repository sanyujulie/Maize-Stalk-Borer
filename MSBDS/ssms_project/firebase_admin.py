import firebase_admin
from firebase_admin import firestore
from firebase_admin import messaging
from firebase_admin import credentials
import time

cred = credentials.Certificate('C:\\Users\\Lenovo\\Desktop\\Maize-Stalk-Borer\\MSBDS\\ssms_project\\cornfield-f722a.json')
firebase_admin.initialize_app(cred)

# # Initialize Firestore
db = firestore.client()

def get_farmers_from_firestore():
    # Reference the 'Farmers' collection
    farmers_ref = db.collection('farmers')
    
    # Fetch all documents from the 'Farmers' collection
    docs = farmers_ref.stream()
    
    # Convert the documents to dictionaries and store them in a list
    farmers_list = []
    for doc in docs:
        farmer = doc.to_dict()
        farmer['id'] = doc.id  # Include the document ID if needed
        if 'createdAt' in farmer:
            farmer['createdAt'] = farmer['createdAt'].strftime('%B %d, %Y at %I:%M:%S %p %Z')  # Customize the format as needed
        farmers_list.append(farmer)
    
    return farmers_list

farmers = get_farmers_from_firestore()
print(farmers)


# kDO6i0hB6mRARvSY5B6FjHdcX6b_aTBZRCjCVZZxvUI


def send_notification(token, message):
    try:
        notification_message = messaging.Message(
            notification=messaging.Notification(
                title='Farm Alert',
                body=message,
            ),
            data={'confirmation_required': str(confirmation_required).lower()},

            token=token,
        )
        response = messaging.send(notification_message)
        print('Successfully sent notification:', response)
    except Exception as e:
        print(f'Error sending notification: {e}')

def get_distance_from_lat_lon_in_km(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of the earth in km
    dLat = math.radians(lat2 - lat1)
    dLon = math.radians(lon2 - lon1)
    a = (math.sin(dLat / 2) * math.sin(dLat / 2) +
         math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
         math.sin(dLon / 2) * math.sin(dLon / 2))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c  # Distance in km
    return distance

def listen_for_notifications():
    notifications_ref = db.collection('notifications')

    def on_snapshot(col_snapshot, changes, read_time):
        for change in changes:
            if change.type.name == 'ADDED':
                notification = change.document.to_dict()
                if notification.get('severity_level') == 'high':
                    print(f"High severity notification detected: {notification}")

                    # Fetch all farmers and send notifications to those with matching coordinates
                    farmers_ref = db.collection('farmers')
                    farmers = farmers_ref.stream()

                    for farmer in farmers:
                        farmer_data = farmer.to_dict()
                        if ('farmLocation' in notification and 
                            'farmLocation' in farmer_data and 
                            'latitude' in notification['farmLocation'] and 
                            'longitude' in notification['farmLocation'] and
                            'latitude' in farmer_data['farmLocation'] and
                            'longitude' in farmer_data['farmLocation']):

                            notif_lat = notification['farmLocation']['latitude']
                            notif_lon = notification['farmLocation']['longitude']
                            farmer_lat = farmer_data['farmLocation']['latitude']
                            farmer_lon = farmer_data['farmLocation']['longitude']

                            # Check if farmer coordinates match the notification coordinates
                            if (notif_lat == farmer_lat and notif_lon == farmer_lon):
                                if 'token' in farmer_data:
                                    print(f"Sending notification to token: {farmer_data['token']}")
                                    send_notification(farmer_data['token'], notification['message'])
                                else:
                                    print("Farmer does not have a token")
                        else:
                            print("Notification or farmer data does not contain location info")

    notifications_ref.on_snapshot(on_snapshot)

# Start listening for notifications
listen_for_notifications()

# Keep the script running
while True:
    time.sleep(1)