import firebase_admin
from firebase_admin import credentials, firestore
from datetime import datetime, timedelta

# Initialize Firebase
cred = credentials.Certificate("unshelf-d4567-firebase-adminsdk-m8g0j-b9bd0b7fd2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def update_completed_orders():
    orders_ref = db.collection('orders')
    completed_orders = orders_ref.where('status', '==', 'Completed').stream()

    for order in completed_orders:
        order_data = order.to_dict()
        created_at = order_data.get('createdAt')

        if created_at:
            # Calculate completedAt timestamp (1 hour after createdAt)
            completed_at_timestamp = created_at + timedelta(hours=1)

            # Update the order with the completedAt field
            orders_ref.document(order.id).update({
                'completedAt': completed_at_timestamp
            })

            print(f"Updated order {order.id} with completedAt: {completed_at_timestamp}")

# Run the function to update completed orders
update_completed_orders()