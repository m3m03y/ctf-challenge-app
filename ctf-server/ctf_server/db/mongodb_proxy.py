"""Proxy for Mongo DB"""

import logging
from pymongo import MongoClient
from ctf_server import config
from ctf_server.db.storage_service import StorageService
from ctf_server.db.dto.flag_dto import FlagDto


class MongodbProxy(StorageService):
    """Handles connection and flag management in Mongo DB"""

    _CONNECTION_STRING = config.mongo["connection_string"]
    _DATABASE_ID = config.mongo["database_id"]
    _COLLECTION_ID = config.mongo["collection_id"]

    def __init__(self, connection_string: str = _CONNECTION_STRING) -> None:
        self._client = MongoClient(connection_string)
        self._database = self._client[self._DATABASE_ID]
        self._collection = self._database[self._COLLECTION_ID]
        logging.info("MONGODB_PROXY::Database connection ready")

    def get_flag(self, challenge_id: str, task_id: str) -> FlagDto:
        """Get flag from storage based on task and challenge ids"""
        matching_flags = list(
            self._collection.find({"challenge_id": challenge_id, "task_id": task_id})
        )
        query_matches = len(matching_flags)
        if query_matches != 1:
            logging.error("MONGODB_PROXY::Invalid flag count find: %d", query_matches)
            return None
        logging.debug("MONGODB_PROXY::Flag successfully found in DB")
        return self._document_to_dto(matching_flags[0])

    def get_all_flags(self) -> list[FlagDto]:
        """Get all flags from storage"""
        flags = self._collection.find()
        flag_dtos = [self._document_to_dto(flag_doc) for flag_doc in flags]
        logging.debug("MONGODB_PROXY::All flags retrived count = %d", len(flag_dtos))
        return flag_dtos

    def create_flag(self, flag: FlagDto) -> FlagDto:
        """Create flag for task and challenge"""
        insert_result = self._collection.insert_one(
            document=self._dto_to_document(flag)
        )
        logging.debug(
            "MONGODB_PROXY::Flag inserted correctly id=%s", insert_result.inserted_id
        )
        get_inserted_query = {"_id": insert_result.inserted_id}
        saved_flag = self._collection.find(get_inserted_query)[0]
        return self._document_to_dto(saved_flag)

    def update_flag(self, flag: FlagDto) -> FlagDto:
        """Update flag document based on flag id"""
        query = {"challenge_id": flag.challenge_id, "task_id": flag.task_id}
        updated_values = {"$set": {"value": flag.value}}
        update_result = self._collection.update_one(query, updated_values)
        if update_result.modified_count != 1:
            logging.error(
                "MONGODB_PROXY::Invalid updated flag count: %d",
                update_result.modified_count,
            )
            return None
        updated_flag = self._collection.find(query)[0]
        logging.debug("MONGODB_PROXY::Flag with id=%s updated successfully", flag.id)
        return self._document_to_dto(updated_flag)

    def delete_flag(self, challenge_id: str, flag_id: str) -> bool:
        """Delete flag based on challenge and task ids"""
        delete_query = {"challenge_id": challenge_id, "_id": flag_id}
        delete_result = self._collection.delete_one(delete_query)
        if delete_result.deleted_count == 1:
            logging.debug(
                "MONGODB_PROXY::Flag with id=%s successfully deleted", flag_id
            )
            return True
        logging.error(
            "MONGODB_PROXY::Flag deletion failed deleted count = %d",
            delete_result.deleted_count,
        )
        return False

    def get_next_task(self, challenge_id: str, task_nr: int) -> str:
        """Get next task id based on given task nr"""
        next_task = self._collection.find_one(
            filter={"challenge_id": challenge_id, "task_nr": task_nr},
            projection={"_id": False, "task_id": True},
        )
        if next_task is None:
            logging.error("MONGODB_PROXY::No next task found")
            return None
        logging.debug("MONGODB_PROXY::Next task successfully found in DB")

        return next_task["task_id"]

    def _dto_to_document(self, flag_dto: FlagDto):
        flag_doc = flag_dto.to_dict()
        del flag_doc["id"]
        return flag_doc

    def _document_to_dto(self, flag_doc) -> FlagDto:
        flag_doc["id"] = flag_doc.pop("_id")
        return FlagDto.from_dict(flag_doc)
