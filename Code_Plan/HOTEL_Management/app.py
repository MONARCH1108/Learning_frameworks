from flask import Flask, render_template, request, jsonify, session
import os
import logging
from datetime import datetime
import json
from logging.handlers import RotatingFileHandler
import uuid

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

# Set up file handler with rotation
file_handler = RotatingFileHandler('logs/restaurant.log', maxBytes=10240000, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)

# Set up console handler
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s'
))
console_handler.setLevel(logging.INFO)

# Configure app logger
app.logger.addHandler(file_handler)
app.logger.addHandler(console_handler)
app.logger.setLevel(logging.INFO)

# Create orders log file for billing records
orders_logger = logging.getLogger('orders')
orders_handler = RotatingFileHandler('logs/orders.log', maxBytes=10240000, backupCount=10)
orders_handler.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
orders_logger.addHandler(orders_handler)
orders_logger.setLevel(logging.INFO)

app.logger.info('Restaurant Ordering System started')

dishes = [
    {"name": "Burger", "price": "$8.99"},
    {"name": "Pizza", "price": "$12.49"},
    {"name": "Chicken Wings", "price": "$10.99"},
    {"name": "Fish Fry", "price": "$14.99"},
    {"name": "Steak Dinner", "price": "$24.99"},
    {"name": "Salad", "price": "$6.49"},
    {"name": "Sandwich", "price": "$7.49"},
    {"name": "Soup", "price": "$4.99"},
    {"name": "Fries", "price": "$2.99"},
    {"name": "Breadsticks", "price": "$3.99"},
    {"name": "Milkshake", "price": "$5.49"},
    {"name": "Ice Cream", "price": "$4.99"},
    {"name": "Waffles", "price": "$8.49"},
    {"name": "Eggs Benedict", "price": "$9.99"},
    {"name": "Breakfast Burrito", "price": "$6.99"},
    {"name": "Chicken Quesadilla", "price": "$7.99"},
    {"name": "Grilled Cheese", "price": "$5.49"},
    {"name": "Falafel Wrap", "price": "$6.99"},
    {"name": "Tacos", "price": "$8.49"}
]

def get_session_id():
    """Get or create a unique session ID"""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def calculate_taxes_and_fees(subtotal):
    """Calculate tax and service fee"""
    tax_rate = 0.08  # 8% tax
    service_fee_rate = 0.03  # 3% service fee
    
    tax = subtotal * tax_rate
    service_fee = subtotal * service_fee_rate
    
    return tax, service_fee

@app.route('/')
def index():
    session_id = get_session_id()
    
    # Initialize session variables if they don't exist
    if 'total_order_list' not in session:
        session['total_order_list'] = []
    if 'bill' not in session:
        session['bill'] = 0.0
    
    app.logger.info(f'Session {session_id}: Accessed main page')
    return render_template('index.html', dishes=dishes)

@app.route('/add_order', methods=['POST'])
def add_order():
    session_id = get_session_id()
    order_name = request.json.get('order', '').strip()
    
    if not order_name:
        app.logger.warning(f'Session {session_id}: Empty order attempted')
        return jsonify({'success': False, 'message': 'Please enter a dish name'})
    
    # Initialize session variables if they don't exist
    if 'total_order_list' not in session:
        session['total_order_list'] = []
    if 'bill' not in session:
        session['bill'] = 0.0
    
    # Find the dish
    found_dish = None
    for dish in dishes:
        if order_name.lower() == dish["name"].lower():
            found_dish = dish
            break
    
    if found_dish:
        price = float(found_dish["price"].replace("$", ""))
        
        # Add to order list
        order_list = session['total_order_list']
        order_item = {
            'name': found_dish["name"], 
            'price': price,
            'timestamp': datetime.now().isoformat()
        }
        order_list.append(order_item)
        session['total_order_list'] = order_list
        
        # Update bill
        session['bill'] = session['bill'] + price
        
        app.logger.info(f'Session {session_id}: Added {found_dish["name"]} (${price:.2f}) to order')
        
        return jsonify({
            'success': True,
            'message': f'{found_dish["name"]} added to order!',
            'order_list': session['total_order_list'],
            'total_bill': round(session['bill'], 2)
        })
    else:
        app.logger.warning(f'Session {session_id}: Dish "{order_name}" not found')
        return jsonify({
            'success': False,
            'message': f'"{order_name}" not found on menu'
        })

@app.route('/remove_item', methods=['POST'])
def remove_item():
    session_id = get_session_id()
    item_index = request.json.get('index')
    
    if 'total_order_list' not in session or item_index is None:
        return jsonify({'success': False, 'message': 'Invalid request'})
    
    order_list = session['total_order_list']
    
    if 0 <= item_index < len(order_list):
        removed_item = order_list.pop(item_index)
        session['total_order_list'] = order_list
        session['bill'] = session['bill'] - removed_item['price']
        
        app.logger.info(f'Session {session_id}: Removed {removed_item["name"]} from order')
        
        return jsonify({
            'success': True,
            'message': f'{removed_item["name"]} removed from order',
            'order_list': session['total_order_list'],
            'total_bill': round(session['bill'], 2)
        })
    else:
        return jsonify({'success': False, 'message': 'Item not found'})

@app.route('/clear_order', methods=['POST'])
def clear_order():
    session_id = get_session_id()
    items_count = len(session.get('total_order_list', []))
    
    session['total_order_list'] = []
    session['bill'] = 0.0
    
    app.logger.info(f'Session {session_id}: Cleared order with {items_count} items')
    
    return jsonify({
        'success': True,
        'message': 'Order cleared!',
        'order_list': [],
        'total_bill': 0.0
    })

@app.route('/get_order', methods=['GET'])
def get_order():
    return jsonify({
        'order_list': session.get('total_order_list', []),
        'total_bill': round(session.get('bill', 0.0), 2)
    })

@app.route('/finalize_order', methods=['POST'])
def finalize_order():
    session_id = get_session_id()
    customer_info = request.json
    
    if not session.get('total_order_list'):
        return jsonify({'success': False, 'message': 'No items in order'})
    
    # Calculate billing details
    subtotal = session['bill']
    tax, service_fee = calculate_taxes_and_fees(subtotal)
    total = subtotal + tax + service_fee
    
    # Generate order ID
    order_id = f"ORD-{datetime.now().strftime('%Y%m%d')}-{str(uuid.uuid4())[:8].upper()}"
    
    # Create final bill
    final_bill = {
        'order_id': order_id,
        'session_id': session_id,
        'timestamp': datetime.now().isoformat(),
        'customer_info': customer_info,
        'items': session['total_order_list'],
        'subtotal': round(subtotal, 2),
        'tax': round(tax, 2),
        'service_fee': round(service_fee, 2),
        'total': round(total, 2),
        'payment_status': 'completed'
    }
    
    # Log the order
    orders_logger.info(json.dumps(final_bill))
    app.logger.info(f'Session {session_id}: Order finalized - {order_id} - Total: ${total:.2f}')
    
    # Clear session
    session['total_order_list'] = []
    session['bill'] = 0.0
    
    return jsonify({
        'success': True,
        'message': 'Order completed successfully!',
        'bill': final_bill
    })

@app.route('/receipt/<order_id>')
def receipt(order_id):
    """Display receipt page"""
    return render_template('receipt.html', order_id=order_id)

@app.route('/admin/logs')
def view_logs():
    """Simple admin interface to view recent logs"""
    try:
        with open('logs/restaurant.log', 'r') as f:
            logs = f.readlines()[-100:]  # Last 100 lines
        
        with open('logs/orders.log', 'r') as f:
            orders = f.readlines()[-50:]  # Last 50 orders
        
        return render_template('admin.html', logs=logs, orders=orders)
    except FileNotFoundError:
        return "Log files not found", 404

@app.route('/admin/analytics')
def analytics():
    """Basic analytics from order logs"""
    try:
        analytics_data = {
            'total_orders': 0,
            'total_revenue': 0,
            'popular_items': {},
            'daily_orders': {}
        }
        
        with open('logs/orders.log', 'r') as f:
            for line in f:
                try:
                    # Extract JSON part from log line
                    json_start = line.find('{')
                    if json_start != -1:
                        order_data = json.loads(line[json_start:])
                        
                        analytics_data['total_orders'] += 1
                        analytics_data['total_revenue'] += order_data['total']
                        
                        # Track popular items
                        for item in order_data['items']:
                            item_name = item['name']
                            analytics_data['popular_items'][item_name] = analytics_data['popular_items'].get(item_name, 0) + 1
                        
                        # Track daily orders
                        order_date = order_data['timestamp'][:10]
                        analytics_data['daily_orders'][order_date] = analytics_data['daily_orders'].get(order_date, 0) + 1
                        
                except json.JSONDecodeError:
                    continue
        
        return jsonify(analytics_data)
    except FileNotFoundError:
        return jsonify({'error': 'No order data found'})

if __name__ == '__main__':
    app.run(debug=True)