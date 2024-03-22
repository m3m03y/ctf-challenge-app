"""Fixtures preparing mongo db container"""

import pytest
from testcontainers.mongodb import MongoDbContainer
from ctf_server.core.crypto import Crypto

mongo_container = MongoDbContainer(image="mongo:latest")
_DATABASE = "CtfLocal"
_COLLECTION = "Flag"

@pytest.fixture(scope="class", name="setup_mongo_container", autouse=True)
def fixture_setup_mongo_container(request):
    """Creates mongo db container for tests and remove it at the end"""
    mongo_container.start()

    def remove_container():
        mongo_container.stop()

    request.addfinalizer(remove_container)


@pytest.fixture(scope="function", name="empty_flag_collection")
def fixture_prepare_empty_flag_collection():
    """Clears flag collection"""
    db = mongo_container.get_connection_client()[_DATABASE]
    collection = db[_COLLECTION]
    collection.delete_many({})
    yield collection


@pytest.fixture(scope="function", name="flag_collection_with_data")
def fixture_prepare_prepopulated_flag_collection(empty_flag_collection):
    """Prepare collection with three flags"""
    collection = empty_flag_collection
    collection.insert_many(
        [
            {
                "challenge_id": "firstchallenge",
                "task_id": "firsttask",
                "value": Crypto.hash_to_md5("flag{test_1}"),
            },
            {
                "challenge_id": "firstchallenge",
                "task_id": "secondtask",
                "value": Crypto.hash_to_md5("flag{test_2}"),
            },
            {
                "challenge_id": "secondchallenge",
                "task_id": "firsttask",
                "value": Crypto.hash_to_md5("flag{test_2_1}"),
            },
        ]
    )
    yield collection

@pytest.fixture(scope="function", name="connection_url")
def fixture_connection_url():
    """Gets connection url to mongo db container"""
    yield mongo_container.get_connection_url()
