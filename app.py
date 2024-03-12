from flask import Flask, send_from_directory, request, jsonify
import os

# Importing backend functionalities
from backend.manage_emd import generate_emd
from backend.SmartWalletSender import SmartWalletSender
from backend.SmartWalletReceiver import SmartWalletReceiver
from backend.view_balence import get_balance_data

app = Flask(__name__)

# Serve HTML pages
@app.route('/')
def index():
    return send_from_directory(os.path.join('static', 'frontend'), 'index.html')

@app.route('/emd')
def edm_page():
    return send_from_directory(os.path.join('static', 'frontend'), 'emd.html')

@app.route('/sender')
def sender_page():
    return send_from_directory(os.path.join('static', 'frontend'), 'sender.html')

@app.route('/receiver')
def receiver_page():
    return send_from_directory(os.path.join('static', 'frontend'), 'receiver.html')

# Backend routes

@app.route('/generate_emd', methods=['POST'])
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
def sender():
    return send_from_directory(os.path.join('static', 'frontend'), 'sender.html')

# Route to handle the form submission from the sender.html file
@app.route('/send_funds', methods=['POST'])
def send_funds():
    data = request.form
    wallet_id = int(data['wallet_id'])
    receiver_id = int(data['receiver_id'])
    amount = int(data['amount'])
    sender = SmartWalletSender(wallet_id)
    token = sender.send_funds(receiver_id, amount)
    return jsonify({'token': token})

@app.route('/receiver')
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
def view_balance():
    return send_from_directory(os.path.join('static', 'frontend'), 'view_balance.html')

@app.route('/get_balance_data')
def get_balance_data_route():
    balance_data = get_balance_data()
    return jsonify(balance_data)


if __name__ == '__main__':
    app.run(debug=True)

