import pymongo
from pymongo import MongoClient
from contextlib import contextmanager

class PaymentStore:
    def __init__(self, db_url, db_name, collection_name):
        self.db_url = db_url
        self.db_name = db_name
        self.collection_name = collection_name
    
    @contextmanager
    def _get_collection(self):
        # Use context manager to ensure the client is closed after use
        client = MongoClient(self.db_url)
        try:
            db = client[self.db_name]
            collection = db[self.collection_name]
            yield collection
        finally:
            client.close()
    
    def store_document(self, document):
        try:
            with self._get_collection() as collection:
                # Insert the document and return the inserted ID
                insert_result = collection.insert_one(document)
                return insert_result.inserted_id
        except pymongo.errors.PyMongoError as e:
            # Properly handle exceptions from PyMongo
            raise Exception(f"An error occurred while inserting the payment: {e}")
