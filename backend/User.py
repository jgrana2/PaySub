from appwrite.client import Client
from appwrite.services.users import Users
from appwrite.services.account import Account
from appwrite.services.databases import Databases
from appwrite.id import ID
from appwrite.permission import Permission
from appwrite.role import Role
from dotenv import load_dotenv
from CreditCard import CreditCard
from Security import Security
from Subscription import Subscription
from datetime import datetime, timedelta
from flask import jsonify
import os
import re

class User:
    def __init__(self, email):
        load_dotenv()
        self.client = Client()
        self.client.set_endpoint('https://cloud.appwrite.io/v1')
        self.client.set_project(os.getenv('PROJECT_ID'))
        self.client.set_key(os.getenv('APPWRITE_API_KEY'))
        self.users = Users(self.client)
        self.email = email
        self.user_id = ""
        try:
            self.user_id = self.get_all_users(email)['$id'] 
            print(f"User {email} found with ID: {self.user_id}")
        except Exception as e:
            print(f"The user {email} doesn't exist.")
        try:
            if not self.user_id:
                result = self.register_user(email)
                self.user_id = result['$id']
                print(f"New user {email} with ID:{self.user_id} created")
        except Exception as e:
            return f"An error occurred: {e}"
    
    def get_email(self):
        return self.email
    
    def save_to_collection(self, data, collection):
        try:
            databases = Databases(self.client)
            result = databases.create_document(
                os.getenv('DATABASE_ID'), 
                collection, 
                'unique()', 
                data,  
                permissions=[Permission.read(Role.user(self.user_id)), Permission.write(Role.user(self.user_id))])
            print(f"""Data {data} saved to the database""")
        except Exception as e:
            print(f"An error ocurred: {e}")
    
    def save_subscriber(self, data, collection):
        try:
            databases = Databases(self.client)
            result = databases.create_document(
                os.getenv('DATABASE_ID'), 
                collection, 
                'unique()', 
                data,  
                permissions=[Permission.read(Role.user(self.user_id)), Permission.write(Role.user(self.user_id)), Permission.write(Role.user(data['original_id']))])
            print(f"""Data {data} saved to the database""")
        except Exception as e:
            print(f"An error ocurred: {e}")
    
    def update_to_collection(self, data, collection, document_id):
        try:
            databases = Databases(self.client)
            result = databases.update_document(
                os.getenv('DATABASE_ID'), 
                collection, 
                document_id, 
                data)
            print(f"""Data {data} updated to the database""")
        except Exception as e:
            print(f"An error ocurred: {e}")
        
    def register_user(self, email):
        try:
            result = self.users.create(ID.unique(), email=email)
            return result
        except Exception as e:
            return f"An error occurred: {e}"
        
    def get_all_users(self, email=None):
        try:
            result = self.users.list()
            if email:
                filtered_user = [user for user in result['users'] if user.get('email') == email]
                return filtered_user[0]
            else:
                return result
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_user_by_id(self, id):
        try:
            result = self.users.list()
            if id:
                filtered_user = [user for user in result['users'] if user.get('$id') == id]
                return filtered_user[0]
            else:
                return result
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def get_creator_by_subscription_id(self, subscription_id):
        try:
            temp_subscription = self.get_subscription(subscription_id) # Returns a Subscription object
            creator = self.get_user_by_id(temp_subscription.get_creator_id())
            return creator
        except Exception as e:
            print(f"An error occurred: {e}")

    def add_card(self, card_number, card_holder, expiration, cvc):
        try:
            self.save_to_collection(
                {"card_number": card_number,
                 "card_holder": card_holder,
                 "expiration": expiration,
                 "cvc": cvc}, 
                os.getenv('CARDS_COLLECTION_ID'))
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def list_cards(self):
        try:
            print("Listing all cards:")
            databases = Databases(self.client)
            result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('CARDS_COLLECTION_ID'))
            filtered_documents = [doc for doc in result['documents'] if f'read("user:{self.user_id}")' in doc['$permissions']]
            id_list = [doc['$id'] for doc in filtered_documents]
            print(id_list)
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_card(self, card_id=None):
        print(card_id)
        databases = Databases(self.client)
        result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('CARDS_COLLECTION_ID'))
        
        # Filtering user cards with permissions
        cards_list = [doc for doc in result['documents'] if f'read("user:{self.user_id}")' in doc['$permissions']]
        if card_id:
            # Search for the specified card_id
            for card in cards_list:
                if card['$id'] == card_id:
                    # Decrypt the JSON bytes
                    decrypted_card = self.decrypt_card(card)
                    return decrypted_card
        elif cards_list:
            # No card_id provided, get the first card in the list
            first_card = cards_list[-1]
            decrypted_card = self.decrypt_card(first_card)
            return decrypted_card
    
        # Return None if no cards found or the specified card_id does not exist
        return None
    
    def decrypt_card(self, card):
        load_dotenv()
        hex_key = os.getenv('ENCRYPTION_KEY')
        byte_key = bytes.fromhex(hex_key)
        security = Security(byte_key)
        decrypted_text = security.decryption(card['card_number'])
        new_card = CreditCard(decrypted_text, card['card_holder'], card['expiration'], card['cvc'], card['card_holder_id_number'], card['card_holder_id_type'], card['card_payment_method_id'])
        return new_card
    
    def add_subscription(self, description, price, frequency):
        try:
            self.save_to_collection({"description": description,
                                     "price": price,
                                     "frequency": frequency},
                                    os.getenv('SUBSCRIPTIONS_COLLECTION_ID'))
        except Exception as e:
            print(f"An error occurred: {e}")
    
    def activate_subscription(self, subscription_id):
        try:
            subscription = self.get_subscription(subscription_id)
            card = self.get_card()
            if (not subscription.get_is_enabled()):
                print('The subscription is currently not enabled)')
            else:
                creator = self.get_creator_by_subscription_id(subscription_id) # Returns the creator db user
                creator_user = User(creator['email']) # User object based on the email
                result = card.process_payment(subscription.price, creator_user)
                if (result):
                    # Add to subscribers
                    creator_user.add_subscriber(self, subscription_id) # Add the paying customer (self) to the subscription creator's list of subscribers.
                    current_n_subscribers = subscription.get_n_subscribers()
                    current_income = subscription.get_income()
                    self.update_to_collection({'n_subscribers': current_n_subscribers + 1, 'income': current_income + subscription.price}, os.getenv('SUBSCRIPTIONS_COLLECTION_ID'), subscription_id)
                    return True
        except Exception as e:
            print(f"An error occurred while activating subscription: {e}")
            return False 
            
    def list_subscriptions(self):
        try:
            print("Listing all subscriptions:")
            databases = Databases(self.client)
            result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIPTIONS_COLLECTION_ID'))
            filtered_documents = [doc for doc in result['documents'] if f'read("user:{self.user_id}")' in doc['$permissions']]
            id_list = [doc['$id'] for doc in filtered_documents]
            print(id_list)
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def get_subscription(self, subscription_id):
        databases = Databases(self.client)
        subscriptions_list = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIPTIONS_COLLECTION_ID'))
        
        for subscription in subscriptions_list['documents']:
            matches = re.findall(r'user:([a-f0-9]+)', str(subscription['$permissions']))
            creator_id = matches[0] if matches else None
            if subscription['$id'] == subscription_id:
                new_subscription = Subscription(subscription['$id'], subscription['description'], subscription['price'], subscription['frequency'], creator_id, subscription['is_enabled'], subscription['n_subscribers'], subscription['income'], subscription['title'])
                return new_subscription
        return None
    
    def add_subscriber(self, subscriber, subscription_id):
        try:
            # get_all_users() returns a single user object
            subscriber_data = self.get_all_users(subscriber.email)
            
            # Calculate renewal date
            subscription = self.get_subscription(subscription_id)
            frequency = subscription.get_frequency()
            title = subscription.get_title()
            current_date = datetime.now()

            if frequency == 'weekly' or frequency == 'Semanal':
                renewal_date = current_date + timedelta(weeks=1)
            elif frequency == 'monthly' or frequency == 'Mensual':
                renewal_date = current_date + timedelta(days=30)  # Approximation
            elif frequency == 'yearly' or frequency == 'Anual':
                renewal_date = current_date + timedelta(days=365)  # Approximation
            elif frequency == 'daily' or frequency == 'Diaria':
                renewal_date = current_date + timedelta(days=1)
            elif frequency == 'hourly' or frequency == 'Cada hora':
                renewal_date = current_date + timedelta(hours=1)
            else:
                raise ValueError("Invalid frequency type")

            self.save_subscriber({
                "email": subscriber_data['email'],
                "original_id": subscriber_data['$id'],
                "subscription_id": subscription_id,
                "title": title,
                "subscription_start_date": current_date.isoformat(),
                "renewal_date": renewal_date.isoformat(),  # Convert to ISO format
                "is_active": True},
                os.getenv('SUBSCRIBERS_COLLECTION_ID'))

            print(f"Subscriber {subscriber_data['email']} added to {self.email}'s list.")
        except Exception as e:
            print(f"An error occurred: {e}")
            
    def list_subscribers(self):
        try:
            print("Listing all subscribers:")
            databases = Databases(self.client)
            result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIBERS_COLLECTION_ID'))
            filtered_documents = [doc for doc in result['documents'] if f'read("user:{self.user_id}")' in doc['$permissions']]
            id_list = [doc['$id'] for doc in filtered_documents]
            print(id_list)
        except Exception as e:
            print(f"An error occurred: {e}")

    def get_subscriber(self, subscriber_id):
        databases = Databases(self.client)
        result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIBERS_COLLECTION_ID'))
        subscribers_list = [doc for doc in result['documents'] if f'read("user:{self.user_id}")' in doc['$permissions']]
        for subscriber in subscribers_list:
            if subscriber['$id'] == subscriber_id:
                new_subscriber = self.get_all_users(subscriber['email'])
                return new_subscriber
        return None
    
    def get_access_token(self):
        try:
            databases = Databases(self.client)
            result = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('ACCESS_TOKENS_COLLECTION_ID'))
            filtered_documents = [doc for doc in result['documents'] if f'read("user:{self.user_id}")' in doc['$permissions']]
            access_token = filtered_documents[0]['mp_access_token']
            
            # Decrypt the JSON bytes
            load_dotenv()
            hex_key = os.getenv('ENCRYPTION_KEY')
            byte_key = bytes.fromhex(hex_key)
            security = Security(byte_key)
            decrypted_text = security.decryption(access_token)
            return decrypted_text
        except Exception as e:
            print(f"An error occurred: {e}")