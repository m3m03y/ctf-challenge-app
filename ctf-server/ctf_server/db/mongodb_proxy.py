"""Proxy for Mongo DB"""

import logging
from pymongo import MongoClient
from ctf_server import config
from ctf_server.db.storage_service import StorageService
from ctf_server.db.dto.flag_dto import FlagDto


class MongodbProxy(StorageService):
    """Handles connection and flag management in Mongo DB"""

    _CONNECTION_STRING = config.local_mongo["connection_string"]
    _DATABASE_ID = config.local_mongo["database_id"]
    _COLLECTION_ID = config.local_mongo["collection_id"]

    def __init__(self) -> None:
        self._client = MongoClient(self._CONNECTION_STRING)
        self._database = self._client[self._DATABASE_ID]
        self._collection = self._database[self._COLLECTION_ID]
        logging.info("MONGODB_PROXY::Database connection ready")

    def get_flag(self, challange_id: str, task_id: str) -> FlagDto:
        """Get flag from storage based on task and challange ids"""
        matching_flags = list(
            self._collection.find({"challange_id": challange_id, "task_id": task_id})
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
        """Create flag for task and challange"""
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
        query = {"challange_id": flag.challange_id, "task_id": flag.task_id}
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

    def delete_flag(self, challange_id: str, flag_id: str) -> bool:
        """Delete flag based on challange and task ids"""
        delete_query = {"challange_id": challange_id, "_id": flag_id}
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

    def _dto_to_document(self, flag_dto: FlagDto):
        return {
            "challange_id": flag_dto.challange_id,
            "task_id": flag_dto.task_id,
            "value": flag_dto.value,
        }

    def _document_to_dto(self, flag_doc) -> FlagDto:
        return FlagDto(
            id=flag_doc["_id"],
            challange_id=flag_doc["challange_id"],
            task_id=flag_doc["task_id"],
            value=flag_doc["value"],
        )
