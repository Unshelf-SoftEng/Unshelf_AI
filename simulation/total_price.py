import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("unshelf-d4567-firebase-adminsdk-m8g0j-b9bd0b7fd2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Reference to the orders collection
orders_collection = db.collection('orders')

# Reference to the products collection
products_collection = db.collection('products')

# Function to calculate total price for each order
def calculate_order_totals():
    # Fetch all orders
    orders = orders_collection.stream()

    for order in orders:
        order_data = order.to_dict()
        total_price = 0.0
        
        # Retrieve order items
        order_items = order_data.get('orderItems', [])

        # Calculate total price
        for item in order_items:
            product_id = item.get('productId')
            quantity = item.get('quantity')

            # Fetch product price
            product_doc = products_collection.document(product_id).get()
            if product_doc.exists:
                product_price = product_doc.to_dict().get('price', 0)
                total_price += product_price * quantity
            else:
                print(f"Product ID {product_id} not found.")
        
        print("Order's total price was calculated and updated successfully");

        # Update the order document with the total price
        orders_collection.document(order.id).update({'totalPrice': total_price})

# Run the function
calculate_order_totals()
