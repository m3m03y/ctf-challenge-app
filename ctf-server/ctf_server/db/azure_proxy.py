"""Adapter for Azure Cosmo DB"""

import logging
from ctf_server.db.dto.flag_dto import FlagDto
from ctf_server.db.storage_service import StorageService
import ctf_server.config as config
import azure.cosmos.cosmos_client as cosmos_client
import azure.cosmos.exceptions as exceptions
from azure.cosmos.container import ContainerProxy
from azure.cosmos.database import DatabaseProxy
from azure.cosmos.partition_key import PartitionKey


class AzureProxy(StorageService):
    """Handles connection and working with Azure Cosmos DB"""

    _HOST = config.azure_connection["host"]
    _MASTER_KEY = config.azure_connection["master_key"]
    _DATABASE_ID = config.azure_dev["database_id"]
    _CONTAINER_ID = config.azure_dev["container_id"]

    def __init__(self) -> None:
        self._client = self._get_client()
        self._database = self._get_or_create_database()
        self._container = self._get_or_create_container()
        logging.info("AZURE_PROXY::Database connection ready")

    def _get_client(self) -> cosmos_client.CosmosClient:
        return cosmos_client.CosmosClient(
            self._HOST,
            {"masterKey": self._MASTER_KEY},
            user_agent="CosmosDBPythonQuickstart",
            user_agent_overwrite=True,
        )

    def _get_or_create_database(self) -> DatabaseProxy:
        try:
            db = self._client.create_database(id=self._DATABASE_ID)
            logging.debug(
                "AZURE_PROXY::Database with id=%s not found, creating new database",
                self._DATABASE_ID,
            )
        except exceptions.CosmosResourceExistsError:
            db = self._client.get_database_client(self._DATABASE_ID)
            logging.debug("AZURE_PROXY::Database with id=%s found", self._DATABASE_ID)
        return db

    def _get_or_create_container(self) -> ContainerProxy:
        try:
            container = self._database.create_container(
                self._CONTAINER_ID, partition_key=PartitionKey(path="/partitionKey")
            )
            logging.debug(
                "AZURE_PROXY::Container with id=%s not found, creating new container",
                self._CONTAINER_ID,
            )
        except exceptions.CosmosResourceExistsError:
            container = self._database.get_container_client(self._CONTAINER_ID)
            logging.debug("AZURE_PROXY::Container with id=%s found", self._DATABASE_ID)
        return container

    def get_flag(self, challange_id: str, task_id: str) -> FlagDto:
        """Get flag from storage based on task and challange ids"""
        matching_flags = list(
            self._container.query_items(
                query="""
                    SELECT * 
                    FROM record 
                    WHERE record.partitionKey=@challange_id AND record.task_id=@task_id
                """,
                parameters=[
                    {"name": "@challange_id", "value": challange_id},
                    {"name": "@task_id", "value": task_id},
                ],
            )
        )
        if len(matching_flags) != 1:
            logging.error("AZURE_PROXY::Count flags matching query: %d", len(matching_flags))
            return None
        logging.debug("AZURE_PROXY::Flag successfully read from DB")
        return self._dict_to_dto(matching_flags[0])

    def get_all_flags(self) -> list[FlagDto]:
        """Get all flags from storage"""
        flags = self._container.read_all_items(max_item_count=20)
        flags_dtos = []
        for flag in flags:
            flags_dtos.append(self._dict_to_dto(flag))
        logging.debug("AZURE_PROXY::Group of flag retireved from DB size = %d", len(flags_dtos))
        return flags_dtos

    def create_flag(self, flag: FlagDto) -> FlagDto:
        """Create flag for task and challange"""
        saved_flag = self._container.create_item(body=self._dto_to_dict(flag))
        logging.debug("AZURE_PROXY::Flag saved correctly id=%s", saved_flag["id"])
        return self._dict_to_dto(saved_flag)

    def update_flag(self, flag: FlagDto) -> FlagDto:
        """Update flag document based on flag id"""
        flag_dict = self._dto_to_dict(flag)
        updated_flag = self._container.replace_item(item=flag_dict["id"], body=flag_dict)
        logging.debug("AZURE_PROXY::Flag with id=%s updated successfully", updated_flag["id"])
        return self._dict_to_dto(updated_flag)


    def delete_flag(self, challange_id: str, flag_id: str) -> bool:
        """Delete flag based on challange and task ids"""
        try:
            self._container.delete_item(item=flag_id, partition_key=challange_id)
            logging.debug("AZURE_PROXY::Flag with id=%s successfully deleted", flag_id)
            return True
        except (exceptions.CosmosResourceNotFoundError, exceptions.CosmosHttpResponseError):
            logging.error("AZURE_PROXY::Could not delete flag with id=%s", flag_id)
            return False

    def _dto_to_dict(self, flag: FlagDto) -> dict:
        return {
            "id": flag.id,
            "partitionKey": flag.challange_id,
            "challange_id": flag.challange_id,
            "task_id": flag.task_id,
            "value": flag.value,
        }

    def _dict_to_dto(self, flag_dict: dict) -> FlagDto:
        return FlagDto(
            id=flag_dict["id"],
            challange_id=flag_dict["challange_id"],
            task_id=flag_dict["task_id"],
            value=flag_dict["value"],
        )
