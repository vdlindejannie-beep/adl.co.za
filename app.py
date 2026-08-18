import os
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "leather_by_annuschka_secret_key"

# PayFast Merchant Credentials
PAYFAST_MERCHANT_ID = "36712149"
PAYFAST_MERCHANT_KEY = "ur6ctzlgqfwbo"
PAYFAST_URL = "https://www.payfast.co.za/eng/process"  # Use https://sandbox.payfast.co.za/eng/process during testing

PRODUCTS = [
    # 1. Travel Bags
    {"id": 1, "name": "Large Luggage / Travel Bag", "category": "Travel Bags", "price": 1725.00, "images": ["Large_Luggage_travel bag.jpeg"], "description": "Spacious full-grain leather travel bag built for extended travel.", "colors": [], "sizes": []},
    {"id": 2, "name": "Medium Luggage / Travel Bag", "category": "Travel Bags", "price": 1150.00, "images": ["Medium_luggage_travel bag.png", "Medium_luggage_travel bag1.png"], "description": "Versatile weekend travel bag with sturdy handles.", "colors": ["Dark", "Light"], "sizes": []},
    {"id": 3, "name": "Small Travel Bag / Overnight Bag", "category": "Travel Bags", "price": 680.00, "images": ["Medium_luggage_travel bag1.png"], "description": "Compact travel companion for short trips and daily use.", "colors": ["Dark", "Light"], "sizes": []},
    {"id": 4, "name": "Overnight Bag", "category": "Travel Bags", "price": 1275.00, "images": ["Overnight Bag.png"], "description": "Classic structured leather overnight bag.", "colors": [], "sizes": []},
    {"id": 5, "name": "Medium Travel Bag / Doctor's Bag", "category": "Travel Bags", "price": 910.00, "images": ["Medium Travel Bag _Dokters bag.png"], "description": "Vintage wide-frame doctor's bag style travel carrier.", "colors": ["Dark", "Light"], "sizes": []},

    # 2. Everyday Essentials
    {"id": 6, "name": "Toiletries / Makeup Bag", "category": "Everyday Essentials", "price": 450.00, "images": ["Toiletries_makup bag.jpeg"], "description": "Handcrafted leather toilet bag. Please specify preferred brown shade.", "colors": ["Shade 1", "Shade 2", "Shade 3", "Shade 4"], "sizes": []},
    {"id": 7, "name": "Coin Purse", "category": "Everyday Essentials", "price": 55.00, "images": ["Coin purse medium 1.jpeg", "Coin purse medium.jpeg", "Coin purse Large.jpeg", "Coin purse Large 1.jpeg"], "description": "Genuine leather coin purse available in multiple brown shades.", "colors": ["Light Brown", "Medium Brown", "Dark Brown"], "sizes": ["Medium (R55)", "Large (R65)"], "size_prices": {"Medium (R55)": 55.00, "Large (R65)": 65.00}},
    {"id": 8, "name": "Pencil Bag", "category": "Everyday Essentials", "price": 175.00, "images": ["Pencil bag.jpeg", "Pencil bag 1.jpeg", "Pencil bag 2.jpeg"], "description": "Durable zipped leather pencil case.", "colors": ["Light", "Medium", "Dark"], "sizes": []},

    # 3. Sling Bags
    {"id": 9, "name": "Sling Bag (Small)", "category": "Sling Bags", "price": 250.00, "images": ["Sling bag (smal).jpeg"], "description": "Lightweight petite leather sling bag.", "colors": [], "sizes": []},
    {"id": 10, "name": "Sling Bag / Satchel (Medium)", "category": "Sling Bags", "price": 435.00, "images": ["Slingba-Sachel (medium).jpeg"], "description": "Medium everyday leather satchel.", "colors": [], "sizes": []},
    {"id": 11, "name": "Sling Bag / Satchel (Large)", "category": "Sling Bags", "price": 500.00, "images": ["Slingba-Sachel (large).png"], "description": "Roomy full-grain leather satchel sling bag.", "colors": [], "sizes": []},
    {"id": 12, "name": "Anti-Theft Sling Bag", "category": "Sling Bags", "price": 365.00, "images": ["Anti-theft sling bag.jpeg"], "description": "Secure sling bag featuring body-facing zip compartments.", "colors": [], "sizes": []},
    {"id": 13, "name": "Cross Body Sling Bag", "category": "Sling Bags", "price": 620.00, "images": ["Cross Bosy Sling Bag.png"], "description": "Classic cross-body leather bag for daily essentials.", "colors": [], "sizes": []},
    {"id": 14, "name": "Adjustable Cross Body Bag / Moon Bag", "category": "Sling Bags", "price": 655.00, "images": ["Adjustable Cross bode Bag_Moon Bag.png"], "description": "Curved moon bag with an adjustable strap.", "colors": ["Dark", "Light"], "sizes": []},
    {"id": 15, "name": "Slingbag with Bow", "category": "Sling Bags", "price": 245.00, "images": ["Slingbag with bow.jpeg", "closeup.jpeg"], "description": "Charming sling bag accented with a leather bow detail.", "colors": ["Light", "Dark"], "sizes": []},
    {"id": 16, "name": "Sling Bag", "category": "Sling Bags", "price": 550.00, "images": ["Sling Bag.png"], "description": "Minimalist handcrafted sling bag.", "colors": [], "sizes": []},
    {"id": 17, "name": "Sling Bag 2", "category": "Sling Bags", "price": 640.00, "images": ["Sling Bag 2.png"], "description": "Contemporary structured sling bag.", "colors": [], "sizes": []},
    {"id": 18, "name": "Cellphone Sling Bag", "category": "Sling Bags", "price": 240.00, "images": ["Celphone slingbag.png"], "description": "Sleek leather pouch for smartphone and cards.", "colors": ["Dark", "Medium", "Light"], "sizes": []},

    # 4. Handbags
    {"id": 19, "name": "Handbag 5", "category": "Handbags", "price": 650.00, "images": ["Handbag 5.png"], "description": "Elegant daily shoulder handbag.", "colors": [], "sizes": []},
    {"id": 20, "name": "Handbag 4", "category": "Handbags", "price": 450.00, "images": ["Handbag 4.png"], "description": "Classic leather handbag with top handles.", "colors": [], "sizes": []},
    {"id": 21, "name": "Handbag 3", "category": "Handbags", "price": 300.00, "images": ["Handbag 3.png"], "description": "Petite leather handbag.", "colors": [], "sizes": []},
    {"id": 22, "name": "Handbag 2", "category": "Handbags", "price": 700.00, "images": ["Handbag 2.png"], "description": "Premium structured tote handbag.", "colors": [], "sizes": []},
    {"id": 23, "name": "Handbag 1", "category": "Handbags", "price": 610.00, "images": ["Handbag 1.png"], "description": "Artisan leather handbag.", "colors": [], "sizes": []},

    # 5. Laptop Bags
    {"id": 24, "name": "Laptop Bag 1", "category": "Laptop Bags", "price": 750.00, "images": ["Laptop bag 1.png"], "description": "Padded leather work laptop bag.", "colors": [], "sizes": []},
    {"id": 25, "name": "Laptop Bag 2", "category": "Laptop Bags", "price": 600.00, "images": ["Laptop bag 2.png"], "description": "Sleek messenger-style laptop briefcase.", "colors": [], "sizes": []},
    {"id": 26, "name": "Laptop Bag 3", "category": "Laptop Bags", "price": 750.00, "images": ["Laptop bag 3.png"], "description": "Executive leather laptop bag with organizer pockets.", "colors": [], "sizes": []},
    {"id": 27, "name": "Laptop Sleeve", "category": "Laptop Bags", "price": 575.00, "images": ["Laptop sleeve 1.png", "Laptop sleeve 2.png"], "description": "Minimalist protective leather laptop sleeve.", "colors": [], "sizes": []},

    # 6. Backpacks
    {"id": 28, "name": "Backpack 1", "category": "Backpacks", "price": 735.00, "images": ["Backpac 1.png"], "description": "Handcrafted leather backpack.", "colors": [], "sizes": []},
    {"id": 29, "name": "Backpack 2", "category": "Backpacks", "price": 665.00, "images": ["Backpac 2.png"], "description": "Durable daily leather backpack.", "colors": [], "sizes": []},
    {"id": 30, "name": "Backpack 3", "category": "Backpacks", "price": 575.00, "images": ["Backpac 3.png"], "description": "Versatile leather backpack.", "colors": [], "sizes": ["Small (R575)", "Medium (R690)", "Large (R770)"], "size_prices": {"Small (R575)": 575.00, "Medium (R690)": 690.00, "Large (R770)": 770.00}},
    {"id": 31, "name": "Backpack 4", "category": "Backpacks", "price": 805.00, "images": ["Backpac 4.png"], "description": "Spacious premium leather backpack.", "colors": [], "sizes": []},
    {"id": 32, "name": "Backpack with Handles", "category": "Backpacks", "price": 655.00, "images": ["Backpac with Handles.png"], "description": "Convertible backpack with top carry handles.", "colors": [], "sizes": []},
    {"id": 33, "name": "Baby Backpack / Diaper Bag", "category": "Backpacks", "price": 920.00, "images": ["Baby backpack_diaper bag.png"], "description": "Stylish and functional leather diaper backpack.", "colors": ["Light", "Dark"], "sizes": []},

    # 7. Home & Leisure
    {"id": 34, "name": "Wine Bag (Double Bottle)", "category": "Home & Leisure", "price": 550.00, "images": ["Wine Bag (Double Bottle).png"], "description": "Luxurious double bottle leather wine carrier.", "colors": [], "sizes": []},
    {"id": 35, "name": "Wine Bag (Single Bottle)", "category": "Home & Leisure", "price": 356.00, "images": ["Wine Bag (Single bottle).png"], "description": "Single bottle leather wine holder.", "colors": [], "sizes": []},
    {"id": 36, "name": "Cooler Bag", "category": "Home & Leisure", "price": 750.00, "images": ["Cooler bag.png"], "description": "Insulated leather cooler bag for outdoor leisure.", "colors": [], "sizes": []},
    {"id": 37, "name": "Leather Apron", "category": "Home & Leisure", "price": 825.00, "images": ["Leather Apron.png"], "description": "Heavy-duty handcrafted leather apron.", "colors": ["Light", "Dark"], "sizes": []},

    # 8. Belts
    {
        "id": 38, 
        "name": "Leather Belt", 
        "category": "Belts", 
        "price": 200.00, 
        "images": [
            "Screenshot 2026-08-14 140410.png", 
            "Screenshot 2026-08-14 140415.png", 
            "Screenshot 2026-08-14 140419.png", 
            "Screenshot 2026-08-14 140423.png", 
            "Screenshot 2026-08-14 140428.png", 
            "Screenshot 2026-08-14 140432.png", 
            "Screenshot 2026-08-14 140436.png", 
            "Screenshot 2026-08-14 140441.png"
        ], 
        "description": "Handmade full-grain leather belt.", 
        "colors": ["Black", "Brown"], 
        "sizes": ["Small (30-32\")", "Medium (34-36\")", "Large (38-40\")", "X-Large (42-44\")"]
    },

    # 9. Leather Care
    {"id": 39, "name": "Leather Care Cream with Microfiber Cloth", "category": "Leather Care", "price": 59.00, "images": ["Screenshot 2026-08-14 140829.png"], "description": "Specialized leather conditioning cream complete with microfiber application cloth.", "colors": [], "sizes": []}
]

ORDERS = [
    {
        "id": "ORD-2026-01",
        "items": "Large Luggage / Travel Bag (1), Pencil Bag (1)",
        "subtotal": 1900.00,
        "transport": 100.00,
        "sales_excl_transport": 1900.00,
        "investor_cut": 190.00
    }
]

CATEGORIES = ["All", "Travel Bags", "Everyday Essentials", "Sling Bags", "Handbags", "Laptop Bags", "Backpacks", "Home & Leisure", "Belts", "Leather Care"]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    category = request.args.get('category', 'All')
    search_query = request.args.get('q', '').strip().lower()
    
    filtered = PRODUCTS
    if category != 'All':
        filtered = [p for p in filtered if p['category'] == category]
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
    if product:
        if 'cart' not in session:
            session['cart'] = []
        cart = session['cart']
        
        color = request.form.get('color', product['colors'][0] if product['colors'] else 'Standard')
        size = request.form.get('size', product['sizes'][0] if product['sizes'] else 'Standard')
        quantity = int(request.form.get('quantity', 1))
        
        unit_price = product['price']
        if 'size_prices' in product and size in product['size_prices']:
            unit_price = product['size_prices'][size]

        existing = next((item for item in cart if item['id'] == product_id and item['color'] == color and item['size'] == size), None)
        if existing:
            existing['quantity'] += quantity
        else:
            cart.append({
                'id': product['id'],
                'name': product['name'],
                'price': unit_price,
                'image': product['images'][0],
                'color': color,
                'size': size,
                'quantity': quantity
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
        session['cart'] = cart
    return redirect(url_for('cart'))

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    cart_items = session.get('cart', [])
    if not cart_items:
        flash("Your cart is empty.", "warning")
        return redirect(url_for('shop'))
    
    subtotal = sum(item['price'] * item['quantity'] for item in cart_items)
    shipping_cost = 120.00
    total = subtotal + shipping_cost

    if request.method == 'POST':
        order_id = f"ORD-2026-{len(ORDERS) + 1:02d}"
        item_summary = ", ".join([f"{item['name']} ({item['quantity']})" for item in cart_items])
        
        # Save temporary order details in session to verify upon PayFast return
        session['pending_order'] = {
            "id": order_id,
            "items": item_summary,
            "subtotal": subtotal,
            "transport": shipping_cost,
            "sales_excl_transport": subtotal,
            "investor_cut": round(subtotal * 0.10, 2)
        }

        # Render PayFast redirect form
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
            name_first=request.form.get('first_name', ''),
            name_last=request.form.get('last_name', ''),
            email_address=request.form.get('email', ''),
            cell_number=request.form.get('phone', '')
        )

    return render_template('checkout.html', cart_items=cart_items, subtotal=subtotal, shipping=shipping_cost, total=total)

@app.route('/payment_success')
def payment_success():
    pending_order = session.pop('pending_order', None)
    if pending_order:
        ORDERS.append(pending_order)
        session.pop('cart', None)
        return render_template('checkout_success.html', order_id=pending_order['id'], subtotal=pending_order['subtotal'])
    return redirect(url_for('shop'))

@app.route('/payfast_itn', methods=['POST'])
def payfast_itn():
    # ITN Webhook Listener for async PayFast notifications
    return "", 200

@app.route('/dashboard')
def dashboard():
    total_sales_excl_transport = sum(order['sales_excl_transport'] for order in ORDERS)
    investor_total_cut = total_sales_excl_transport * 0.10
    return render_template('dashboard.html', orders=ORDERS, total_sales=total_sales_excl_transport, investor_cut=investor_total_cut, active_products=len(PRODUCTS))

if __name__ == '__main__':
    app.run(debug=True)