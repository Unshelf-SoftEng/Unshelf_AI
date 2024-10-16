import random
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore

# Initialize Firebase
cred = credentials.Certificate("unshelf-d4567-firebase-adminsdk-m8g0j-b9bd0b7fd2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def delete_documents_with_buyer_id_field():
    # Reference to the orders collection
    orders_ref = db.collection('orders')
    
    # Fetch all documents in the collection
    docs = orders_ref.stream()

    # Iterate through the documents and check for the existence of buyer_id
    for doc in docs:
        if 'buyer_id' in doc.to_dict():  # Check if buyer_id field exists
            print(f'Deleting document {doc.id} with buyer_id field.')
            orders_ref.document(doc.id).delete()


# Define the start and end orderId range
start_order_id = "20240901-000"  # Start of September
end_order_id = "20241031-999"    # End of October

# Query for documents where orderId is within the specified range
orders_ref = db.collection('orders')
query = orders_ref.order_by('__name__').start_at([start_order_id]).end_at([end_order_id])

# Execute the query and delete matching documents
docs = query.stream()

for doc in docs:
    # Print document id and delete it
    print(f"Deleting document with ID: {doc.id}, Order ID: {doc.to_dict()['orderId']}")
    db.collection('orders').document(doc.id).delete()


print(f"Documents with orderId between {start_order_id} and {end_order_id} have been deleted.")

# Run the deletion function
delete_documents_with_buyer_id_field()

