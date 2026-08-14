from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/shop')
def shop():
    return render_template('shop.html')

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/calculate', methods=['POST'])
def calculate():
    data = request.json
    items = data.get('items', [])
    
    # Calculate raw subtotal / total order value
    subtotal = sum(item['price'] * item['quantity'] for item in items)
    
    # Calculate Jan's 10% fee (cut/commission)
    jans_fee = subtotal * 0.10
    total = subtotal  # Customer pays the full subtotal
    
    return jsonify({
        'subtotal': round(subtotal, 2),
        'jans_fee': round(jans_fee, 2),
        'total': round(total, 2)
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)