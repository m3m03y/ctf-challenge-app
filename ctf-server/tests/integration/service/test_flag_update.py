"""Test flag management service module - update flag part"""

from ctf_server.core.crypto import Crypto
from ctf_server.model.flag import Flag
from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.db.mongodb_proxy import MongodbProxy
from ctf_server.service.flag_service import FlagService


class TestFlagUpdate:
    """Tests flag service update functions"""

    def test_valid_flag_should_be_updated_and_contain_new_hashed_value(
        self, flag_collection_with_data, connection_url
    ):
        """Test flag update"""
        initial_size = len(list(flag_collection_with_data.find()))
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(
            value="flag{test_updated_name}",
            task_id="firsttask",
            challenge_id="firstchallenge",
        )
        updated_flag = flag_service.update_flag(flag)
        assert updated_flag.challenge_id == flag.challenge_id
        assert updated_flag.task_id == flag.task_id
        assert updated_flag.value == Crypto.hash_to_md5(flag.value)

        updated_size = len(list(flag_collection_with_data.find()))
        assert initial_size == updated_size

    def test_invalid_flag_should_not_overwrite_db_data(
        self, flag_collection_with_data, connection_url
    ):
        """Test flag update"""
        initial_size = len(list(flag_collection_with_data.find()))
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(
            value="flag{INVALID-NAME}",
            task_id="firsttask",
            challenge_id="firstchallenge",
        )
        updated_flag = flag_service.update_flag(flag)
        assert updated_flag is None

        updated_size = len(list(flag_collection_with_data.find()))
        assert initial_size == updated_size

        existing_record = flag_collection_with_data.find(
            {"challenge_id": flag.challenge_id, "task_id": flag.task_id}
        )[0]
        assert existing_record["value"] == Crypto.hash_to_md5("flag{test_1}")

    def test_update_not_existing_flag_should_fail(
        self, flag_collection_with_data, connection_url
    ):
        """Test flag update"""
        initial_size = len(list(flag_collection_with_data.find()))
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(
            value="flag{test_update}",
            task_id="secondtask",
            challenge_id="secondchallenge",
        )
        updated_flag = flag_service.update_flag(flag)
        assert updated_flag is None

        updated_size = len(list(flag_collection_with_data.find()))
        assert initial_size == updated_size
