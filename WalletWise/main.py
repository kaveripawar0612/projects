from flask import Flask, render_template, request, redirect, url_for, flash
from flask_socketio import SocketIO, emit
from datetime import datetime
import logging
import os

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET", "dev_key")

# Initialize SocketIO
socketio = SocketIO(app)

PAYMENT_METHODS = {
    'googlepay': {'name': 'Google Pay', 'icon': 'fa-google-pay'},
    'cash': {'name': 'Cash', 'icon': 'fa-money-bill'},
    'card': {'name': 'Card', 'icon': 'fa-credit-card'},
    'bank': {'name': 'Bank Transfer', 'icon': 'fa-university'},
    'other': {'name': 'Other', 'icon': 'fa-circle-dollar'}
}

@app.route('/')
def index():
    return render_template('index.html',
                         payment_methods=PAYMENT_METHODS)

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    try:
        amount = float(request.form['amount'])
        description = request.form['description']
        payment_method = request.form['payment_method']

        if amount <= 0:
            flash('Amount must be greater than 0', 'error')
            return redirect(url_for('index'))

        transaction = {
            'amount': amount,
            'description': description,
            'payment_method': payment_method,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M'),
            'payment_method_icon': PAYMENT_METHODS[payment_method]['icon'],
            'payment_method_name': PAYMENT_METHODS[payment_method]['name']
        }

        # Emit the transaction data
        socketio.emit('transaction_added', transaction)
        flash('Transaction added successfully', 'success')
    except ValueError:
        flash('Invalid amount', 'error')
    return redirect(url_for('index'))

@app.route('/set_budget', methods=['POST'])
def set_budget():
    try:
        budget = float(request.form['budget'])
        if budget < 0:
            flash('Budget cannot be negative', 'error')
        else:
            # Emit the budget data
            socketio.emit('budget_updated', {'budget': budget})
            flash('Budget updated successfully', 'success')
    except ValueError:
        flash('Invalid budget amount', 'error')
    return redirect(url_for('index'))

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)