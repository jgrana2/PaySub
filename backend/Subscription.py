from appwrite.services.databases import Databases
from appwrite.client import Client
from appwrite.query import Query
import os
from dotenv import load_dotenv

class Subscription:
    def __init__(self, id=None, description=None, price =None, frequency=None, creator=None, is_enabled=True, subscribers=0, income=0, title=None):
        load_dotenv()
        self.id = id
        self.description = description
        self.price = price
        self.frequency = frequency
        self.is_enabled = is_enabled
        self.creator = creator
        self.subscribers = subscribers
        self.income = income
        self.title = title
    
    def get_id(self):
        return self.id
    
    def get_description(self):
        return self.description

    def display_subscription_details(self):
        print("ID:", self.id)
        print("Description:", self.description)
        print("Price:", self.price)
        print("Frequency:", self.frequency)
        print("Is active:", self.is_enabled)
        print("Creator:", self.creator)

    def get_creator_id(self):
        return self.creator

    def get_frequency(self):
        return self.frequency
    
    def get_title(self):
        return self.title
    
    def get_active_subscriptions(self):
        self.client = Client()
        self.client.set_endpoint('https://cloud.appwrite.io/v1')
        self.client.set_project(os.getenv('PROJECT_ID'))
        self.client.set_key(os.getenv('APPWRITE_API_KEY'))
        databases = Databases(self.client)
        active_subscribers = databases.list_documents(os.getenv('DATABASE_ID'), os.getenv('SUBSCRIBERS_COLLECTION_ID'), [Query.equal("is_active", True), Query.limit(100),])['documents']
        return active_subscribers
    
    def get_is_enabled(self):
        return self.is_enabled
    
    def get_price(self):
        return self.price
    
    def get_n_subscribers(self):
        return self.subscribers
    
    def get_income(self):
        return self.income