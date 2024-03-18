"""Fixtures preparing mongo db container"""

import pytest
from testcontainers.mongodb import MongoDbContainer

mongo_container = MongoDbContainer(image="mongo:latest")
_database = "CtfLocal"
_collection = "Flag"

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
    db = mongo_container.get_connection_client()[_database]
    collection = db[_collection]
    collection.delete_many({})
    yield collection


@pytest.fixture(scope="function", name="_prepare_flag_collection_with_data")
def fixture_prepare_prepopulated_flag_collection(_prepare_empty_flag_collection):
    """Prepare collection with three flags"""
    db = mongo_container.get_connection_client()[_database]
    collection = db[_collection]
    collection.insert_many(
        [
            {
                "challange_id": "firstchallange",
                "task_id": "firsttask",
                "value": "flag{test_1}",
            },
            {
                "challange_id": "firstchallange",
                "task_id": "secondtask",
                "value": "flag{test_2}",
            },
            {
                "challange_id": "secondchallange",
                "task_id": "firsttask",
                "value": "flag{test_2_1}",
            },
        ]
    )


@pytest.fixture(scope="function", name="connection_url")
def fixture_connection_url():
    """Gets connection url to mongo db container"""
    yield mongo_container.get_connection_url()
