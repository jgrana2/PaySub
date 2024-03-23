from appwrite.services.databases import Databases
from appwrite.client import Client
from appwrite.query import Query
from flask import Flask, request, redirect
import os
from dotenv import load_dotenv
from flask import jsonify
from flask_cors import CORS
from Security import Security
from User import User
from flask_cors import cross_origin

app = Flask(__name__)
CORS(app, origins=["https://paysub.app", "https://www.paysub.app"])

def check_subscription(subscription_id):
    load_dotenv()
    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')
    client.set_project(os.getenv('PROJECT_ID'))
    client.set_key(os.getenv('APPWRITE_API_KEY'))
    databases = Databases(client)
    try:
        result = databases.get_document(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIPTIONS_COLLECTION_ID'), subscription_id)
        # print(result)
        return result
    except Exception as e:
        return False

def display_subscription_page(subscription):
    svelte_subscription_url = f"http://localhost:5173/subscription/{subscription['$id']}"
    return redirect(svelte_subscription_url)

@app.route('/subscription/<subscription_id>', methods=['GET'])
@cross_origin()
def get_subscription(subscription_id):
    try:
        subscription = check_subscription(subscription_id)
        permission = subscription['$permissions'][0] # Just the the first one (read permission), all permissions have the same user
        start = permission.find('user:') + len('user:')
        end = permission.find('")', start)
        subscription_creator = permission[start:end]
    except Exception as e:
        print(f"An error ocurred: {e}")

    if subscription:
        subscription_data = {
            'id': subscription['$id'],
            'title': subscription['title'],
            'subtitle': subscription['subtitle'],
            'description': subscription.get('description', ''),
            'long_description': subscription.get('long_description', ''),
            'frequency': subscription.get('frequency', ''),
            'is_enabled': subscription.get('is_enabled'),
            'price': subscription.get('price', 0),
            'creator': subscription_creator,
            'image_file_id': subscription.get('image_file_id'),
            'image_bucket_id': subscription.get('image_bucket_id'),
            'subscribers': subscription.get('subscribers')
        }
        return jsonify(subscription_data)
    else:
        return jsonify({'error': f"Subscription with ID {subscription_id} was not found."}), 404

@app.route('/active_subscriptions/<user_email>', methods=['GET'])
@cross_origin()
def get_active_subscriptions(user_email):
    load_dotenv()
    client = Client()
    client.set_endpoint('https://cloud.appwrite.io/v1')
    client.set_project(os.getenv('PROJECT_ID'))
    client.set_key(os.getenv('APPWRITE_API_KEY'))
    databases = Databases(client)
    try:
        result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIBERS_COLLECTION_ID'), [Query.equal("email", user_email)])['documents']
        return jsonify(result)
    except Exception as e:
        print(f"An error ocurred: {e}")

@app.route('/subscribe', methods=['GET'])
@cross_origin()
def subscribe():
    # Fetch the subscription ID from the GET request's query parameters
    subscription_id = request.args.get('subscription_id')
    
    if not subscription_id:
        return "Missing subscription ID", 400
        
    # Do something with the subscription ID.
    print(f"Received subscription ID: {subscription_id}")
    
    # Check if the subscription exists
    subscription = check_subscription(subscription_id)
    if subscription:
        return display_subscription_page(subscription)
    else:
        return f"Subscription ID {subscription_id} doesn't exist", 400
    
    return f"Subscription ID {subscription_id} received", 200

# Placeholder function to get the current logged in user's default credit card
def get_default_credit_card(temp_user):
    # Replace with actual implementation
    temp_user.get_card().display_card_info()
    return "1234-5678-9101-1121"

@app.route('/activate-subscription', methods=['POST'])
@cross_origin()
def activate_subscription_route():
    
    # Get the user's email
    if not request.json or 'user_email' not in request.json:
        return jsonify({"error": "User is not logged in"}), 401
    user_email = request.json['user_email']

    # Create a new temporary user object with the logged in user email to connect to the database
    user = User(user_email)
    
    # Get subscription ID from the POST data
    if not request.json or 'subscription_id' not in request.json:
        return jsonify({"error": "Subscription ID is required"}), 400
    subscription_id = request.json['subscription_id']

    # Activate the subscription with the given subscription ID
    if user.activate_subscription(subscription_id):
        return jsonify({"message": "Subscription activated successfully"}), 200
    else:
        return jsonify({"error": "Failed to activate subscription"}), 500

@app.route('/cards', methods=['GET'])
@cross_origin()
def get_user_cards():
    # Get user_id from query parameters
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'Missing user_id query parameter'}), 400
    
    try:
        # Function `get_user_cards_from_db` should be implemented to interact with the database
        temp_user = User("test@example.com")
        
        actualUser = User(temp_user.get_user_by_id(user_id)['email']);

        card = actualUser.get_card()

        # Check if the card is None, which signifies there's no card available.
        if card is None:
            return jsonify({'hasCards': 'false'}), 200  # Assuming you want to return 200 even if there's no card
        else:
            # Return positive response if the card exists
            return jsonify({'hasCards': 'true'}), 200
    except Exception as e:
        # Log exception details here
        print(e)
        return jsonify({'error': 'There was an error processing your request'}), 500

@app.route('/encrypt', methods=['POST'])
@cross_origin()
def encrypt_data():
    # Get payload
    if not request.json or 'payload' not in request.json:
        return jsonify({"error": "No payload"}), 401
    payload = request.json['payload']

    # Encrypt the JSON bytes
    load_dotenv()
    hex_key = os.getenv('ENCRYPTION_KEY')
    byte_key = bytes.fromhex(hex_key)
    security = Security(byte_key)
    encrypted_text = security.encryption(payload)
    
    # Return the encrypted data
    return jsonify({"encrypted_data": encrypted_text})

@app.route('/decrypt', methods=['POST'])
@cross_origin()
def decrypt_data():
    # Get payload
    if not request.json or 'payload' not in request.json:
        return jsonify({"error": "No payload"}), 401
    payload = request.json['payload']

    # Decrypt the JSON bytes
    load_dotenv()
    hex_key = os.getenv('ENCRYPTION_KEY')
    byte_key = bytes.fromhex(hex_key)
    security = Security(byte_key)
    decrypted_text = security.decryption(payload)
    
    # Return the decrypted data
    return jsonify({"decrypted_data": decrypted_text})

if __name__ == '__main__':
    app.run(debug=True)
