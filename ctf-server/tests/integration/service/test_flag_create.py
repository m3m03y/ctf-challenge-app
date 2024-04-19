"""Test flag management service module - create flag part"""

from ctf_server.core.crypto import Crypto
from ctf_server.model.flag import Flag
from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.db.mongodb_proxy import MongodbProxy
from ctf_server.service.flag_service import FlagService


class TestFlagCreate:
    """Tests create flag function"""

    def test_valid_flag_should_be_created_and_contain_hashed_value(
        self, empty_flag_collection, connection_url
    ):
        """Test valid flag created successfully"""
        initial_size = len(list(empty_flag_collection.find()))
        assert initial_size == 0
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(
            value="flag{test}",
            task_id="firsttask",
            challenge_id="firstchallenge",
            task_nr=1,
        )
        created_flag = flag_service.create_flag(flag)
        assert created_flag is not None
        assert created_flag.challenge_id == flag.challenge_id
        assert created_flag.task_id == flag.task_id
        assert created_flag.value == Crypto.hash_to_md5(flag.value)
        assert created_flag.task_nr == 1

        insert_size = len(list(empty_flag_collection.find()))
        assert insert_size == 1

    def test_invalid_flag_should_not_be_created(
        self, empty_flag_collection, connection_url
    ):
        """Test invalid flag must not be created"""
        initial_size = len(list(empty_flag_collection.find()))
        assert initial_size == 0
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(
            value="flag{INVALID-NAME}",
            task_id="firsttask",
            challenge_id="firstchallenge",
            task_nr=1,
        )
        created_flag = flag_service.create_flag(flag)
        assert created_flag is None

        insert_size = len(list(empty_flag_collection.find()))
        assert insert_size == 0

    def test_empty_flag_should_not_be_created(
        self, empty_flag_collection, connection_url
    ):
        """Test empty flag must not be created"""
        initial_size = len(list(empty_flag_collection.find()))
        assert initial_size == 0
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(value="", challenge_id="test", task_id="test", task_nr=1)
        created_flag = flag_service.create_flag(flag)
        assert created_flag is None

        insert_size = len(list(empty_flag_collection.find()))
        assert insert_size == 0

    def test_flag_should_not_be_created_if_already_exists_per_challenge_and_task(
        self, empty_flag_collection, connection_url
    ):
        """Test create flag with existing task and challenge ids combination should fail"""
        flag = Flag(
            value="flag{test}",
            task_id="firsttask",
            challenge_id="firstchallenge",
            task_nr=1,
        )

        empty_flag_collection.insert_one(
            {
                "challenge_id": flag.challenge_id,
                "task_id": flag.task_id,
                "value": flag.value,
                "task_nr": flag.task_nr,
            }
        )
        initial_size = len(list(empty_flag_collection.find()))
        assert initial_size == 1
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        created_flag = flag_service.create_flag(flag)
        assert created_flag is None

        insert_size = len(list(empty_flag_collection.find()))
        assert insert_size == 1
