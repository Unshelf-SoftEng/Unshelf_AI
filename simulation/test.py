import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate('unshelf-d4567-firebase-adminsdk-m8g0j-b9bd0b7fd2.json')
firebase_admin.initialize_app(cred)

# Initialize Firestore
db = firestore.client()

def test_firestore_connection():
    try:
        # Attempt to get all documents from a specific collection
        collection_ref = db.collection('orders')
        docs = collection_ref.stream()

        if docs:
            print("Access to Firestore is successful! Documents in the collection:")
            for doc in docs:
                print(f"{doc.id}: {doc.to_dict()}")
        else:
            print("No documents found in the collection.")
    
    except Exception as e:
        print("Error accessing Firestore:", e)

test_firestore_connection()

