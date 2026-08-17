import os
from flask import Flask, flash, redirect, render_template, request, session, url_for

app = Flask(__name__)
app.secret_key = "leather_by_annuschka_secret_key"

# Product Catalog with accurate image mapping and categories
PRODUCTS = [
    # Travel & Luggage
    {
        "id": 1,
        "name": "Large Luggage / Travel Bag",
        "category": "Travel & Luggage",
        "price": 3850.00,
        "image": "Screenshot 2026-08-14 142732.jpeg",
        "description": "Spacious premium full-grain leather travel bag designed for extended journeys.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard (Large)"],
    },
    {
        "id": 2,
        "name": "Medium Luggage / Travel Bag",
        "category": "Travel & Luggage",
        "price": 3200.00,
        "image": "Medium_luggage_travel bag.png",
        "description": "Ideal weekend getaway bag crafted from durable, supple leather.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Medium"],
    },
    {
        "id": 3,
        "name": "Small Travel Bag / Overnight Bag",
        "category": "Travel & Luggage",
        "price": 2650.00,
        "image": "Small_luggage_travel bag1.png",
        "description": "Compact overnight travel bag with robust brass hardware and comfortable handles.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Small"],
    },
    {
        "id": 4,
        "name": "Overnight Bag",
        "category": "Travel & Luggage",
        "price": 2800.00,
        "image": "Overnight Bag.png",
        "description": "Classic structured overnight bag for seamless short trips.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 5,
        "name": "Medium Travel Bag / Doctor's Bag",
        "category": "Travel & Luggage",
        "price": 3100.00,
        "image": "Medium Travel Bag _Dokters bag.png",
        "description": "Vintage-inspired doctor's bag style with wide-frame opening.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Medium"],
    },
    # Handbags & Slings
    {
        "id": 6,
        "name": "Sling Bag / Satchel (Large)",
        "category": "Handbags & Slings",
        "price": 1950.00,
        "image": "Slingba-Sachel (large).png",
        "description": "Large artisan leather satchel with adjustable shoulder strap.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Large"],
    },
    {
        "id": 7,
        "name": "Sling Bag / Satchel (Medium)",
        "category": "Handbags & Slings",
        "price": 1650.00,
        "image": "Slingba-Sachel (medium).png",
        "description": "Medium everyday leather satchel combining elegance and practicality.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Medium"],
    },
    {
        "id": 8,
        "name": "Cross Body Sling Bag",
        "category": "Handbags & Slings",
        "price": 1450.00,
        "image": "Cross Bosy Sling Bag.png",
        "description": "Versatile cross-body bag for effortless daily wear.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 9,
        "name": "Adjustable Cross Body Bag / Moon Bag",
        "category": "Handbags & Slings",
        "price": 1350.00,
        "image": "Adjustable Cross bode Bag_Moon Bag.png",
        "description": "Contemporary curved moon bag with adjustable strap.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 10,
        "name": "Sling Bag",
        "category": "Handbags & Slings",
        "price": 1250.00,
        "image": "Sling Bag.png",
        "description": "Minimalist leather sling bag for essentials.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 11,
        "name": "Sling Bag 2",
        "category": "Handbags & Slings",
        "price": 1250.00,
        "image": "Sling Bag 2.png",
        "description": "Alternative design minimalist leather sling bag.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 12,
        "name": "Cellphone Sling Bag",
        "category": "Handbags & Slings",
        "price": 850.00,
        "image": "Celphone slingbag.png",
        "description": "Compact carrier perfectly sized for your smartphone and cards.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 13,
        "name": "Anti-theft Sling Bag",
        "category": "Handbags & Slings",
        "price": 1550.00,
        "image": "Anti-theft sling bag.jpeg",
        "description": "Secure travel sling bag with hidden zip compartments.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 14,
        "name": "Sling Bag (Small)",
        "category": "Handbags & Slings",
        "price": 1100.00,
        "image": "Sling bag (smal).jpeg",
        "description": "Petite leather sling for light days out.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Small"],
    },
    {
        "id": 15,
        "name": "Slingbag with Bow",
        "category": "Handbags & Slings",
        "price": 1350.00,
        "image": "Slingbag with bow.jpeg",
        "description": "Charming leather sling featuring a delicate handcrafted bow accent.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 16,
        "name": "Handbag 1",
        "category": "Handbags & Slings",
        "price": 2100.00,
        "image": "Handbag 1.png",
        "description": "Elegant structured leather handbag with twin carry handles.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 17,
        "name": "Handbag 2",
        "category": "Handbags & Slings",
        "price": 2200.00,
        "image": "Handbag 2.png",
        "description": "Sophisticated everyday handbag crafted from premium hide.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 18,
        "name": "Handbag 3",
        "category": "Handbags & Slings",
        "price": 2150.00,
        "image": "Handbag 3.png",
        "description": "Chic spacious handbag with secure zippered top.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 19,
        "name": "Handbag 4",
        "category": "Handbags & Slings",
        "price": 2300.00,
        "image": "Handbag 4.png",
        "description": "Luxury leather handbag with refined hardware details.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 20,
        "name": "Handbag 5",
        "category": "Handbags & Slings",
        "price": 2050.00,
        "image": "Handbag 5.png",
        "description": "Timeless leather handbag designed for versatile styling.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    # Backpacks & Laptop Bags
    {
        "id": 21,
        "name": "Backpack 1",
        "category": "Backpacks & Laptop Bags",
        "price": 2750.00,
        "image": "Backpac 1.png",
        "description": "Robust leather backpack with comfortable shoulder straps.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 22,
        "name": "Backpack 2",
        "category": "Backpacks & Laptop Bags",
        "price": 2850.00,
        "image": "Backpac 2.png",
        "description": "Executive leather backpack with ample internal compartments.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 23,
        "name": "Backpack 3",
        "category": "Backpacks & Laptop Bags",
        "price": 2700.00,
        "image": "Backpac 3.png",
        "description": "Sleek minimalist leather backpack for daily commutes.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 24,
        "name": "Backpack 4",
        "category": "Backpacks & Laptop Bags",
        "price": 2900.00,
        "image": "Backpac 4.png",
        "description": "Durable heavy-duty leather backpack built for adventure.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 25,
        "name": "Backpack with Handles",
        "category": "Backpacks & Laptop Bags",
        "price": 2950.00,
        "image": "Backpac with Handles.png",
        "description": "Versatile convertible backpack featuring top carry handles.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 26,
        "name": "Baby Backpack / Diaper Bag",
        "category": "Backpacks & Laptop Bags",
        "price": 2600.00,
        "image": "Baby backpack_diaper bag.png",
        "description": "Stylish leather diaper bag and backpack with stroller straps.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 27,
        "name": "Laptop Bag 1",
        "category": "Backpacks & Laptop Bags",
        "price": 2850.00,
        "image": "Laptop bag 1.png",
        "description": "Padded leather laptop briefcase for professionals.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["13 inch", "15 inch"],
    },
    {
        "id": 28,
        "name": "Laptop Bag 2",
        "category": "Backpacks & Laptop Bags",
        "price": 2950.00,
        "image": "Laptop bag 2.png",
        "description": "Premium leather messenger-style laptop bag.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["13 inch", "15 inch"],
    },
    {
        "id": 29,
        "name": "Laptop Bag 3",
        "category": "Backpacks & Laptop Bags",
        "price": 2800.00,
        "image": "Laptop bag 3.png",
        "description": "Sleek executive laptop bag with secure compartments.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["13 inch", "15 inch"],
    },
    {
        "id": 30,
        "name": "Laptop Sleeve 1",
        "category": "Backpacks & Laptop Bags",
        "price": 1200.00,
        "image": "Laptop sleeve 1.png",
        "description": "Minimalist protective leather laptop sleeve.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["13 inch", "15 inch"],
    },
    {
        "id": 31,
        "name": "Laptop Sleeve 2",
        "category": "Backpacks & Laptop Bags",
        "price": 1250.00,
        "image": "Laptop sleeve 2.png",
        "description": "Handcrafted leather sleeve with magnetic closure flap.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["13 inch", "15 inch"],
    },
    # Small Goods & Accessories
    {
        "id": 32,
        "name": "Coin Purse Large",
        "category": "Small Goods & Accessories",
        "price": 450.00,
        "image": "Coin purse Large.jpeg",
        "description": "Roomy leather coin and card purse.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 33,
        "name": "Coin Purse Medium",
        "category": "Small Goods & Accessories",
        "price": 350.00,
        "image": "Coin purse medium.jpeg",
        "description": "Compact coin purse for loose change and small essentials.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 34,
        "name": "Pencil Bag",
        "category": "Small Goods & Accessories",
        "price": 380.00,
        "image": "Pencil bag.jpeg",
        "description": "Durable leather pen and pencil case.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 35,
        "name": "Toiletries & Makeup Bag",
        "category": "Small Goods & Accessories",
        "price": 950.00,
        "image": "Toiletries_makup bag.jpeg",
        "description": "Spacious leather wash bag for travel grooming essentials.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    # Home, Leisure & Care
    {
        "id": 36,
        "name": "Leather Apron",
        "category": "Home, Leisure & Care",
        "price": 1850.00,
        "image": "Leather Apron.png",
        "description": "Heavy-duty handcrafted leather apron for cooking, crafting, and woodworking.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 37,
        "name": "Cooler Bag",
        "category": "Home, Leisure & Care",
        "price": 2400.00,
        "image": "Cooler bag.png",
        "description": "Insulated leather cooler bag for picnics and outdoor excursions.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 38,
        "name": "Wine Bag (Single Bottle)",
        "category": "Home, Leisure & Care",
        "price": 850.00,
        "image": "Wine Bag (Single bottle).png",
        "description": "Elegant single-bottle leather wine carrier with handle.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
    {
        "id": 39,
        "name": "Wine Bag (Double Bottle)",
        "category": "Home, Leisure & Care",
        "price": 1250.00,
        "image": "Wine Bag (Double Bottle).png",
        "description": "Luxurious double-bottle leather wine carrier for gifting.",
        "colors": ["Cognac", "Dark Brown", "Black"],
        "sizes": ["Standard"],
    },
]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shop')
def shop():
    category = request.args.get('category', 'All')
    search_query = request.args.get('q', '').strip().lower()
    
    filtered_products = PRODUCTS
    if category != 'All':
        filtered_products = [p for p in filtered_products if p['category'] == category]
    
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower() or search_query in p['description'].lower()]
        
    categories = ['All', 'Travel & Luggage', 'Handbags & Slings', 'Backpacks & Laptop Bags', 'Small Goods & Accessories', 'Home, Leisure & Care']
    
    return render_template('shop.html', products=filtered_products, categories=categories, selected_category=category, search_query=search_query)

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