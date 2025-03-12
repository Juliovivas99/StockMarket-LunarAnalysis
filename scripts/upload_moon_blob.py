from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Get credentials from .env file
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_BLOB_SAS_URL = os.getenv("AZURE_BLOB_SAS_URL_LUNAR")
AZURE_BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER_LUNAR")
LUNAR_FILE_PATH = "data/lunar_phases.csv"

try:
    if not os.path.exists(LUNAR_FILE_PATH):
        raise FileNotFoundError(f"❌ File {LUNAR_FILE_PATH} not found!")

    print(f"📤 Uploading {LUNAR_FILE_PATH} to {AZURE_BLOB_CONTAINER}...")

    # Connect to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
    blob_client = blob_service_client.get_blob_client(
        container=AZURE_BLOB_CONTAINER, blob=os.path.basename(LUNAR_FILE_PATH)
    )

    with open(LUNAR_FILE_PATH, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)

    print(f"✅ Uploaded {LUNAR_FILE_PATH} to {AZURE_BLOB_CONTAINER}")

except Exception as e:
    print(f"❌ Error uploading lunar data: {e}")
    sys.exit(1)