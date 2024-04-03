from flask import Flask, send_from_directory, request, jsonify, flash, session, render_template, redirect, url_for
import os
import hashlib
from functools import wraps
import mysql.connector
from mysql.connector import Error
from flask import make_response
from flask import session


# Importing backend functionalities
from backend.manage_emd import generate_emd
from backend.SmartWalletSender import SmartWalletSender
from backend.SmartWalletSender import get_logged_in_user_wallet_id
from backend.SmartWalletReceiver import SmartWalletReceiver
from backend.view_balence import get_balance_data
from backend.register import register_user
from backend.login import login_user


app = Flask(__name__, template_folder='templates')

# Generate and set the secret key
random_bytes = os.urandom(24)
hashed_bytes = hashlib.sha256(random_bytes).digest()
app.secret_key = hashed_bytes.hex()

# Decorator to check if the user is logged in
def login_required(view):
    @wraps(view)
    def wrapped_view(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return view(*args, **kwargs)
    return wrapped_view

def check_if_user_is_logged_in():
    """Check if the user_id is stored in the session."""
    return 'user_id' in session

# Serve HTML pages
@app.route('/')
def index():
    user_links = check_if_user_is_logged_in()  # Check if the user is logged in
    user_id = session.get('user_id') if user_links else None  # Get the user_id from session if logged in
    return render_template('index.html', user_links=user_links, user_id=user_id)


@app.route('/emd')
@login_required
def edm_page():
    return send_from_directory(os.path.join('static', 'frontend'), 'emd.html')

@app.route('/sender')
@login_required
def sender_page():
    return send_from_directory(os.path.join('static', 'frontend'), 'sender.html')

@app.route('/receiver')
@login_required
def receiver_page():
    return send_from_directory(os.path.join('static', 'frontend'), 'receiver.html')

from flask import redirect, url_for, session, request, flash

@app.route('/login', methods=['GET', 'POST'])
def login():
    # Check if user is already logged in
    if 'user_id' in session:
        # If the user is already logged in, clear the session and redirect to the login page or homepage
        session.pop('user_id', None)
        app.logger.info("User was already logged in. Session cleared.")
        flash('You were logged out because you navigated back to the login page.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        user_id = request.form['user_id']
        password = request.form['password']

        # Assuming login_user returns a tuple (success, message)
        success, message = login_user(user_id, password)

        if success:
            session['user_id'] = user_id  # Set the user_id in the session
            app.logger.info(f"User {user_id} logged in successfully.")
            return redirect(url_for('index'))  # Redirect to the index page after successful login
        else:
            app.logger.warning(f"Login failed for user {user_id}. Reason: {message}")
            flash(f"Login failed. {message}")  # You might want to handle this more gracefully
            return redirect(url_for('login'))

    else:
        return render_template('login.html')
    

@app.route('/register', methods=['GET', 'POST'])
def register():
    # Placeholder for your registration logic
    if request.method == 'POST':
        # Example of handling a form submission
        user_id = request.form.get('user_id')
        password = request.form.get('password')
        
        # Placeholder for calling your register_user function
        # Example: message, success = register_user(user_id, password)
        # For demonstration, let's assume registration is always successful
        flash("Registration successful. Please login.")
        return register_user(user_id, password)
    
    # Render the registration template if method is GET or registration fails
    return render_template('register.html')

@app.route('/logout')
def logout():
    # Remove user_id from session to log the user out
    session.pop('user_id', None)
    # You can also use session.clear() to remove everything from the session
    # Redirect to the login page or the homepage after logout
    return redirect(url_for('login'))


# Backend routes

@app.route('/generate_emd', methods=['POST'])
@login_required
def generate_emd_route():
    # Extract student_id and amount from the request
    student_id = request.form.get('studentId')
    amount = request.form.get('amount')

    # Check if both student_id and amount are provided
    if not student_id or not amount:
        return jsonify({"error": "Student ID and amount are required parameters."}), 400

    # Call the generate_emd function with the extracted parameters
    return generate_emd(student_id, amount)


# Route to serve the sender.html file
@app.route('/sender')
@login_required
def sender():
    return send_from_directory(os.path.join('static', 'frontend'), 'sender.html')

# Route to handle the form submission from the sender.html file
@app.route('/send_funds', methods=['POST'])
@login_required
def send_funds():
    receiver_id = request.form['receiver_id']
    amount = request.form['amount']
    sender_id = get_logged_in_user_wallet_id()
    
    if sender_id is None:
        return jsonify({'error': 'User ID not found in session. Please log in.'}), 400
        
    sender = SmartWalletSender(sender_id, receiver_id, amount)
    token = sender.send_funds()
    return jsonify({'token': token})

@app.route('/receiver')
@login_required
def receiver():
    return send_from_directory(os.path.join('static', 'frontend'), 'receiver.html')


@app.route('/receive_funds', methods=['POST'])
def receive_funds():
    wallet_receiver_id = request.form['walletReceiverId']
    received_token = request.form['receivedToken']
    wallet_receiver = SmartWalletReceiver(wallet_receiver_id)
    result = wallet_receiver.receive_funds(received_token)
    return result

@app.route('/view_balance')
@login_required
def view_balance():
    return send_from_directory(os.path.join('static', 'frontend'), 'view_balance.html')

@app.route('/get_balance_data')
@login_required
def get_balance_data_route():
    balance_data = get_balance_data()
    return jsonify(balance_data)

@app.route('/check_session')
def check_session():
    # Print the entire session
    print(session)

    # Access specific keys in the session
    user_id = session.get('user_id')
    print("User ID:", user_id)

    # You can print more session data as needed

    return "Session checked. Check the console for session details."

if __name__ == '__main__':
    app.run(debug=True)

