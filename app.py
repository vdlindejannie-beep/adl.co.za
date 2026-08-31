from datetime import datetime, timedelta
from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_apscheduler import APScheduler
import os
import requests

# 1. Initialize Flask Application
app = Flask(__name__)

# 2. App Configuration & Environment Variables
app.config["SECRET_KEY"] = os.environ.get(
    "FLASK_SECRET_KEY", "default-fallback-key"
)
BREVO_API_KEY = os.environ.get("SENDINBLUE_API_KEY")
STUDIO_EMAIL = os.environ.get("STUDIO_EMAIL", "leatherbyannuschka@gmail.com")

# Supabase Configuration (using direct REST API to prevent client library version clashes)
SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")

# Secure Dashboard Logins from Environment Variables
DASHBOARD_USER = os.environ.get("DASHBOARD_USER", "annuschka")
DASHBOARD_PASS = os.environ.get("DASHBOARD_PASS", "securepassword123")

# 3. Background Scheduler Setup
scheduler = APScheduler()
scheduler.init_app(app)
scheduler.start()

# --- PayFast Merchant Credentials ---
PAYFAST_MERCHANT_ID = "36712149"
PAYFAST_MERCHANT_KEY = "ur6ctzlgqfwbo"
PAYFAST_URL = "https://www.payfast.co.za/eng/process"

# --- Static Product Catalog ---
PRODUCTS = [
    {
        "id": 1,
        "name": "Large Luggage / Travel Bag",
        "category": "Travel Bags",
        "price": 1725.00,
        "images": ["Large_Luggage_travel bag.jpeg"],
        "description": (
            "Spacious full-grain leather travel bag built for extended"
            " travel."
        ),
        "colors": [],
        "sizes": [],
    },
    {
        "id": 2,
        "name": "Medium Luggage / Travel Bag",
        "category": "Travel Bags",
        "price": 1150.00,
        "images": [
            "Medium_luggage_travel bag.png",
            "Medium_luggage_travel bag1.png",
        ],
        "description": "Versatile weekend travel bag with sturdy handles.",
        "colors": ["Dark", "Light"],
        "sizes": [],
    },
    {
        "id": 3,
        "name": "Small Travel Bag / Overnight Bag",
        "category": "Travel Bags",
        "price": 680.00,
        "images": [
            "Small_luggage_travel bag1.jpeg",
            "Screenshot 2026-08-19 092959.png",
        ],
        "description": "Compact travel companion for short trips and daily use.",
        "colors": ["Dark", "Light"],
        "sizes": [],
    },
    {
        "id": 4,
        "name": "Overnight Bag",
        "category": "Travel Bags",
        "price": 1275.00,
        "images": ["Overnight Bag.png"],
        "description": "Classic structured leather overnight bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 5,
        "name": "Medium Travel Bag / Doctor's Bag",
        "category": "Travel Bags",
        "price": 910.00,
        "images": ["Medium Travel Bag _Dokters bag.png"],
        "description": "Vintage wide-frame doctor's bag style travel carrier.",
        "colors": ["Dark", "Light"],
        "sizes": [],
    },
    {
        "id": 6,
        "name": "Toiletries / Makeup Bag",
        "category": "Everyday Essentials",
        "price": 450.00,
        "images": ["Toiletries_makup bag.jpeg"],
        "description": (
            "Handcrafted leather toilet bag. Please specify preferred brown"
            " shade."
        ),
        "colors": ["Shade 1", "Shade 2", "Shade 3", "Shade 4"],
        "sizes": [],
    },
    {
        "id": 7,
        "name": "Coin Purse",
        "category": "Everyday Essentials",
        "price": 55.00,
        "images": [
            "Coin purse medium 1.jpeg",
            "Coin purse medium.jpeg",
            "Coin purse Large.jpeg",
            "Coin purse Large 1.jpeg",
        ],
        "description": (
            "Genuine leather coin purse available in multiple brown shades."
        ),
        "colors": ["Light Brown", "Medium Brown", "Dark Brown"],
        "sizes": ["Medium (R55)", "Large (R65)"],
        "size_prices": {"Medium (R55)": 55.00, "Large (R65)": 65.00},
    },
    {
        "id": 8,
        "name": "Pencil Bag",
        "category": "Everyday Essentials",
        "price": 175.00,
        "images": ["Pencil bag.jpeg", "Pencil bag 1.jpeg", "Pencil bag 2.jpeg"],
        "description": "Durable zipped leather pencil case.",
        "colors": ["Light", "Medium", "Dark"],
        "sizes": [],
    },
    {
        "id": 40,
        "name": "Cosmetic / Makeup Bag",
        "category": "Everyday Essentials",
        "price": 180.00,
        "images": ["Screenshot 2026-08-19 093234.png"],
        "description": "Elegant cosmetic bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 9,
        "name": "Sling Bag (Small)",
        "category": "Sling Bags",
        "price": 250.00,
        "images": ["Sling bag (smal).jpeg"],
        "description": "Lightweight petite leather sling bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 10,
        "name": "Sling Bag / Satchel (Medium)",
        "category": "Sling Bags",
        "price": 435.00,
        "images": ["Slingba-Sachel (medium).jpeg"],
        "description": "Medium everyday leather satchel.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 11,
        "name": "Sling Bag / Satchel (Large)",
        "category": "Sling Bags",
        "price": 500.00,
        "images": ["Slingba-Sachel (large).png"],
        "description": "Roomy full-grain leather satchel sling bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 12,
        "name": "Anti-Theft Sling Bag",
        "category": "Sling Bags",
        "price": 365.00,
        "images": ["Anti-theft sling bag.jpeg"],
        "description": (
            "Secure sling bag featuring body-facing zip compartments."
        ),
        "colors": [],
        "sizes": [],
    },
    {
        "id": 13,
        "name": "Cross Body Sling Bag",
        "category": "Sling Bags",
        "price": 620.00,
        "images": ["Cross Bosy Sling Bag.png"],
        "description": "Classic cross-body leather bag for daily essentials.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 14,
        "name": "Adjustable Cross Body Bag / Moon Bag",
        "category": "Sling Bags",
        "price": 655.00,
        "images": ["Adjustable Cross bode Bag_Moon Bag.png"],
        "description": "Curved moon bag with an adjustable strap.",
        "colors": ["Dark", "Light"],
        "sizes": [],
    },
    {
        "id": 15,
        "name": "Slingbag with Bow",
        "category": "Sling Bags",
        "price": 245.00,
        "images": ["Slingbag with bow.jpeg", "closeup.jpeg"],
        "description": "Charming sling bag accented with a leather bow detail.",
        "colors": ["Light", "Dark"],
        "sizes": [],
    },
    {
        "id": 16,
        "name": "Sling Bag",
        "category": "Sling Bags",
        "price": 550.00,
        "images": ["Sling Bag.png"],
        "description": "Minimalist handcrafted sling bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 17,
        "name": "Sling Bag 2",
        "category": "Sling Bags",
        "price": 640.00,
        "images": ["Sling Bag 2.png"],
        "description": "Contemporary structured sling bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 18,
        "name": "Cellphone Sling Bag",
        "category": "Sling Bags",
        "price": 240.00,
        "images": ["Celphone slingbag.png"],
        "description": "Sleek leather pouch for smartphone and cards.",
        "colors": ["Dark", "Medium", "Light"],
        "sizes": [],
    },
    {
        "id": 19,
        "name": "Handbag 1",
        "category": "Handbags",
        "price": 650.00,
        "images": ["Handbag 5.png"],
        "description": "Elegant daily shoulder handbag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 20,
        "name": "Handbag 2",
        "category": "Handbags",
        "price": 450.00,
        "images": ["Handbag 4.png"],
        "description": "Classic leather handbag with top handles.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 21,
        "name": "Handbag 3",
        "category": "Handbags",
        "price": 300.00,
        "images": ["Handbag 3.png"],
        "description": "Petite leather handbag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 22,
        "name": "Handbag 4",
        "category": "Handbags",
        "price": 700.00,
        "images": ["Handbag 2.png"],
        "description": "Premium structured tote handbag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 23,
        "name": "Handbag 5",
        "category": "Handbags",
        "price": 610.00,
        "images": ["Handbag 1.png"],
        "description": "Artisan leather handbag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 24,
        "name": "Laptop Bag 1",
        "category": "Laptop Bags",
        "price": 750.00,
        "images": ["Laptop bag 1.png"],
        "description": "Padded leather work laptop bag.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 25,
        "name": "Laptop Bag 2",
        "category": "Laptop Bags",
        "price": 600.00,
        "images": ["Laptop bag 2.png"],
        "description": "Sleek messenger-style laptop briefcase.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 26,
        "name": "Laptop Bag 3",
        "category": "Laptop Bags",
        "price": 750.00,
        "images": ["Laptop bag 3.png"],
        "description": "Executive leather laptop bag with organizer pockets.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 27,
        "name": "Laptop Sleeve",
        "category": "Laptop Bags",
        "price": 575.00,
        "images": ["Laptop sleeve 2.png", "Laptop sleeve 1.png"],
        "description": "Minimalist protective leather laptop sleeve.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 28,
        "name": "Backpack 1",
        "category": "Backpacks",
        "price": 735.00,
        "images": ["Backpac 1.png"],
        "description": "Handcrafted leather backpack.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 29,
        "name": "Backpack 2",
        "category": "Backpacks",
        "price": 665.00,
        "images": ["Backpac 2.png"],
        "description": "Durable daily leather backpack.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 30,
        "name": "Backpack 3",
        "category": "Backpacks",
        "price": 575.00,
        "images": ["Backpac 3.png"],
        "description": "Versatile leather backpack.",
        "colors": [],
        "sizes": ["Small (R575)", "Medium (R690)", "Large (R770)"],
        "size_prices": {
            "Small (R575)": 575.00,
            "Medium (R690)": 690.00,
            "Large (R770)": 770.00,
        },
    },
    {
        "id": 31,
        "name": "Backpack 4",
        "category": "Backpacks",
        "price": 805.00,
        "images": ["Backpac 4.png"],
        "description": "Spacious premium leather backpack.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 32,
        "name": "Backpack with Handles",
        "category": "Backpacks",
        "price": 655.00,
        "images": ["Backpac with Handles.png"],
        "description": "Convertible backpack with top carry handles.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 33,
        "name": "Baby Backpack / Diaper Bag",
        "category": "Backpacks",
        "price": 920.00,
        "images": ["Baby backpack_diaper bag.png"],
        "description": "Stylish and functional leather diaper backpack.",
        "colors": ["Light", "Dark"],
        "sizes": [],
    },
    {
        "id": 34,
        "name": "Wine Bag (Double Bottle)",
        "category": "Home & Leisure",
        "price": 550.00,
        "images": ["Wine Bag (Double Bottle).png"],
        "description": "Luxurious double bottle leather wine carrier.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 35,
        "name": "Wine Bag (Single Bottle)",
        "category": "Home & Leisure",
        "price": 365.00,
        "images": ["Wine Bag (Single bottle).png"],
        "description": "Single bottle leather wine holder.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 36,
        "name": "Cooler Bag",
        "category": "Home & Leisure",
        "price": 750.00,
        "images": ["Cooler bag.png"],
        "description": "Insulated leather cooler bag for outdoor leisure.",
        "colors": [],
        "sizes": [],
    },
    {
        "id": 37,
        "name": "Leather Apron",
        "category": "Home & Leisure",
        "price": 825.00,
        "images": ["Leather Apron.png"],
        "description": "Heavy-duty handcrafted leather apron.",
        "colors": ["Light", "Dark"],
        "sizes": [],
    },
    {
        "id": 38,
        "name": "Leather Belt",
        "category": "Belts",
        "price": 200.00,
        "images": ["Screenshot 2026-08-14 140410.png"],
        "description": "Handmade full-grain leather belt.",
        "colors": ["Black", "Brown"],
        "sizes": [
            'Small (30-32")',
            'Medium (34-36")',
            'Large (38-40")',
            'X-Large (42-44")',
        ],
    },
    {
        "id": 39,
        "name": "Leather Care Cream with Microfiber Cloth",
        "category": "Leather Care",
        "price": 59.00,
        "images": ["WhatsApp Image 2026-08-18 at 15.25.08.jpeg"],
        "description": (
            "Specialized leather conditioning cream complete with microfiber"
            " application cloth."
        ),
        "colors": [],
        "sizes": [],
    },
]

CATEGORIES = [
    "All",
    "Travel Bags",
    "Everyday Essentials",
    "Sling Bags",
    "Handbags",
    "Laptop Bags",
    "Backpacks",
    "Home & Leisure",
    "Belts",
    "Leather Care",
]
PEPAXI_OPTIONS = {
    "3-5": {"name": "PEP Paxi (3-5 Business Days)", "price": 120.00},
    "7-9": {"name": "PEP Paxi (7-9 Business Days)", "price": 90.00},
}


# --- Database Helper Functions (Supabase REST API) ---
def get_db_reviews():
  if SUPABASE_URL and SUPABASE_KEY:
    try:
      headers = {
          "apikey": SUPABASE_KEY,
          "Authorization": f"Bearer {SUPABASE_KEY}",
          "Content-Type": "application/json",
      }
      response = requests.get(
          f"{SUPABASE_URL}/rest/v1/reviews?select=*&order=created_at.desc",
          headers=headers,
          timeout=5,
      )
      if response.status_code == 200:
        data = response.json()
        if data:
          return data
    except Exception as e:
      print(f"Supabase fetch reviews error: {e}")
  return [
      {
          "name": "Sarah M.",
          "rating": 5,
          "comment": (
              "Absolutely beautiful leather quality! Bought the overnight bag"
              " and it gets so many compliments."
          ),
          "created_at": "2026-08-01T10:00:00",
      },
      {
          "name": "Johan K.",
          "rating": 5,
          "comment": (
              "Sturdy belt and fast delivery. Very impressed with the"
              " craftsmanship."
          ),
          "created_at": "2026-08-02T10:00:00",
      },
  ]


def get_db_orders():
  if SUPABASE_URL and SUPABASE_KEY:
    try:
      headers = {
          "apikey": SUPABASE_KEY,
          "Authorization": f"Bearer {SUPABASE_KEY}",
          "Content-Type": "application/json",
      }
      response = requests.get(
          f"{SUPABASE_URL}/rest/v1/orders?select=*&order=timestamp.desc",
          headers=headers,
          timeout=5,
      )
      if response.status_code == 200:
        data = response.json()
        if data:
          for order in data:
            if order.get("timestamp"):
              try:
                order["timestamp"] = datetime.fromisoformat(
                    order["timestamp"].replace("Z", "+00:00")
                )
              except Exception:
                pass
          return data
    except Exception as e:
      print(f"Supabase fetch orders error: {e}")
  return []


def save_order_to_db(order_data):
  if SUPABASE_URL and SUPABASE_KEY:
    try:
      payload = order_data.copy()
      if isinstance(payload.get("timestamp"), datetime):
        payload["timestamp"] = payload["timestamp"].isoformat()
      headers = {
          "apikey": SUPABASE_KEY,
          "Authorization": f"Bearer {SUPABASE_KEY}",
          "Content-Type": "application/json",
          "Prefer": "return=representation",
      }
      requests.post(
          f"{SUPABASE_URL}/rest/v1/orders",
          json=payload,
          headers=headers,
          timeout=5,
      )
    except Exception as e:
      print(f"Supabase insert order error: {e}")


def update_order_status_in_db(order_id, status):
  if SUPABASE_URL and SUPABASE_KEY:
    try:
      headers = {
          "apikey": SUPABASE_KEY,
          "Authorization": f"Bearer {SUPABASE_KEY}",
          "Content-Type": "application/json",
          "Prefer": "return=representation",
      }
      payload = {
          "status": status,
          "shipped_at": datetime.now().isoformat(),
      }
      requests.patch(
          f"{SUPABASE_URL}/rest/v1/orders?id=eq.{order_id}",
          json=payload,
          headers=headers,
          timeout=5,
      )
    except Exception as e:
      print(f"Supabase update order error: {e}")


# --- HTTPS Email Sender via Brevo REST API ---
def send_email_https(subject, recipient_email, body_text):
  if not BREVO_API_KEY or not STUDIO_EMAIL:
    return False
  url = "https://api.brevo.com/v3/smtp/email"
  headers = {
      "accept": "application/json",
      "api-key": BREVO_API_KEY,
      "content-type": "application/json",
  }
  payload = {
      "sender": {"name": "Leather by Annuschka", "email": STUDIO_EMAIL},
      "to": [{"email": recipient_email}],
      "subject": subject,
      "textContent": body_text,
  }
  response = requests.post(url, json=payload, headers=headers)
  return response.status_code in [200, 201, 202]


# --- Session Inactivity Timeout Hook ---
@app.before_request
def check_session_timeout():
    if session.get("dashboard_logged_in"):
        now = datetime.now()
        last_active_str = session.get("last_active")
        if last_active_str:
            try:
                last_active = datetime.fromisoformat(last_active_str)
                if now - last_active > timedelta(minutes=5):
                    session.clear()
                    flash("Session expired due to inactivity.", "warning")
                    return redirect(url_for("dashboard_login"))
            except Exception:
                pass
        session["last_active"] = now.isoformat()


# --- Background Scheduler Job ---
def generate_summary_email(period_name):
  with app.app_context():
    now = datetime.now()
    orders = get_db_orders()
    if period_name == "Weekly":
      cutoff_date = now - timedelta(days=7)
      recent_orders = [
          o
          for o in orders
          if isinstance(o.get("timestamp"), datetime)
          and o.get("timestamp") >= cutoff_date
      ]
    else:
      first_of_this_month = now.replace(
          day=1, hour=0, minute=0, second=0, microsecond=0
      )
      last_day_of_prev_month = first_of_this_month - timedelta(days=1)
      recent_orders = [
          o
          for o in orders
          if isinstance(o.get("timestamp"), datetime)
          and o.get("timestamp").month == last_day_of_prev_month.month
      ]

    total_orders = len(recent_orders)
    gross_revenue = sum(o.get("sales_excl_transport", 0) for o in recent_orders)
    investor_cut = gross_revenue * 0.10

    subject = f"📊 Studio Performance Report ({period_name})"
    body = (
        f"Hi Annuschka,\n\n{period_name} Summary:\nTotal Orders:"
        f" {total_orders}\nGross Revenue: R {gross_revenue:,.2f}\nInvestor Cut (10%):"
        f" R {investor_cut:,.2f}"
    )
    if STUDIO_EMAIL:
      send_email_https(subject, STUDIO_EMAIL, body)


@scheduler.task("cron", id="weekly_report", day_of_week="fri", hour=8, minute=0)
def weekly_job():
  generate_summary_email("Weekly")


@scheduler.task("cron", id="monthly_report", day=1, hour=8, minute=0)
def monthly_job():
  generate_summary_email("Monthly")


# --- Flask Routes ---
@app.route("/")
def index():
  reviews = get_db_reviews()
  return render_template("index.html", reviews=reviews)


@app.route("/add_review", methods=["POST"])
def add_review():
  name = request.form.get("name", "Anonymous").strip()
  rating = int(request.form.get("rating", 5))
  comment = request.form.get("comment", "").strip()

  if comment:
    new_review = {
        "name": name if name else "Anonymous",
        "rating": rating,
        "comment": comment,
        "created_at": datetime.now().isoformat(),
    }
    if SUPABASE_URL and SUPABASE_KEY:
      try:
        headers = {
            "apikey": SUPABASE_KEY,
            "Authorization": f"Bearer {SUPABASE_KEY}",
            "Content-Type": "application/json",
            "Prefer": "return=representation",
        }
        response = requests.post(
            f"{SUPABASE_URL}/rest/v1/reviews",
            json=new_review,
            headers=headers,
            timeout=5,
        )
        print("Supabase Insert Response:", response.status_code, response.text)
      except Exception as e:
        print(f"CRITICAL Supabase review insert error: {e}")
    else:
      print(
          "Supabase configuration missing. Check your SUPABASE_URL and"
          " SUPABASE_KEY environment variables."
      )

    flash("Thank you! Your review has been submitted successfully.", "success")
  return redirect(url_for("index") + "#reviews")


@app.route("/shop")
def shop():
  category = request.args.get("category", "All")
  search_query = request.args.get("q", "").strip().lower()
  filtered = PRODUCTS
  if category != "All":
    filtered = [p for p in filtered if p["category"] == category]
  if search_query:
    filtered = [
        p
        for p in filtered
        if search_query in p["name"].lower()
        or search_query in p["description"].lower()
    ]
  return render_template(
      "shop.html",
      products=filtered,
      categories=CATEGORIES,
      selected_category=category,
      search_query=search_query,
  )


@app.route("/cart")
def cart():
  cart_items = session.get("cart", [])
  total = sum(item["price"] * item["quantity"] for item in cart_items)
  return render_template("cart.html", cart_items=cart_items, total=total)


@app.route("/add_to_cart/<int:product_id>", methods=["POST"])
def add_to_cart(product_id):
  product = next((p for p in PRODUCTS if p["id"] == product_id), None)
  if product:
    if "cart" not in session:
      session["cart"] = []
    cart = session["cart"]
    color = request.form.get(
        "color", product["colors"][0] if product["colors"] else "Standard"
    )
    size = request.form.get(
        "size", product["sizes"][0] if product["sizes"] else "Standard"
    )
    quantity = int(request.form.get("quantity", 1))
    unit_price = product["price"]
    if "size_prices" in product and size in product["size_prices"]:
      unit_price = product["size_prices"][size]

    existing = next(
        (
            item
            for item in cart
            if item["id"] == product_id
            and item["color"] == color
            and item["size"] == size
        ),
        None,
    )
    if existing:
      existing["quantity"] += quantity
    else:
      cart.append({
          "id": product["id"],
          "name": product["name"],
          "price": unit_price,
          "image": product["images"][0],
          "color": color,
          "size": size,
          "available_colors": product.get("colors", []),
          "available_sizes": product.get("sizes", []),
          "quantity": quantity,
      })
    session["cart"] = cart
    flash(f"Added {product['name']} to cart!", "success")
  return redirect(url_for("cart"))


@app.route("/update_cart/<int:index>", methods=["POST"])
def update_cart(index):
  cart = session.get("cart", [])
  if 0 <= index < len(cart):
    action = request.form.get("action")
    if action == "increase":
      cart[index]["quantity"] += 1
    elif action == "decrease":
      cart[index]["quantity"] -= 1
      if cart[index]["quantity"] <= 0:
        cart.pop(index)
    elif action == "remove":
      cart.pop(index)
    session["cart"] = cart
  return redirect(url_for("cart"))


@app.route("/checkout", methods=["GET", "POST"])
def checkout():
  cart_items = session.get("cart", [])
  if not cart_items:
    flash("Your cart is empty.", "warning")
    return redirect(url_for("shop"))

  subtotal = sum(item["price"] * item["quantity"] for item in cart_items)
  shipping_key = request.form.get("shipping_option", "3-5")
  shipping_info = PEPAXI_OPTIONS.get(shipping_key, PEPAXI_OPTIONS["3-5"])
  total = subtotal + shipping_info["price"]

  if request.method == "POST":
    orders_count = len(get_db_orders())
    order_id = f"ORD-2026-{orders_count + 1:02d}"
    item_summary = ", ".join([
        f"{item['name']} [{item.get('color')}, {item.get('size')}]"
        f" ({item['quantity']})"
        for item in cart_items
    ])
    first_name = request.form.get("first_name", "")
    last_name = request.form.get("last_name", "")
    customer_email = request.form.get("email", "")

    pending_order = {
        "id": order_id,
        "items": item_summary,
        "subtotal": subtotal,
        "transport": shipping_info["price"],
        "sales_excl_transport": subtotal,
        "timestamp": datetime.now(),
        "customer_name": f"{first_name} {last_name}".strip(),
        "customer_email": customer_email,
        "status": "Pending",
    }
    session["pending_order"] = pending_order

    return render_template(
        "payfast_redirect.html",
        payfast_url=PAYFAST_URL,
        merchant_id=PAYFAST_MERCHANT_ID,
        merchant_key=PAYFAST_MERCHANT_KEY,
        return_url=url_for("payment_success", _external=True),
        cancel_url=url_for("cart", _external=True),
        notify_url=url_for("payfast_itn", _external=True),
        m_payment_id=order_id,
        amount=f"{total:.2f}",
        item_name=f"Order #{order_id}",
        name_first=first_name,
        name_last=last_name,
        email_address=customer_email,
        cell_number=request.form.get("phone", ""),
    )

  return render_template(
      "checkout.html",
      cart_items=cart_items,
      subtotal=subtotal,
      shipping=shipping_info["price"],
      total=total,
      paxi_options=PEPAXI_OPTIONS,
  )


@app.route("/payment_success")
def payment_success():
  pending_order = session.pop("pending_order", None)
  if pending_order:
    save_order_to_db(pending_order)
    session.pop("cart", None)
    return render_template(
        "checkout_success.html",
        order_id=pending_order["id"],
        subtotal=pending_order["subtotal"],
    )
  return redirect(url_for("shop"))


@app.route('/payfast/itn', methods=['POST'])
def payfast_itn():
    data = request.form.to_dict()
    
    if data.get('payment_status') == 'COMPLETE':
        order_id = data.get('m_payment_id', 'N/A')
        item_name = data.get('item_name', 'Leather Item')
        amount_str = data.get('amount_gross', '0.00')
        customer_email = data.get('email_address')
        customer_name = f"{data.get('name_first', '')} {data.get('name_last', '')}".strip()
        
        try:
            amount_float = float(amount_str)
        except ValueError:
            amount_float = 0.00

        new_order = {
            "id": order_id,
            "items": item_name,
            "sales_excl_transport": amount_float,
            "investor_cut": round(amount_float * 0.10, 2),
            "timestamp": datetime.now(),
            "customer_name": customer_name or 'Guest Customer',
            "customer_email": customer_email,
            "status": "Pending"
        }

        # Prevent duplicate entries by checking existing orders in Supabase
        existing_orders = get_db_orders()
        if not any(o.get('id') == order_id for o in existing_orders):
            save_order_to_db(new_order)

        body_owner = (
            f"Hi Annuschka,\n\nA new order has been paid successfully!\n\n"
            f"Order ID: {order_id}\n"
            f"Items: {item_name}\n"
            f"Total Paid: R {amount_float:,.2f}\n"
            f"Customer Email: {customer_email}\n\n"
            f"Log into your Studio Dashboard to process shipping."
        )

        body_customer = (
            f"Thank you for supporting local craftsmanship!\n\n"
            f"We've received your payment of R {amount_float:,.2f} for order #{order_id}.\n"
            f"Your item is being prepared with care in our studio."
        )

        try:
            send_email_https(f"New Paid Order #{order_id} - R{amount_float:,.2f}", STUDIO_EMAIL, body_owner)
            if customer_email:
                send_email_https("Order Confirmation - Leather by Annuschka", customer_email, body_customer)
        except Exception as e:
            print(f"ITN Email sending error: {e}")

        return "ITN Processed", 200

    return "Invalid Status", 400

@app.route("/dashboard/login", methods=["GET", "POST"])
def dashboard_login():
  if request.method == "POST":
    if (
        request.form.get("username") == DASHBOARD_USER
        and request.form.get("password") == DASHBOARD_PASS
    ):
      session["dashboard_logged_in"] = True
      session["last_active"] = datetime.now().isoformat()
      return redirect(url_for("dashboard"))
    flash("Invalid credentials.", "error")
  return render_template("dashboard_login.html")


@app.route("/dashboard/logout")
def dashboard_logout():
  session.clear()
  return redirect(url_for("dashboard_login"))


@app.route("/dashboard")
def dashboard():
  if not session.get("dashboard_logged_in"):
    return redirect(url_for("dashboard_login"))

  orders = get_db_orders()
  now = datetime.now()
  weekly_orders = [
      o
      for o in orders
      if isinstance(o.get("timestamp"), datetime)
      and o.get("timestamp") >= now - timedelta(days=7)
  ]
  pending_orders = [o for o in orders if o.get("status") == "Pending"]
  total_sales = sum(o.get("sales_excl_transport", 0) for o in orders)
  investor_cut = total_sales * 0.10

  return render_template(
      "dashboard.html",
      orders=orders,
      weekly_orders=weekly_orders,
      pending_orders=pending_orders,
      total_sales=total_sales,
      investor_cut=investor_cut,
      active_products=len(PRODUCTS),
  )


@app.route("/mark_shipped/<order_id>", methods=["POST"])
def mark_shipped(order_id):
  if not session.get("dashboard_logged_in"):
    return redirect(url_for("dashboard_login"))
  update_order_status_in_db(order_id, "Shipped")
  flash(f"Order #{order_id} marked as shipped.", "success")
  return redirect(url_for("dashboard"))


if __name__ == "__main__":
  app.run(debug=True)