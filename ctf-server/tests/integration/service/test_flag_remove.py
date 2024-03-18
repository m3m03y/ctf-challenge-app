"""Test flag management service module - remove flag part"""

from ctf_server.core.flag_validator_strategy import PlainInputStoredHashedStrategy
from ctf_server.db.mongodb_proxy import MongodbProxy
from ctf_server.service.flag_service import FlagService


class TestFlagRemove:
    """Tests flag remove function"""

    def test_existing_flag_should_be_successfully_deleted(
        self, flag_collection_with_data, connection_url
    ):
        """Test flag delete"""
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        initial_size = len(list(flag_collection_with_data.find()))
        task_id = "firsttask"
        challange_id = "firstchallange"
        result = flag_service.remove_flag(challange_id, task_id)
        assert result

        after_remove_size = len(list(flag_collection_with_data.find()))
        assert after_remove_size == initial_size - 1

        deleted_records = flag_collection_with_data.find(
            {"challange_id": challange_id, "task_id": task_id}
        )
        assert len(list(deleted_records)) == 0

    def test_delete_not_existing_flag_should_fail(
        self, flag_collection_with_data, connection_url
    ):
        """Test flag delete"""
        flag_service = FlagService(
            MongodbProxy(connection_url),
            PlainInputStoredHashedStrategy(),
        )

        initial_size = len(list(flag_collection_with_data.find()))
        task_id = "secondtask"
        challange_id = "secondchallange"
        result = flag_service.remove_flag(challange_id, task_id)
        assert not result

        after_remove_size = len(list(flag_collection_with_data.find()))
        assert after_remove_size == initial_size
