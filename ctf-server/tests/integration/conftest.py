"""Fixtures preparing mongo db container"""
import pytest
from testcontainers.mongodb import MongoDbContainer

mongo_container = MongoDbContainer(image="mongo:latest")


@pytest.fixture(scope="class")
def setup_mongo_container(request):
    """Creates mongo db container for tests and remove it at the end"""
    mongo_container.start()

    def remove_container():
        mongo_container.stop()

    request.addfinalizer(remove_container)


@pytest.fixture(scope="function")
def prepare_flag_collection(setup_mongo_container):
    """Clears flag collection"""
    db = mongo_container.get_connection_client()["Test"]
    collection = db["Flag"]
    collection.delete_many({})


@pytest.fixture(scope="function")
def connection_url():
    """Gets connection url to mongo db container"""
    yield mongo_container.get_connection_url()
