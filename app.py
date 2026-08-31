import os
import hashlib
from urllib.parse import urlencode
from datetime import datetime, timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_apscheduler import APScheduler
import requests


app = Flask(__name__)

# --- Configuration & Environment Variables ---
app.secret_key = os.environ.get("SECRET_KEY", "leather_by_annuschka_secret_key")

# PostgreSQL Database URI with fallback to local SQLite
db_url = os.environ.get("DATABASE_URL", "sqlite:///studio.db")
if db_url.startswith("postgres://"):
    db_url = db_url.replace("postgres://", "postgresql://", 1)
app.config["SQLALCHEMY_DATABASE_URI"] = db_url
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)
scheduler = APScheduler()

# Brevo HTTPS REST API Credentials
BREVO_API_KEY = os.environ.get("SENDINBLUE_API_KEY") or os.environ.get("BREVO_API_KEY")
STUDIO_EMAIL = os.environ.get("STUDIO_EMAIL", "leatherbyannuschka@gmail.com")

# PayFast Merchant Credentials
PAYFAST_MERCHANT_ID = os.environ.get("PAYFAST_MERCHANT_ID", "10000100")
PAYFAST_MERCHANT_KEY = os.environ.get("PAYFAST_MERCHANT_KEY", "46f0cd694581a")
PAYFAST_PASSPHRASE = os.environ.get("PAYFAST_PASSPHRASE", "")
PAYFAST_URL = os.environ.get("PAYFAST_URL", "https://sandbox.payfast.co.za/eng/process")

# --- Database Models ---
class Order(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.String(50), primary_key=True)
    customer_name = db.Column(db.String(150), nullable=False)
    customer_email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(50), nullable=True)
    paxi_code = db.Column(db.String(200), nullable=True)
    items = db.Column(db.Text, nullable=False)
    subtotal = db.Column(db.Float, nullable=False)
    transport = db.Column(db.Float, nullable=False)
    sales_excl_transport = db.Column(db.Float, nullable=False)
    investor_cut = db.Column(db.Float, nullable=False)
    status = db.Column(db.String(50), default="Pending")  # Pending, Paid, Shipped
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    shipped_at = db.Column(db.DateTime, nullable=True)

class Review(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# --- Product Catalog ---
PRODUCTS = [
    {"id": 1, "name": "Large Luggage / Travel Bag", "category": "Travel Bags", "price": 1725.00, "images": ["Large_Luggage_travel bag.jpeg"], "description": "Spacious full-grain leather travel bag built for extended travel.", "colors": [], "sizes": []},
    {"id": 2, "name": "Medium Travel Bag", "category": "Travel Bags", "price": 1450.00, "images": ["Medium Travel Bag 1.jpeg", "Medium Travel Bag 2.jpeg"], "description": "Durable medium leather duffel bag.", "colors": [], "sizes": []},
    {"id": 6, "name": "Toiletries / Makeup Bag", "category": "Everyday Essentials", "price": 450.00, "images": ["Toiletries_makup bag.jpeg"], "description": "Handcrafted leather toilet bag. Please specify preferred brown shade.", "colors": ["Shade 1", "Shade 2", "Shade 3", "Shade 4"], "sizes": []},
    {"id": 7, "name": "Coin Purse", "category": "Everyday Essentials", "price": 55.00, "images": ["Coin purse medium 1.jpeg", "Coin purse medium.jpeg", "Coin purse Large.jpeg", "Coin purse Large 1.jpeg"], "description": "Genuine leather coin purse available in multiple brown shades.", "colors": ["Light Brown", "Medium Brown", "Dark Brown"], "sizes": ["Medium (R55)", "Large (R65)"], "size_prices": {"Medium (R55)": 55.00, "Large (R65)": 65.00}},
    {"id": 8, "name": "Pencil Bag", "category": "Everyday Essentials", "price": 175.00, "images": ["Pencil bag.jpeg", "Pencil bag 1.jpeg", "Pencil bag 2.jpeg"], "description": "Durable zipped leather pencil case.", "colors": ["Light", "Medium", "Dark"], "sizes": []},
    {"id": 40, "name": "Cosmetic / Makeup Bag", "category": "Everyday Essentials", "price": 180.00, "images": ["Screenshot 2026-08-19 093234.png"], "description": "Elegant cosmetic bag.", "colors": [], "sizes": []},
    {"id": 9, "name": "Sling Bag (Small)", "category": "Sling Bags", "price": 250.00, "images": ["Sling bag (smal).jpeg"], "description": "Lightweight petite leather sling bag.", "colors": [], "sizes": []},
    {"id": 10, "name": "Sling Bag (Medium)", "category": "Sling Bags", "price": 380.00, "images": ["Sling Bag (Medium).jpeg"], "description": "Versatile medium leather sling bag.", "colors": [], "sizes": []},
    {"id": 11, "name": "Sling Bag (Large)", "category": "Sling Bags", "price": 450.00, "images": ["Sling bag (large).jpeg"], "description": "Spacious daily leather sling bag.", "colors": [], "sizes": []},
]

CATEGORIES = ["All", "Travel Bags", "Everyday Essentials", "Sling Bags", "Handbags", "Laptop Bags", "Backpacks", "Home & Leisure", "Belts", "Leather Care"]

# --- HTTPS Email Sender via Brevo REST API ---
def send_email_https(subject, recipient_email, body_text):
    """Sends transactional email over HTTPS Port 443 to bypass firewall blocks."""
    if not BREVO_API_KEY:
        print(f"Warning: BREVO_API_KEY missing. Could not send email: {subject}")
        return False

    url = "https://api.brevo.com/v3/smtp/email"
    headers = {
        "accept": "application/json",
        "api-key": BREVO_API_KEY,
        "content-type": "application/json"
    }
    payload = {
        "sender": {"name": "Leather by Annuschka", "email": STUDIO_EMAIL},
        "to": [{"email": recipient_email}],
        "subject": subject,
        "textContent": body_text
    }
    
    response = requests.post(url, json=payload, headers=headers)
    if response.status_code not in [200, 201, 202]:
        raise Exception(f"Brevo API Error ({response.status_code}): {response.text}")
    return True

# --- PayFast Signature Verification ---
def generate_payfast_signature(data, passphrase=""):
    payload = []
    for key in sorted(data.keys()):
        if key != "signature" and data[key] != "":
            payload.append(f"{key}={data[key].strip()}")
    if passphrase:
        payload.append(f"passphrase={passphrase.strip()}")
    pf_string = "&".join(payload)
    return hashlib.md5(pf_string.encode("utf-8")).hexdigest()

# --- Background Scheduled Performance Reports ---
def generate_summary_email(period_name):
    with app.app_context():
        now = datetime.utcnow()
        if period_name == "Weekly":
            cutoff = now - timedelta(days=7)
            recent_orders = Order.query.filter(Order.timestamp >= cutoff, Order.status.in_(["Paid", "Shipped"])).all()
        else:
            first_this_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            last_prev_month = first_this_month - timedelta(days=1)
            recent_orders = Order.query.filter(
                db.extract('month', Order.timestamp) == last_prev_month.month,
                db.extract('year', Order.timestamp) == last_prev_month.year,
                Order.status.in_(["Paid", "Shipped"])
            ).all()

        total_orders = len(recent_orders)
        gross_revenue = sum(o.sales_excl_transport for o in recent_orders)
        jan_commission = gross_revenue * 0.10
        net_studio_payout = gross_revenue - jan_commission

        subject = f"Studio Performance Report ({period_name})"
        body = (
            f"Hi Annuschka,\n\nHere is your {period_name.lower()} studio summary:\n\n"
            f"  Total Orders: {total_orders}\n"
            f"  Gross Revenue (Excl. Shipping): R {gross_revenue:,.2f}\n"
            f"  Jan's Platform Fee (10%): R {jan_commission:,.2f}\n"
            f"  Net Studio Earnings: R {net_studio_payout:,.2f}\n\n"
            f"Check the studio dashboard for itemized details."
        )
        send_email_https(subject, STUDIO_EMAIL, body)

@scheduler.task('cron', id='weekly_report', day_of_week='fri', hour=8, minute=0)
def weekly_job():
    try:
        generate_summary_email("Weekly")
    except Exception as e:
        print(f"Weekly scheduled email error: {e}")

@scheduler.task('cron', id='monthly_report', day=1, hour=8, minute=0)
def monthly_job():
    try:
        generate_summary_email("Monthly")
    except Exception as e:
        print(f"Monthly scheduled email error: {e}")

# --- Flask Routes ---
@app.route('/')
def index():
    reviews = Review.query.order_by(Review.created_at.desc()).all()
    return render_template('index.html', reviews=reviews)

@app.route('/shop')
def shop():
    category = request.args.get('category', 'All')
    search_query = request.args.get('search', '').strip().lower()
    
    if category != 'All':
        filtered = [p for p in PRODUCTS if p['category'] == category]
    else:
        filtered = PRODUCTS

    if search_query:
        filtered = [p for p in filtered if search_query in p['name'].lower() or search_query in p['description'].lower()]

    return render_template('shop.html', products=filtered, categories=CATEGORIES, selected_category=category, search_query=search_query)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = next((p for p in PRODUCTS if p['id'] == product_id), None)
    if not product:
        flash("Product not found.", "danger")
        return redirect(url_for('shop'))

    color = request.form.get('color', product['colors'][0] if product['colors'] else '')
    size = request.form.get('size', product['sizes'][0] if product['sizes'] else '')
    price = product['size_prices'].get(size, product['price']) if 'size_prices' in product else product['price']

    cart = session.get('cart', [])
    cart.append({
        'id': product['id'],
        'name': product['name'],
        'price': price,
        'image': product['images'][0],
        'color': color,
        'size': size,
        'quantity': 1,
        'available_colors': product['colors'],
        'available_sizes': product['sizes']
    })
    session['cart'] = cart
    flash(f"Added {product['name']} to cart!", "success")
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:index>', methods=['POST'])
def update_cart(index):
    cart = session.get('cart', [])
    if 0 <= index < len(cart):
        action = request.form.get('action')
        if action == 'increase':
            cart[index]['quantity'] += 1
        elif action == 'decrease':
            cart[index]['quantity'] -= 1
            if cart[index]['quantity'] <= 0:
                cart.pop(index)
        elif action == 'remove':
            cart.pop(index)
        elif action == 'update_options':
            cart[index]['color'] = request.form.get('color', cart[index]['color'])
            cart[index]['size'] = request.form.get('size', cart[index]['size'])
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        return redirect(url_for('shop'))

    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping_option = request.args.get('shipping_option', '3-5') if request.method == 'GET' else request.form.get('shipping_option', '3-5')
    shipping_cost = 120.00 if shipping_option == '3-5' else 90.00
    total = subtotal + shipping_cost

    if request.method == 'POST':
        order_count = Order.query.count() + 1
        order_id = f"ORD-2026-{order_count:02d}"
        item_summary = ", ".join([f"{item['name']} ({item['quantity']})" for item in cart_items])
        first_name = request.form.get('first_name', '')
        last_name = request.form.get('last_name', '')
        customer_email = request.form.get('email', '')
        customer_name = f"{first_name} {last_name}".strip()

        # Save pending order to database
        new_order = Order(
            id=order_id,
            customer_name=customer_name,
            customer_email=customer_email,
            phone=request.form.get('phone', ''),
            paxi_code=request.form.get('paxi_code', ''),
            items=item_summary,
            subtotal=subtotal,
            transport=shipping_cost,
            sales_excl_transport=subtotal,
            investor_cut=round(subtotal * 0.10, 2),
            status="Pending"
        )
        db.session.add(new_order)
        db.session.commit()

        session['pending_order_id'] = order_id
        session['cart'] = []

        return render_template(
            'payfast_redirect.html',
            payfast_url=PAYFAST_URL,
            merchant_id=PAYFAST_MERCHANT_ID,
            merchant_key=PAYFAST_MERCHANT_KEY,
            return_url=url_for('payment_success', _external=True),
            cancel_url=url_for('cart', _external=True),
            notify_url=url_for('payfast_itn', _external=True),
            m_payment_id=order_id,
            amount=f"{total:.2f}",
            item_name=f"Leather by Annuschka Order #{order_id}",
            name_first=first_name,
            name_last=last_name,
            email_address=customer_email,
            cell_number=request.form.get('phone', '')
        )

    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, shipping=shipping_cost, total=total, selected_shipping=shipping_option)

@app.route('/payment_success')
def payment_success():
    order_id = session.get('pending_order_id')
    order = Order.query.get(order_id) if order_id else None
    return render_template('checkout_success.html', order_id=order_id, subtotal=order.subtotal if order else 0.0)

@app.route('/payfast/itn', methods=['POST'])
def payfast_itn():
    data = request.form.to_dict()
    
    # Optional PayFast signature verification
    if PAYFAST_PASSPHRASE:
        expected_sig = generate_payfast_signature(data, PAYFAST_PASSPHRASE)
        if data.get("signature") != expected_sig:
            return "Invalid Signature", 400

    if data.get('payment_status') == 'COMPLETE':
        order_id = data.get('m_payment_id')
        order = Order.query.get(order_id)
        if order:
            order.status = "Paid"
            db.session.commit()

            body_owner = (
                f"Hi Annuschka,\n\nA new order has been paid successfully!\n\n"
                f"Order ID: {order.id}\n"
                f"Customer: {order.customer_name} ({order.customer_email})\n"
                f"Phone: {order.phone}\n"
                f"PEP Paxi Store: {order.paxi_code}\n"
                f"Items: {order.items}\n"
                f"Total Paid: R {data.get('amount_gross', '0.00')}\n\n"
                f"Log into your Studio Dashboard to dispatch."
            )
            body_customer = (
                f"Hi {order.customer_name},\n\n"
                f"Thank you for supporting local craftsmanship!\n"
                f"We've received your payment for order #{order.id}.\n"
                f"Your order is being prepared with care in our studio."
            )
            try:
                send_email_https(f"New Paid Order #{order.id}", STUDIO_EMAIL, body_owner)
                if order.customer_email:
                    send_email_https(f"Order Confirmation #{order.id} - Leather by Annuschka", order.customer_email, body_customer)
            except Exception as e:
                print(f"ITN Email error: {e}")

        return "ITN Processed", 200

    return "Invalid Status", 400

@app.route('/dashboard')
def dashboard():
    now = datetime.utcnow()
    seven_days_ago = now - timedelta(days=7)

    all_orders = Order.query.order_by(Order.timestamp.desc()).all()
    weekly_orders = [o for o in all_orders if o.timestamp and o.timestamp >= seven_days_ago]
    pending_orders = [o for o in all_orders if o.status in ['Pending', 'Paid']]
    shipped_orders = [o for o in all_orders if o.status == 'Shipped']

    total_sales = sum(o.sales_excl_transport for o in all_orders if o.status in ['Paid', 'Shipped'])
    investor_cut = total_sales * 0.10

    return render_template(
        'dashboard.html',
        orders=all_orders,
        weekly_orders=weekly_orders,
        pending_orders=pending_orders,
        shipped_orders=shipped_orders,
        total_sales=total_sales,
        investor_cut=investor_cut,
        active_products=len(PRODUCTS)
    )

@app.route('/mark_shipped/<order_id>', methods=['POST'])
def mark_shipped(order_id):
    order = Order.query.get(order_id)
    if order:
        order.status = 'Shipped'
        order.shipped_at = datetime.utcnow()
        db.session.commit()

        if order.customer_email:
            subject = f"Your Order #{order.id} Has Shipped! - Leather by Annuschka"
            body = (
                f"Hi {order.customer_name},\n\n"
                f"Great news! Your handcrafted order #{order.id} ({order.items}) has been packaged and shipped from our studio.\n\n"
                f"PEP Paxi Destination: {order.paxi_code}\n\n"
                f"Thank you for supporting local South African craftsmanship!\n\n"
                f"Warm regards,\nLeather by Annuschka Studio"
            )
            try:
                send_email_https(subject, order.customer_email, body)
                flash(f"Order #{order_id} marked as shipped & email sent to {order.customer_email}!", "success")
            except Exception as e:
                flash(f"Order marked as shipped, but email failed: {e}", "warning")
        else:
            flash(f"Order #{order_id} marked as shipped (no email on file).", "info")
    return redirect(url_for('dashboard'))

@app.route('/add_review', methods=['POST'])
def add_review():
    name = request.form.get('name')
    rating = int(request.form.get('rating', 5))
    comment = request.form.get('comment')

    if name and comment:
        new_review = Review(name=name, rating=rating, comment=comment)
        db.session.add(new_review)
        db.session.commit()
        flash("Thank you for your review!", "success")
    return redirect(url_for('index') + '#reviews')

with app.app_context():
    db.create_all()

# --- App Initialization & Database Setup ---
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    scheduler.init_app(app)
    scheduler.start()
    app.run(debug=True)