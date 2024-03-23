# Import the necessary libraries
from appwrite.client import Client
from appwrite.services.storage import Storage
from dotenv import load_dotenv
import os

# Initialize the Appwrite client
load_dotenv()
client = Client()
client.set_endpoint('https://cloud.appwrite.io/v1')
client.set_project(os.getenv('PROJECT_ID'))
client.set_key(os.getenv('APPWRITE_API_KEY'))

# Initialize the Storage service
storage = Storage(client)

# Get a list of all files in the bucket
files = storage.list_files(os.getenv('IMAGES_BUCKET_ID')) 

# Delete each file in the bucket
for file in files['files']:
    storage.delete_file(os.getenv('IMAGES_BUCKET_ID'), file['$id'])
    print(f"File {file['$id']} deleted")

print("All files in the bucket have been deleted successfully.")