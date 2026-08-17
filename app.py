import os
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "leather_by_annuschka_secret_key"

# ===================================================================
# ALL PRODUCTS WITH YOUR EXACT IMAGE NAMES & PRICES
# ===================================================================

TRAVEL_PRODUCTS = [
    {"id": 1, "name": "Large Luggage / Travel Bag", "category": "Travel & Luggage", "price": 1725.00,
     "image": "Large_Luggage_travel bag.jpeg", "images": ["Large_Luggage_travel bag.jpeg"],
     "description": "Spacious premium full-grain leather travel bag designed for extended journeys.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard (Large)"]},
    {"id": 2, "name": "Medium Luggage / Travel Bag", "category": "Travel & Luggage", "price": 1150.00,
     "image": "Medium_luggage_travel bag.jpeg", "images": ["Medium_luggage_travel bag.jpeg", "Medium_luggage_travel bag1.jpeg"],
     "description": "Ideal weekend getaway bag crafted from durable, supple leather.",
     "colors": ["Dark", "Light"], "sizes": ["Medium"]},
    {"id": 3, "name": "Small Travel Bag / Overnight Bag", "category": "Travel & Luggage", "price": 680.00,
     "image": "Medium_luggage_travel bag1.jpeg", "images": ["Medium_luggage_travel bag1.jpeg"],
     "description": "Compact overnight travel bag with robust brass hardware and comfortable handles.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Small"]},
    {"id": 4, "name": "Overnight Bag", "category": "Travel & Luggage", "price": 1275.00,
     "image": "Overnight Bag.jpeg", "images": ["Overnight Bag.jpeg"],
     "description": "Classic structured overnight bag for seamless short trips.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 5, "name": "Medium Travel Bag / Dokters Bag", "category": "Travel & Luggage", "price": 910.00,
     "image": "Medium Travel Bag _Dokters bag.jpeg", "images": ["Medium Travel Bag _Dokters bag.jpeg"],
     "description": "Vintage-inspired doctor's bag style with wide-frame opening.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Medium"]},
]

TOILETRIES = {"id": 34, "name": "Toiletries & Makeup Bag", "category": "Small Goods & Accessories", "price": 450.00,
              "image": "Toiletries_makup bag.jpeg", "images": ["Toiletries_makup bag.jpeg"],
              "description": "Spacious leather wash bag for travel grooming essentials.",
              "colors": ["Brown", "Light Brown", "Dark Brown", "Black"], "sizes": ["Standard"]}

COIN_PURSES = {"id": 31, "name": "Coin Purse Large", "category": "Small Goods & Accessories", "price": 65.00,
               "image": "Coin purse Large.jpeg", "images": ["Coin purse Large.jpeg", "Coin purse Large 1.jpeg"],
               "description": "Roomy leather coin and card purse.", "colors": ["Brown"], "sizes": ["Standard"]}

PENCIL_BAGS = {"id": 33, "name": "Pencil Bag", "category": "Small Goods & Accessories", "price": 175.00,
               "image": "Pencil bag.jpeg", "images": ["Pencil bag.jpeg", "Pencil bag 1.jpeg", "Pencil bag 2.jpeg"],
               "description": "Durable leather pen and pencil case.",
               "colors": ["Light", "Medium", "Dark"], "sizes": ["Standard"]}

SLING_BAGS = [
    {"id": 14, "name": "Sling bag(smal)", "category": "Handbags & Slings", "price": 250.00,
     "image": "Sling bag (smal).jpeg", "images": ["Sling bag (smal).jpeg"],
     "description": "Petite leather sling for light days out.", "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Small"]},
    {"id": 7, "name": "Sling bag / Sachel(medium)", "category": "Handbags & Slings", "price": 435.00,
     "image": "Slingba-Sachel (medium).jpeg", "images": ["Slingba-Sachel (medium).jpeg"],
     "description": "Medium everyday leather satchel combining elegance and practicality.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Medium"]},
    {"id": 6, "name": "Sling Bag / Sachel(large)", "category": "Handbags & Slings", "price": 500.00,
     "image": "Slingba-Sachel (large).jpeg", "images": ["Slingba-Sachel (large).jpeg"],
     "description": "Large artisan leather satchel with adjustable shoulder strap.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Large"]},
    {"id": 13, "name": "Anti-Theft Sling Bag", "category": "Handbags & Slings", "price": 365.00,
     "image": "Anti-theft sling bag.jpeg", "images": ["Anti-theft sling bag.jpeg"],
     "description": "Secure travel sling bag with hidden zip compartments.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 8, "name": "Cross Bosy Sling Bag", "category": "Handbags & Slings", "price": 620.00,
     "image": "Cross Bosy Sling Bag.jpeg", "images": ["Cross Bosy Sling Bag.jpeg"],
     "description": "Versatile cross-body bag for effortless daily wear.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 9, "name": "Adjustable Cross bode Bag / Moon Bag", "category": "Handbags & Slings", "price": 655.00,
     "image": "Adjustable Cross bode Bag_Moon Bag.jpeg", "images": ["Adjustable Cross bode Bag_Moon Bag.jpeg"],
     "description": "Contemporary curved moon bag with adjustable strap.",
     "colors": ["Dark", "Light"], "sizes": ["Standard"]},
    {"id": 15, "name": "Slingbag with bow", "category": "Handbags & Slings", "price": 245.00,
     "image": "Slingbag with bow.jpeg", "images": ["Slingbag with bow.jpeg", "closeup.jpeg"],
     "description": "Charming leather sling featuring a delicate handcrafted bow accent.",
     "colors": ["Light", "Dark"], "sizes": ["Standard"]},
    {"id": 10, "name": "Sling Bag", "category": "Handbags & Slings", "price": 550.00,
     "image": "Sling Bag.jpeg", "images": ["Sling Bag.jpeg"],
     "description": "Minimalist leather sling bag for essentials.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 11, "name": "Sling Bag 2", "category": "Handbags & Slings", "price": 640.00,
     "image": "Sling Bag 2.jpeg", "images": ["Sling Bag 2.jpeg"],
     "description": "Alternative design minimalist leather sling bag.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 12, "name": "Cellphone sling back", "category": "Handbags & Slings", "price": 240.00,
     "image": "Celphone slingbag.jpeg", "images": ["Celphone slingbag.jpeg"],
     "description": "Compact carrier perfectly sized for your smartphone and cards.",
     "colors": ["Dark", "Medium", "Light"], "sizes": ["Standard"]},
]

HANDBAGS = [
    {"id": 20, "name": "Handbag", "category": "Handbags & Slings", "price": 650.00,
     "image": "Handbag 5.jpeg", "images": ["Handbag 5.jpeg"],
     "description": "Timeless leather handbag designed for versatile styling.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 19, "name": "Handbag", "category": "Handbags & Slings", "price": 450.00,
     "image": "Handbag 4.jpeg", "images": ["Handbag 4.jpeg"],
     "description": "Luxury leather handbag with refined hardware details.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 18, "name": "Handbag", "category": "Handbags & Slings", "price": 300.00,
     "image": "Handbag 3.jpeg", "images": ["Handbag 3.jpeg"],
     "description": "Chic spacious handbag with secure zippered top.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 17, "name": "Handbag", "category": "Handbags & Slings", "price": 700.00,
     "image": "Handbag 2.jpeg", "images": ["Handbag 2.jpeg"],
     "description": "Sophisticated everyday handbag crafted from premium hide.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 16, "name": "Handbag", "category": "Handbags & Slings", "price": 610.00,
     "image": "Handbag 1.jpeg", "images": ["Handbag 1.jpeg"],
     "description": "Elegant structured leather handbag with twin carry handles.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
]

LAPTOP_BAGS = [
    {"id": 27, "name": "Laptop Bag", "category": "Backpacks & Laptop Bags", "price": 750.00,
     "image": "Laptop bag 1.jpeg", "images": ["Laptop bag 1.jpeg"],
     "description": "Padded leather laptop briefcase for professionals.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["13 inch", "15 inch"]},
    {"id": 28, "name": "Laptop Bag", "category": "Backpacks & Laptop Bags", "price": 600.00,
     "image": "Laptop bag 2.jpeg", "images": ["Laptop bag 2.jpeg"],
     "description": "Premium leather messenger-style laptop bag.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["13 inch", "15 inch"]},
    {"id": 29, "name": "Laptop Bag", "category": "Backpacks & Laptop Bags", "price": 750.00,
     "image": "Laptop bag 3.jpeg", "images": ["Laptop bag 3.jpeg"],
     "description": "Sleek executive laptop bag with secure compartments.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["13 inch", "15 inch"]},
    {"id": 30, "name": "Laptop Sleeve", "category": "Backpacks & Laptop Bags", "price": 575.00,
     "image": "Laptop sleeve 2.jpeg", "images": ["Laptop sleeve 2.jpeg", "Laptop sleeve 1.jpeg"],
     "description": "Minimalist protective leather laptop sleeve.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["13 inch", "15 inch"]},
]

BACKPACKS = [
    {"id": 21, "name": "Backpack", "category": "Backpacks & Laptop Bags", "price": 735.00,
     "image": "Backpac 1.jpeg", "images": ["Backpac 1.jpeg"],
     "description": "Robust leather backpack with comfortable shoulder straps.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 22, "name": "Backpack", "category": "Backpacks & Laptop Bags", "price": 665.00,
     "image": "Backpac 2.jpeg", "images": ["Backpac 2.jpeg"],
     "description": "Executive leather backpack with ample internal compartments.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 23, "name": "Backpack", "category": "Backpacks & Laptop Bags", "price": 575.00,
     "image": "Backpac 3.jpeg", "images": ["Backpac 3.jpeg"],
     "description": "Sleek minimalist leather backpack for daily commutes.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Small"]},
    {"id": 24, "name": "Backpack", "category": "Backpacks & Laptop Bags", "price": 805.00,
     "image": "Backpac 4.jpeg", "images": ["Backpac 4.jpeg"],
     "description": "Durable heavy-duty leather backpack built for adventure.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 25, "name": "Backpack with Handles", "category": "Backpacks & Laptop Bags", "price": 655.00,
     "image": "Backpac with Handles.jpeg", "images": ["Backpac with Handles.jpeg"],
     "description": "Versatile convertible backpack featuring top carry handles.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 26, "name": "Baby Backpack / Diaper Bag", "category": "Backpacks & Laptop Bags", "price": 920.00,
     "image": "Baby backpack_diaper bag.jpeg", "images": ["Baby backpack_diaper bag.jpeg"],
     "description": "Stylish leather diaper bag and backpack with stroller straps.",
     "colors": ["Light", "Dark"], "sizes": ["Standard"]},
]

HOME_PRODUCTS = [
    {"id": 38, "name": "Wine Bag (Double Bottle)", "category": "Home, Leisure & Care", "price": 550.00,
     "image": "Wine Bag (Double Bottle).jpeg", "images": ["Wine Bag (Double Bottle).jpeg"],
     "description": "Luxurious double-bottle leather wine carrier for gifting.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 37, "name": "Wine Bag (Single bottle)", "category": "Home, Leisure & Care", "price": 356.00,
     "image": "Wine Bag (Single bottle).jpeg", "images": ["Wine Bag (Single bottle).jpeg"],
     "description": "Elegant single-bottle leather wine carrier with handle.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 36, "name": "Cooler Bag", "category": "Home, Leisure & Care", "price": 750.00,
     "image": "Cooler bag.jpeg", "images": ["Cooler bag.jpeg"],
     "description": "Insulated leather cooler bag for picnics and outdoor excursions.",
     "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 35, "name": "Leather Apron", "category": "Home, Leisure & Care", "price": 825.00,
     "image": "Leather Apron.jpeg", "images": ["Leather Apron.jpeg"],
     "description": "Heavy-duty handcrafted leather apron for cooking, crafting, and woodworking.",
     "colors": ["Light", "Dark"], "sizes": ["Standard"]},
]

BELTS = [
    {"id": 101, "name": "Leather Belt", "category": "Belts", "price": 200.00,
     "image": "Screenshot 2026-08-14 140410.jpeg", "images": [
         "Screenshot 2026-08-14 140410.jpeg", "Screenshot 2026-08-14 140415.jpeg",
         "Screenshot 2026-08-14 140419.jpeg", "Screenshot 2026-08-14 140423.jpeg",
         "Screenshot 2026-08-14 140428.jpeg", "Screenshot 2026-08-14 140432.jpeg",
         "Screenshot 2026-08-14 140436.jpeg", "Screenshot 2026-08-14 140441.jpeg"],
     "description": "Premium full-grain leather belt.", "colors": ["Black", "Brown"], "sizes": ["Standard"]},
]

LEATHER_CARE = [
    {"id": 102, "name": "Leather Care Cream with Microfiber Cloth", "category": "Leather Care", "price": 59.00,
     "image": "Screenshot 2026-08-14 140829.jpeg", "images": ["Screenshot 2026-08-14 140829.jpeg"],
     "description": "Protect and maintain your leather pieces.", "colors": ["Brown"], "sizes": ["Standard"]},
]

# ===================================================================
# REVIEWS (fixes the broken review section)
# ===================================================================
reviews = session.get('reviews', [])

@app.route('/add_review', methods=['POST'])
def add_review():
    name = request.form.get('reviewer_name')
    rating = request.form.get('rating')
    comment = request.form.get('comment')
    if name and comment:
        reviews.append({
            'name': name,
            'rating': int(rating),
            'comment': comment,
            'date': '2026'
        })
        session['reviews'] = reviews
        flash("Thank you for your review! ❤️", "success")
    return redirect(url_for('index'))

# ===================================================================
# ROUTES
# ===================================================================
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    category = request.args.get('category', 'All')
    search_query = request.args.get('q', '').strip().lower()
    
    filtered_products = []  # we will filter below
    
    if category != 'All':
        if category == 'Travel & Luggage':
            filtered_products = TRAVEL_PRODUCTS
        elif category == 'Handbags & Slings':
            filtered_products = SLING_BAGS + HANDBAGS
        elif category == 'Backpacks & Laptop Bags':
            filtered_products = LAPTOP_BAGS + BACKPACKS
        elif category == 'Small Goods & Accessories':
            filtered_products = [TOILETRIES, COIN_PURSES, PENCIL_BAGS]
        elif category == 'Home, Leisure & Care':
            filtered_products = HOME_PRODUCTS
        elif category == 'Belts':
            filtered_products = BELTS
        elif category == 'Leather Care':
            filtered_products = LEATHER_CARE
    
    if search_query:
        filtered_products = [p for p in filtered_products if 
                            search_query in p['name'].lower() or search_query in p['description'].lower()]
    
    categories = ['All', 'Travel & Luggage', 'Handbags & Slings', 'Backpacks & Laptop Bags',
                  'Small Goods & Accessories', 'Home, Leisure & Care', 'Belts', 'Leather Care']
    
    return render_template('shop.html',
                           products=filtered_products,
                           categories=categories,
                           selected_category=category,
                           search_query=search_query,
                           travel_products=TRAVEL_PRODUCTS,
                           toiletries=TOILETRIES,
                           coin_purses=COIN_PURSES,
                           pencil_bags=PENCIL_BAGS,
                           sling_bags=SLING_BAGS,
                           handbags=HANDBAGS,
                           laptop_bags=LAPTOP_BAGS,
                           backpacks=BACKPACKS,
                           home_products=HOME_PRODUCTS,
                           belts=BELTS,
                           leather_care=LEATHER_CARE)

@app.route('/cart')
def cart():
    cart_items = session.get('cart', [])
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    return render_template('cart.html', cart_items=cart_items, total=total)

@app.route('/add_to_cart/<int:product_id>', methods=['POST'])
def add_to_cart(product_id):
    product = None
    for p in TRAVEL_PRODUCTS:
        if p['id'] == product_id:
            product = p
            break
    if not product:
        for p in SLING_BAGS + HANDBAGS + LAPTOP_BAGS + BACKPACKS:
            if p['id'] == product_id:
                product = p
                break
    if not product:
        return redirect(url_for('shop'))
    
    if 'cart' not in session:
        session['cart'] = []
    cart = session['cart']
    
    color = request.form.get('color', product['colors'][0])
    size = request.form.get('size', product['sizes'][0])
    quantity = int(request.form.get('quantity', 1))
    
    existing = next((item for item in cart if item['id'] == product_id and item['color'] == color and item['size'] == size), None)
    if existing:
        existing['quantity'] += quantity
    else:
        cart.append({
            'id': product['id'],
            'name': product['name'],
            'price': product['price'],
            'image': product['image'],
            'color': color,
            'size': size,
            'quantity': quantity
        })
    session['cart'] = cart
    flash(f"Added {product['name']} to your cart!", "success")
    return redirect(url_for('cart'))

@app.route('/update_cart/<int:index>', methods=['POST'])
def update_cart(index):
    cart = session.get('cart', [])
    action = request.form.get('action')
    if 0 <= index < len(cart):
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
    
    total = sum(item['price'] * item['quantity'] for item in cart_items)
    
    if request.method == 'POST':
        name = request.form.get('name')
        session.pop('cart', None)
        return render_template('checkout_success.html', name=name, total=total)
        
    return render_template('checkout.html', cart_items=cart_items, total=total)

if __name__ == '__main__':
    app.run(debug=True)