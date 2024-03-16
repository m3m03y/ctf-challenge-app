"""Test flag management service module"""

from ctf_server.core.crypto import Crypto
from ctf_server.model.flag import Flag
from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.db.mongodb_proxy import MongodbProxy
from ctf_server.service.flag_service import FlagService


class TestFlagService:
    """Tests flag service functions"""

    def test_flag_created_correctly(self, prepare_flag_collection, connection_url):
        # monkeypatch.setenv("MONGODB_CONNECTION_STRING", mongo_container.get_connection_url())
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        flag = Flag(
            value="flag{test}", task_id="firsttask", challange_id="firstchallange"
        )
        created_flag = flag_service.create_flag(flag)
        assert created_flag.challange_id == flag.challange_id
        assert created_flag.task_id == flag.task_id
        assert created_flag.value == Crypto.hash_to_md5(flag.value)
