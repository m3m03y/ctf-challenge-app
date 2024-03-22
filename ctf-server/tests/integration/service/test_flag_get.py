"""Test flag management service module - get flag part"""

from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.db.mongodb_proxy import MongodbProxy
from ctf_server.model.flag import Flag
from ctf_server.service.flag_service import FlagService
from ctf_server.core.crypto import Crypto


class TestFlagRemove:
    """Tests get flags functions"""

    def test_get_all_flag_should_return_3_entries(
        self, flag_collection_with_data, connection_url
    ):
        """Test get all flag from db"""
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )
        expected_flags = [
            Flag(
                value=Crypto.hash_to_md5("flag{test_1}"),
                challenge_id="firstchallenge",
                task_id="firsttask",
            ),
            Flag(
                value=Crypto.hash_to_md5("flag{test_2}"),
                challenge_id="firstchallenge",
                task_id="secondtask",
            ),
            Flag(
                value=Crypto.hash_to_md5("flag{test_2_1}"),
                challenge_id="secondchallenge",
                task_id="firsttask",
            ),
        ]
        initial_size = len(list(flag_collection_with_data.find()))

        flags = flag_service.get_all_flags()

        assert initial_size == len(flags)

        assert expected_flags == flags

    def test_get_single_existing_flag_should_get_valid_entry(
        self, flag_collection_with_data, connection_url
    ):
        """Test get single existing flag"""
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )
        expected_flag = Flag(
            value=Crypto.hash_to_md5("flag{test_1}"),
            challenge_id="firstchallenge",
            task_id="firsttask",
        )

        initial_size = len(list(flag_collection_with_data.find()))
        assert initial_size == 3
        
        flag = flag_service.get_flag(expected_flag.challenge_id, expected_flag.task_id)
        assert expected_flag == flag

    def test_get_not_existing_flag_should_return_none(
        self, flag_collection_with_data, connection_url
    ):
        """Test get not existing flag"""
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        initial_size = len(list(flag_collection_with_data.find()))
        assert initial_size == 3

        flag = flag_service.get_flag("not_existing", "not_existing")
        assert flag is None
