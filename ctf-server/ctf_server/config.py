"""Configuration file"""
import os

azure_connection = {
    "host": os.environ.get(
        "AZURE_ACCOUNT_HOST", "https://project.documents.azure.com:443/"
    ),
    "master_key": os.environ.get(
        "AZURE_ACCOUNT_KEY",
        "account-key",
    ),
}

azure_dev = {
    "database_id": os.environ.get("COSMOS_DATABASE", "CtfDevelopment"),
    "container_id": os.environ.get("COSMOS_CONTAINER", "Flag"),
}

azure_prod = {
    "database_id": os.environ.get("COSMOS_DATABASE", "CtfChallange"),
    "container_id": os.environ.get("COSMOS_CONTAINER", "Flag"),
}

local_mongo = {
    "connection_string": os.environ.get(
        "MONGODB_CONNECTION_STRING", "mongodb://root:pass123@localhost:27017/"
    ),
    "database_id": os.environ.get("MONGODB_DATABASE", "CtfLocal"),
    "collection_id": os.environ.get("MONGODB_COLLECTION", "Flag")
}
