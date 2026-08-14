import os
from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'leather-by-annuschka-secret-key'

# In-memory database for reviews and orders
REVIEWS = [
    {"name": "Marike v.d. Merwe", "rating": 5, "comment": "Absolute top quality! The leather backpack exceeded all my expectations.", "date": "August 2026"},
    {"name": "Pieter B.", "rating": 5, "comment": "Brought the medium travel bag for a weekend trip. Beautiful craftsmanship and smells amazing.", "date": "August 2026"}
]

ORDERS = []

PRODUCTS = [
    # Travel Bags
    {
        "id": "large-luggage",
        "name": "Large Luggage / Travel Bag",
        "category": "Travel Bags",
        "price": 1725,
        "images": ["Large_Luggage_travel bag.jpeg"],
        "description": "Spacious handcrafted large travel bag built for durability and long journeys.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "medium-luggage",
        "name": "Medium Luggage / Travel Bag",
        "category": "Travel Bags",
        "price": 1150,
        "images": ["Medium_luggage_travel bag.jpeg", "Medium_luggage_travel bag1.jpeg"],
        "description": "Versatile medium luggage piece available in two classic shades.",
        "colors": ["Dark", "Light"],
        "sizes": []
    },
    {
        "id": "small-travel-bag",
        "name": "Small Travel Bag / Overnight Bag",
        "category": "Travel Bags",
        "price": 680,
        "images": ["Medium_luggage_travel bag1.jpeg"],
        "description": "Compact overnight travel bag for short trips.",
        "colors": ["Dark", "Light"],
        "sizes": []
    },
    {
        "id": "overnight-bag",
        "name": "Overnight Bag",
        "category": "Travel Bags",
        "price": 1275,
        "images": ["Overnight Bag.jpeg"],
        "description": "Premium overnight bag crafted with exceptional leather quality.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "medium-travel-bag-dokters",
        "name": "Medium Travel Bag / Doctor's Bag",
        "category": "Travel Bags",
        "price": 910,
        "images": ["Medium Travel Bag _Dokters bag.jpeg"],
        "description": "Classic structured doctor's style travel bag in two color options.",
        "colors": ["Dark", "Light"],
        "sizes": []
    },

    # Everyday Essentials
    {
        "id": "toiletries-makeup-bag",
        "name": "Toiletries / Makeup Bag",
        "category": "Everyday Essentials",
        "price": 450,
        "images": ["Toiletries_makup bag.jpeg"],
        "description": "Handcrafted toiletries and makeup bag. Available in 4 shades of brown (specify preference in comment).",
        "colors": ["Shade 1 (Light Brown)", "Shade 2 (Medium Brown)", "Shade 3 (Dark Brown)", "Shade 4 (Rich Chestnut)"],
        "sizes": []
    },
    {
        "id": "coin-purse",
        "name": "Coin Purse (Medium or Large)",
        "category": "Everyday Essentials",
        "price": 55,
        "images": ["Coin purse medium 1.jpeg", "Coin purse medium.jpeg", "Coin purse Large.jpeg", "Coin purse Large 1.jpeg"],
        "description": "Handcrafted coin purse available in Medium and Large across multiple shades of brown.",
        "colors": ["Multiple Shades of Brown"],
        "sizes": ["Medium", "Large"],
        "price_variants": {"Medium": 55, "Large": 65}
    },
    {
        "id": "pencil-bag",
        "name": "Pencil Bag",
        "category": "Everyday Essentials",
        "price": 175,
        "images": ["Pencil bag.jpeg", "Pencil bag 1.jpeg", "Pencil bag 2.jpeg"],
        "description": "Sturdy leather pencil bag available in light, medium, or dark colors.",
        "colors": ["Light", "Medium", "Dark"],
        "sizes": []
    },

    # Sling Bags
    {
        "id": "sling-bag-small",
        "name": "Sling Bag (Small)",
        "category": "Sling Bags",
        "price": 250,
        "images": ["Sling bag (smal).jpeg"],
        "description": "Compact and stylish small leather sling bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "sling-bag-satchel-medium",
        "name": "Sling Bag / Satchel (Medium)",
        "category": "Sling Bags",
        "price": 435,
        "images": ["Slingba-Sachel (medium).jpeg"],
        "description": "Medium-sized leather satchel / sling bag for everyday carry.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "sling-bag-satchel-large",
        "name": "Sling Bag / Satchel (Large)",
        "category": "Sling Bags",
        "price": 500,
        "images": ["Slingba-Sachel (large).jpeg"],
        "description": "Large leather satchel / sling bag offering generous storage.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "anti-theft-sling-bag",
        "name": "Anti-Theft Sling Bag",
        "category": "Sling Bags",
        "price": 365,
        "images": ["Anti-theft sling bag.jpeg"],
        "description": "Secure anti-theft design leather sling bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "cross-body-sling-bag",
        "name": "Cross Body Sling Bag",
        "category": "Sling Bags",
        "price": 620,
        "images": ["Cross Bosy Sling Bag.jpeg"],
        "description": "Comfortable and elegant cross-body leather sling bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "adjustable-cross-body-moon-bag",
        "name": "Adjustable Cross Body Bag / Moon Bag",
        "category": "Sling Bags",
        "price": 655,
        "images": ["Adjustable Cross bode Bag_Moon Bag.jpeg"],
        "description": "Versatile moon bag with adjustable strap, available in dark or light.",
        "colors": ["Dark", "Light"],
        "sizes": []
    },
    {
        "id": "slingbag-with-bow",
        "name": "Slingbag with Bow",
        "category": "Sling Bags",
        "price": 245,
        "images": ["Slingbag with bow.jpeg", "closeup.jpeg"],
        "description": "Charming sling bag accented with a leather bow detail. Available in light and dark.",
        "colors": ["Light", "Dark"],
        "sizes": []
    },
    {
        "id": "sling-bag",
        "name": "Sling Bag",
        "category": "Sling Bags",
        "price": 550,
        "images": ["Sling Bag.jpeg"],
        "description": "Classic everyday leather sling bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "sling-bag-2",
        "name": "Sling Bag 2",
        "category": "Sling Bags",
        "price": 640,
        "images": ["Sling Bag 2.jpeg"],
        "description": "Alternative design premium leather sling bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "cellphone-sling-bag",
        "name": "Cellphone Sling Bag",
        "category": "Sling Bags",
        "price": 240,
        "images": ["Celphone slingbag.jpeg"],
        "description": "Minimalist cellphone sling bag available in dark, medium, and light.",
        "colors": ["Dark", "Medium", "Light"],
        "sizes": []
    },

    # Handbags
    {
        "id": "handbag-5",
        "name": "Handbag",
        "category": "Handbags",
        "price": 650,
        "images": ["Handbag 5.jpeg"],
        "description": "Exquisite handcrafted leather handbag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "handbag-4",
        "name": "Handbag",
        "category": "Handbags",
        "price": 450,
        "images": ["Handbag 4.jpeg"],
        "description": "Timeless leather handbag design.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "handbag-3",
        "name": "Handbag",
        "category": "Handbags",
        "price": 300,
        "images": ["Handbag 3.jpeg"],
        "description": "Compact everyday leather handbag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "handbag-2",
        "name": "Handbag",
        "category": "Handbags",
        "price": 700,
        "images": ["Handbag 2.jpeg"],
        "description": "Spacious premium leather handbag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "handbag-1",
        "name": "Handbag",
        "category": "Handbags",
        "price": 610,
        "images": ["Handbag 1.jpeg"],
        "description": "Elegantly crafted signature leather handbag.",
        "colors": [],
        "sizes": []
    },

    # Laptop bags
    {
        "id": "laptop-bag-1",
        "name": "Laptop Bag",
        "category": "Laptop bags",
        "price": 750,
        "images": ["Laptop bag 1.jpeg"],
        "description": "Professional padded leather laptop bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "laptop-bag-2",
        "name": "Laptop Bag",
        "category": "Laptop bags",
        "price": 600,
        "images": ["Laptop bag 2.jpeg"],
        "description": "Sleek and slim leather laptop bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "laptop-bag-3",
        "name": "Laptop Bag",
        "category": "Laptop bags",
        "price": 750,
        "images": ["Laptop bag 3.jpeg"],
        "description": "Executive full-grain leather laptop bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "laptop-sleeve",
        "name": "Laptop Sleeve",
        "category": "Laptop bags",
        "price": 575,
        "images": ["Laptop sleeve 2.jpeg", "Laptop sleeve 1.jpeg"],
        "description": "Protective handcrafted leather laptop sleeve with dual image views.",
        "colors": [],
        "sizes": []
    },

    # Backpacks
    {
        "id": "backpack-1",
        "name": "Backpack",
        "category": "Backpacks",
        "price": 735,
        "images": ["Backpac 1.jpeg"],
        "description": "Rugged everyday leather backpack.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "backpack-2",
        "name": "Backpack",
        "category": "Backpacks",
        "price": 665,
        "images": ["Backpac 2.jpeg"],
        "description": "Comfortable and stylish leather backpack.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "backpack-3",
        "name": "Backpack",
        "category": "Backpacks",
        "price": 575,
        "images": ["Backpac 3.jpeg"],
        "description": "Multi-size leather backpack available in Small (R575), Medium (R690), and Large (R770).",
        "colors": [],
        "sizes": ["Small", "Medium", "Large"],
        "price_variants": {"Small": 575, "Medium": 690, "Large": 770}
    },
    {
        "id": "backpack-4",
        "name": "Backpack",
        "category": "Backpacks",
        "price": 805,
        "images": ["Backpac 4.jpeg"],
        "description": "Large capacity premium leather backpack.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "backpack-with-handles",
        "name": "Backpack with Handles",
        "category": "Backpacks",
        "price": 655,
        "images": ["Backpac with Handles.jpeg"],
        "description": "Versatile leather backpack featuring top carry handles.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "baby-backpack-diaper-bag",
        "name": "Baby Backpack / Diaper Bag",
        "category": "Backpacks",
        "price": 920,
        "images": ["Baby backpack_diaper bag.jpeg"],
        "description": "Thoughtfully designed leather diaper bag / baby backpack. Available in light or dark.",
        "colors": ["Light", "Dark"],
        "sizes": []
    },

    # Home & Leisure
    {
        "id": "wine-bag-double",
        "name": "Wine Bag (Double Bottle)",
        "category": "Home & Leisure",
        "price": 550,
        "images": ["Wine Bag (Double Bottle).jpeg"],
        "description": "Padded leather double wine bottle carrier.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "wine-bag-single",
        "name": "Wine Bag (Single Bottle)",
        "category": "Home & Leisure",
        "price": 356,
        "images": ["Wine Bag (Single bottle).jpeg"],
        "description": "Elegant single wine bottle leather carrier.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "cooler-bag",
        "name": "Cooler Bag",
        "category": "Home & Leisure",
        "price": 750,
        "images": ["Cooler bag.jpeg"],
        "description": "Insulated premium leather cooler bag.",
        "colors": [],
        "sizes": []
    },
    {
        "id": "leather-apron",
        "name": "Leather Apron",
        "category": "Home & Leisure",
        "price": 825,
        "images": ["Leather Apron.jpeg"],
        "description": "Durable handcrafted leather apron. Available in light and dark.",
        "colors": ["Light", "Dark"],
        "sizes": []
    },

    # Belts
    {
        "id": "leather-belt",
        "name": "Leather Belt",
        "category": "Belts",
        "price": 200,
        "images": [
            "Screenshot 2026-08-14 140410.jpeg",
            "Screenshot 2026-08-14 140415.jpeg",
            "Screenshot 2026-08-14 140419.jpeg",
            "Screenshot 2026-08-14 140423.jpeg",
            "Screenshot 2026-08-14 140428.jpeg",
            "Screenshot 2026-08-14 140432.jpeg",
            "Screenshot 2026-08-14 140436.jpeg",
            "Screenshot 2026-08-14 140441.jpeg"
        ],
        "description": "Classic full-grain leather belt. Multiple photos available to browse.",
        "colors": [],
        "sizes": []
    },

    # Leather care
    {
        "id": "leather-care-cream",
        "name": "Leather Care Cream with Microfiber Cloth",
        "category": "Leather care",
        "price": 59,
        "images": ["Screenshot 2026-08-14 140829.jpeg"],
        "description": "Premium leather care cream paired with a soft microfiber cloth to nourish and protect your leather items.",
        "colors": [],
        "sizes": []
    }
]

@app.route('/')
def index():
    return render_template('index.html', reviews=REVIEWS)

@app.route('/shop')
def shop():
    return render_template('shop.html', products=PRODUCTS)

@app.route('/checkout', methods=['GET', 'POST'])
def checkout():
    if request.method == 'POST':
        data = request.form
        order = {
            "name": data.get("name"),
            "email": data.get("email"),
            "phone": data.get("phone"),
            "address": data.get("address"),
            "comment": data.get("comment"),
            "items": data.get("items_json")
        }
        ORDERS.append(order)
        flash("Order inquiry submitted successfully! Annuschka will contact you shortly.", "success")
        return redirect(url_for('index'))
    return render_template('checkout.html')

@app.route('/add_review', methods=['POST'])
def add_review():
    name = request.form.get("reviewer_name")
    rating = int(request.form.get("rating", 5))
    comment = request.form.get("comment")
    if name and comment:
        REVIEWS.insert(0, {"name": name, "rating": rating, "comment": comment, "date": "August 2026"})
        flash("Thank you for your review!", "success")
    return redirect(url_for('index') + "#reviews")

if __name__ == '__main__':
    app.run(debug=True, port=5000)