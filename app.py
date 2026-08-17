# ... existing imports ...

# NEW PRODUCTS
BELTS = [
    {"id": 101, "name": "Leather Belt", "category": "Belts", "price": 200.00, "images": ["Screenshot 2026-08-14 140410.jpeg", "Screenshot 2026-08-14 140415.jpeg", "Screenshot 2026-08-14 140419.jpeg", "Screenshot 2026-08-14 140423.jpeg", "Screenshot 2026-08-14 140428.jpeg", "Screenshot 2026-08-14 140432.jpeg", "Screenshot 2026-08-14 140436.jpeg", "Screenshot 2026-08-14 140441.jpeg"], "colors": ["Black", "Brown"], "sizes": ["Standard"]},
]

LEATHER_CARE = [
    {"id": 102, "name": "Leather Care Cream with Microfiber Cloth", "category": "Leather Care", "price": 59.00, "images": ["Screenshot 2026-08-14 140829.jpeg"], "colors": ["Brown"], "sizes": ["Standard"]},
]

# UPDATED PRODUCTS (only the changes for your request – the rest stay as-is)
PRODUCTS = [
    # Travel & Luggage (your exact names/images)
    {"id": 1, "name": "Large Luggage / Travel Bag", "category": "Travel & Luggage", "price": 1725.00, "image": "Large_Luggage_travel bag.jpeg", "images": ["Large_Luggage_travel bag.jpeg"], "description": "Spacious premium full-grain leather travel bag...", "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard (Large)"]},
    {"id": 2, "name": "Medium Luggage / Travel Bag", "category": "Travel & Luggage", "price": 1150.00, "image": "Medium_luggage_travel bag.jpeg", "images": ["Medium_luggage_travel bag.jpeg", "Medium_luggage_travel bag1.jpeg"], "description": "Ideal weekend getaway bag...", "colors": ["Dark", "Light"], "sizes": ["Medium"]},
    {"id": 3, "name": "Small Travel Bag / Overnight Bag", "category": "Travel & Luggage", "price": 680.00, "image": "Medium_luggage_travel bag1.jpeg", "images": ["Medium_luggage_travel bag1.jpeg"], "description": "Compact overnight travel bag...", "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Small"]},
    {"id": 4, "name": "Overnight Bag", "category": "Travel & Luggage", "price": 1275.00, "image": "Overnight Bag.jpeg", "images": ["Overnight Bag.jpeg"], "description": "Classic structured overnight bag...", "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Standard"]},
    {"id": 5, "name": "Medium Travel Bag / Dokters Bag", "category": "Travel & Luggage", "price": 910.00, "image": "Medium Travel Bag _Dokters bag.jpeg", "images": ["Medium Travel Bag _Dokters bag.jpeg"], "description": "Vintage-inspired doctor's bag...", "colors": ["Cognac", "Dark Brown", "Black"], "sizes": ["Medium"]},
    # ... (all other original products stay exactly the same – I only changed the ones you listed) ...
    # (For brevity I kept the rest unchanged – they already had correct image names)
]

# Reviews in session
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
        flash("Thank you for your review!", "success")
    return redirect(url_for('index'))

# Your existing routes + new ones
@app.route('/shop')
def shop():
    category = request.args.get('category', 'All')
    search_query = request.args.get('q', '').strip().lower()
    filtered_products = PRODUCTS
    if category != 'All':
        filtered_products = [p for p in filtered_products if p['category'] == category]
    if search_query:
        filtered_products = [p for p in filtered_products if search_query in p['name'].lower() or search_query in p['description'].lower()]

    # Pass the new sections
    return render_template('shop.html', 
                           products=filtered_products, 
                           categories=['All', 'Travel & Luggage', 'Handbags & Slings', 'Backpacks & Laptop Bags', 'Small Goods & Accessories', 'Home, Leisure & Care', 'Belts', 'Leather Care'],
                           selected_category=category, 
                           search_query=search_query,
                           travel_products=filtered_products,  # or filter yourself if you want
                           belts=BELTS,
                           leather_care=LEATHER_CARE)

# (Your existing cart, checkout, update_cart routes stay exactly the same – they already support color/size/quantity)

if __name__ == '__main__':
    app.run(debug=True)