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


@pytest.fixture(scope="function", name="_flag_collection_with_data")
def fixture_prepare_prepopulated_flag_collection():
    """Prepare collection with three flags"""
    db = mongo_container.get_connection_client()[_DATABASE]
    collection = db[_COLLECTION]
    collection.insert_many(
        [
            {
                "challange_id": "firstchallange",
                "task_id": "firsttask",
                "value": Crypto.hash_to_md5("flag{test_1}"),
            },
            {
                "challange_id": "firstchallange",
                "task_id": "secondtask",
                "value": Crypto.hash_to_md5("flag{test_2}"),
            },
            {
                "challange_id": "secondchallange",
                "task_id": "firsttask",
                "value": Crypto.hash_to_md5("flag{test_2_1}"),
            },
        ]
    )
    yield collection
