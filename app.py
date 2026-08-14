import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__)
# Use environment variable for secret key in production, with a secure fallback for local testing
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'your_random_secret_key_here')

# Mock product database (Update with Annuschka's actual leather products)
PRODUCTS = [
    {'id': 1, 'name': 'Leather Bag', 'price': 1200.00, 'image': 'bag.jpg'},
    # Add your other products here
]

@app.route('/')
def index():
    return render_template('index.html', products=PRODUCTS)

@app.route('/shop')
def shop():
    return render_template('shop.html', products=PRODUCTS)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):
    if 'cart' not in session:
        session['cart'] = []
    
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if product:
        session['cart'].append(product)
        session.modified = True
    return redirect(url_for('cart'))

@app.route('/cart')
def cart():
    return render_template('cart.html', cart=session.get('cart', []))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        # 1. Capture customer shipping details
        shipping_details = {
            'name': request.form.get('name'),
            'address': request.form.get('address'),
            'delivery_method': request.form.get('delivery_method')
        }
        session['shipping'] = shipping_details
        
        # Calculate total amount from cart
        total_amount = sum(p['price'] for p in session.get('cart', []))
        
        # Fetch Payfast merchant credentials securely from environment variables
        merchant_id = os.environ.get('PAYFAST_MERCHANT_ID', 'YOUR_MERCHANT_ID')
        
        # 2. Render Payfast redirect template
        return render_template('payfast_redirect.html', 
                               merchant_id=merchant_id, 
                               amount=total_amount,
                               item_name="Leather by Annuschka Order")
    return render_template('checkout.html')

@app.route('/payfast/itn', methods=['POST'])
def payfast_itn():
    """
    Payfast calls this endpoint automatically in the background 
    once a payment has been successfully processed.
    """
    data = request.form.to_dict()
    
    # Check if Payfast reports the payment as complete
    if data.get('payment_status') == 'COMPLETE':
        shipping_info = session.get('shipping', {})
        customer_name = shipping_info.get('name', 'Unknown Customer')
        delivery_address = shipping_info.get('address', 'Local Pickup')
        delivery_method = shipping_info.get('delivery_method', 'courier')
        
        cart_items = session.get('cart', [])
        item_summary = ", ".join([item['name'] for item in cart_items])
        total_amount = data.get('amount_gross', '0.00')
        
        # Trigger the email notification
        send_order_email(customer_name, delivery_address, delivery_method, item_summary, total_amount)
        
        # Clear cart and shipping info after successful completion
        session.pop('cart', None)
        session.pop('shipping', None)
        
    return '', 200

def send_order_email(name, address, delivery_method, items, amount):
    """
    Sends an email notification with the order details using Python's smtplib.
    """
    sender_email = os.environ.get('MAIL_USERNAME')
    sender_password = os.environ.get('MAIL_PASSWORD')
    receiver_email = os.environ.get('NOTIFICATION_EMAIL', sender_email)
    
    if not sender_email or not sender_password:
        print("Email credentials not configured.")
        return

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = f"New Paid Order: {name} - Leather by Annuschka"
    
    body = f"""
    New order successfully paid via Payfast!
    
    Customer Name: {name}
    Fulfillment Type: {delivery_method.upper()}
    Delivery Address: {address}
    
    Items Purchased: {items}
    Total Paid: R{amount}
    
    Please prepare this order for shipping or pickup.
    """
    msg.attach(MIMEText(body, 'plain'))
    
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
    except Exception as e:
        print(f"Failed to send order email: {e}")

if __name__ == '__main__':
    app.run(debug=True)