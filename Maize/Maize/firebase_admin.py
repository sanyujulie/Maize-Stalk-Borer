import firebase_admin
from firebase_admin import firestore
from firebase_admin import messaging
from firebase_admin import credentials
import time

cred = credentials.Certificate('C:\\Users\\Lenovo\\Desktop\\MAIZE STALK FARM\\Maize\\Maize\\cornfield-f722a.json')
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

        # Add severity to the farmer dictionary    
        farmers_list.append(farmer)
    
    return farmers_list

farmers = get_farmers_from_firestore()
print(farmers)