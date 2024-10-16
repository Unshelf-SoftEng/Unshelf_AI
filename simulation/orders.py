import random
from datetime import datetime, timedelta
import firebase_admin
from firebase_admin import credentials, firestore
from collections import defaultdict

# Initialize Firebase
cred = credentials.Certificate("unshelf-d4567-firebase-adminsdk-m8g0j-b9bd0b7fd2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Constants
buyers = [
    "2wfeBvMr49XHtAYXWDNSPpEMj892",
    "DvVHPPSWMtV7GBFjSW1jymsv1op1"
]

sellers = {
    "2gxma4nHjhcHsOgDDDarlyeEvy12": ["129dGNJcv97ia63LFct7", "z5KIKYlz8ut2qN84q7p5"],
    "RAoWxQZXaxNOnOTMnbdUI8z82fd2": ["JO5r8Vkp1piH6u9wVMEX", "ollnbueZ8gShlZFh4iWM"],
    "MH5QOJLUzdYMs6a0OKluIY6Dudm1": ["T141TjxB0FcYrDGfRwco", "bpGvuTHq9RQ11ievURhI", "hfLOytmHTRJRJwiHBg5t", "oJwTibRIuXui80gwffv6"]
}

statuses = ["Pending", "Ready", "Completed"]

# Function to create an order
def create_order(order_id, buyer_id, order_date):
    seller_id = random.choice(list(sellers.keys()))
    products = sellers[seller_id]
    order_items = []
    status = random.choice(statuses)
    pickup_code = ''
    completed_at = None

    if status in ['Ready', 'Completed']:
        # Generate the pickup code for both 'Ready' and 'Completed' statuses
        pickup_code = ''.join(random.choices('1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=8))

    if status == 'Completed':
        # Add 'completed_at' for the 'Completed' status
        completed_at = order_date + timedelta(hours=1)

    for _ in range(random.randint(1, 5)):  # Random number of products in an order
        product_id = random.choice(products)
        quantity = random.randint(1, 10)  # Random quantity
        order_items.append({
            "productId": product_id,
            "quantity": quantity
        })

    return {
        "buyerId": buyer_id,
        "createdAt": order_date,
        "orderId": order_id,
        "orderItems": order_items,
        "sellerId": seller_id,
        "status": random.choice(statuses),
        "completedAt": completed_at,
        "pickupCode": pickup_code
    }

# Generate orders for September and October
orders = []
start_date = datetime(2024, 9, 1)
order_count_per_day = defaultdict(int)

# Generate 100 orders
for i in range(100):
   # Alternate between September and October
    if i < 50:
        order_date = start_date + timedelta(days=random.randint(0, 30))  # Random date in September
    else:
        order_date = start_date.replace(month=10) + timedelta(days=random.randint(0, 31))  # Random date in October

    # Add random hour (10 AM to 9 PM)
    random_hour = random.randint(10, 21)  # Random hour from 10 (10 AM) to 21 (9 PM)
    random_minute = random.randint(0, 59)  # Random minute

    # Set the hour and minute for the order date
    order_date = order_date.replace(hour=random_hour, minute=random_minute) 
    
    # Increment the order count for that specific day
    order_count_per_day[order_date.date()] += 1
    order_number = order_count_per_day[order_date.date()]
    
    # Generate the order ID with the reset counter per day
    order_id = f"{order_date.strftime('%Y%m%d')}-{str(order_number).zfill(3)}"
    
    # Choose a random buyer ID
    buyer_id = random.choice(buyers)
    
    # Append the order to the list
    orders.append(create_order(order_id, buyer_id, order_date))

for order in orders:
    db.collection('orders').add(order);

print("100 orders created successfully.")