import firebase_admin
from firebase_admin import credentials, firestore

cred = credentials.Certificate("unshelf-d4567-firebase-adminsdk-m8g0j-b9bd0b7fd2.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Constants
TRANSACTION_FEE_PERCENTAGE = 0.02

def process_completed_orders():
    # Reference to the orders collection
    orders_ref = db.collection('orders')
    
    # Query to fetch all orders with status 'Completed'
    completed_orders_query = orders_ref.where(field_path='status', op_string='==', value='Completed')
    completed_orders = completed_orders_query.stream()

    for order_doc in completed_orders:
        order_data = order_doc.to_dict()
        order_id = order_doc.get('orderId')
        total_price = order_data.get('totalPrice', 0)
        seller_id = order_data.get('sellerId')
        order_date = order_data.get('completedAt')

        if order_date is None:
            print('Order Id' + order_id)
            print('Order Date not found')
            return


        # Calculate fees and earnings
        transaction_fee = round(total_price * TRANSACTION_FEE_PERCENTAGE, 2)
        seller_earnings = total_price - transaction_fee

        # Create a transaction record
        transaction_data = {
            'orderId': order_id,
            'totalPrice': total_price,
            'transactionFee': transaction_fee,
            'sellerEarnings': seller_earnings,
            'sellerId': seller_id,
            'date': order_date,
            'type': "sale"
        }

        # Store the transaction in Firestore
        db.collection('transactions').add(transaction_data)

        # Log the completion and transaction details
        print(f"Order {order_id} completed. Transaction recorded with the following details:")
        print(f"  Total Price: {total_price}")
        print(f"  Transaction Fee: {transaction_fee}")
        print(f"  Seller Earnings: {seller_earnings}")

# Example usage
process_completed_orders()