import os
from dotenv import load_dotenv
from azure.identity import ClientSecretCredential
from azure.storage.blob import BlobServiceClient

# Load environment variables from .env file
load_dotenv()

# Get the values from the environment variables
tenant_id = os.getenv('AZURE_TENANT_ID')
client_id = os.getenv('AZURE_CLIENT_ID')
client_secret = os.getenv('AZURE_CLIENT_SECRET')
storage_account_url = os.getenv('AZURE_STORAGE_ACCOUNT_URL')
container_name = os.getenv('AZURE_CONTAINER_NAME')

credential = ClientSecretCredential(tenant_id, client_id, client_secret)
blob_service_client = BlobServiceClient(account_url=storage_account_url, credential=credential)

# Upload a file
blob_name = "file.csv"
file_path = f"data/{blob_name}"

container_client = blob_service_client.get_container_client(container_name)
blob_client = container_client.get_blob_client(blob_name)

with open(file_path, "rb") as data:
    blob_client.upload_blob(data)

print(f"File {file_path} uploaded to {container_name}/{blob_name}")