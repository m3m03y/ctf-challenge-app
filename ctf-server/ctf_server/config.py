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

azure = {
    "database_id": os.environ.get("COSMOS_DATABASE", "CtfDevelopment"),
    "container_id": os.environ.get("COSMOS_CONTAINER", "Flag"),
}

mongo = {
    "connection_string": os.environ.get(
        "MONGODB_CONNECTION_STRING", "mongodb://<user>:<pass>@localhost:<port>"
    ),
    "database_id": os.environ.get("MONGODB_DATABASE", "CtfLocal"),
    "collection_id": os.environ.get("MONGODB_COLLECTION", "Flag")
}
