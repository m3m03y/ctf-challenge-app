import os

local_settings = {}

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
