import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# Get the values from the environment variables
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
storage_account_url = os.getenv('AZURE_STORAGE_ACCOUNT_URL')
container_name = os.getenv('AZURE_CONTAINER_NAME')

# Authenticate using the service principal
credential = ClientSecretCredential(tenant_id, client_id, client_secret)
blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=credential)

# Get the container client
container_client = blob_service_client.get_container_client(container_name)

# List all blobs in the container
print(f"Listing blobs in container '{container_name}':")
try:
    blobs_list = container_client.list_blobs()
    for blob in blobs_list:
        # Get blob properties
        blob_client = container_client.get_blob_client(blob)
        blob_properties = blob_client.get_blob_properties()

        # Extract size and last modified date
        blob_size = blob_properties.size
        last_modified = blob_properties.last_modified.strftime('%Y-%m-%d %H:%M:%S')

        print(f"Blob name: {blob.name}")
        print(f"  Size: {blob_size} bytes")
        print(f"  Last Modified: {last_modified}")
except Exception as e:
    print(f"An error occurred: {e}")