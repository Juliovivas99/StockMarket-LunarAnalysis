from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv
import os
import sys

# Load environment variables
load_dotenv()

# Get credentials from .env file
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
AZURE_BLOB_SAS_URL = os.getenv("AZURE_BLOB_SAS_URL_STOCK")
AZURE_BLOB_CONTAINER = os.getenv("AZURE_BLOB_CONTAINER_STOCK")
LATEST_FILES_PATH = "latest_files.txt"

try:
    # Read all stock data file paths
    with open(LATEST_FILES_PATH, "r") as f:
        FILE_PATHS = [line.strip() for line in f.readlines()]

    if not FILE_PATHS:
        raise FileNotFoundError("❌ No stock files found!")

    # Connect to Azure Blob Storage
    blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

    for file_path in FILE_PATHS:
        if not os.path.exists(file_path):
            print(f"⚠️ Skipping missing file: {file_path}")
            continue

        print(f"📤 Uploading {file_path} to {AZURE_BLOB_CONTAINER}...")

        blob_client = blob_service_client.get_blob_client(
            container=AZURE_BLOB_CONTAINER, blob=os.path.basename(file_path)
        )

        with open(file_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)

        print(f"✅ Uploaded {file_path} to {AZURE_BLOB_CONTAINER}")

    print("🎉 All stock files uploaded successfully!")

except Exception as e:
    print(f"❌ Error uploading stock data: {e}")
    sys.exit(1)