"""Module that contains logick for base actions on flags"""

import logging
from datetime import datetime as dt
from ctf_server.core.crypto import Crypto
from ctf_server.core.flag_validator import FlagValidator
from ctf_server.core.flag_validator_strategy import FlagValidatorStrategy
from ctf_server.db.dto.flag_dto import FlagDto
from ctf_server.db.storage_service import StorageService
from ctf_server.model.flag import Flag
from ctf_server.model.state import State


class FlagService:
    """Class with base functions to work on flags"""

    def __init__(
        self, storage_service: StorageService, strategy: FlagValidatorStrategy
    ) -> None:
        self._storage_service = storage_service
        self._flag_validator = FlagValidator(strategy)

    def submit_flag(self, flag: Flag) -> State:
        """
        Takes one flag as an input, then based on its challange and task
        reference the correct flag value is requested from storage. Finally
        uses flag validator to check whether provided flag is correct for
        specific task.

        Args:
            flag (Flag): flag provided by user

        Returns:
            state (State): state calculated based on user input
        """
        actual_flag = self._storage_service.get_flag(flag.challange_id, flag.task_id)
        return self._flag_validator.is_valid_flag(flag.value, actual_flag.value)

    def get_flag(self, challange_id: str, task_id: id) -> Flag:
        """Get flag per challange and task id

        Args:
            challange_id (str): flag challange id
            task (id): flag task id

        Returns:
            Flag: returns flag from storage
        """
        logging.debug("Try to get a flag [challange_id=%s, task_id=%s]", challange_id, task_id)
        flag_dto = self._storage_service.get_flag(challange_id, task_id)
        if flag_dto is None:
            return None
        return Flag(
            value=flag_dto.value,
            challange_id=flag_dto.challange_id,
            task_id=flag_dto.task_id,
        )

    def get_all_flags(self) -> list[Flag]:
        """Get all flags from storage"""
        logging.debug("Try to get all")
        flag_dtos = self._storage_service.get_all_flags()
        flags = []
        for flag_dto in flag_dtos:
            flags.append(
                Flag(
                    value=flag_dto.value,
                    challange_id=flag_dto.challange_id,
                    task_id=flag_dto.task_id,
                )
            )
        return flags

    def create_flag(self, flag: Flag) -> Flag:
        """Based on flag details provided by user creates object in storage

        Args:
            flag (Flag): data provided by user

        Returns:
            Flag: returns None if there is an error otherwise returns saved flag dto
        """
        if flag.value is None:
            logging.debug("FLAG_SERVICE::Flag creation failed - flag value is none")
            return None
        is_valid_format = self._flag_validator.validate_flag_format(flag.value)
        if not is_valid_format:
            logging.debug("FLAG_SERVICE::Flag creation failed - invalid flag format")
            return None

        if self._storage_service.get_flag(flag.challange_id, flag.task_id) is not None:
            logging.debug("FLAG_SERVICE::Flag creation failed - flag already exists")
            return None

        flag_dto = FlagDto(
            id=str(int(dt.timestamp(dt.now()))),
            value=Crypto.hash_to_md5(flag.value),
            challange_id=flag.challange_id,
            task_id=flag.task_id,
        )
        flag_dto = self._storage_service.create_flag(flag_dto)
        logging.debug("FLAG_SERVICE::Flag created successfully")
        return Flag(
            value=flag_dto.value,
            challange_id=flag_dto.challange_id,
            task_id=flag_dto.task_id,
        )

    def remove_flag(self, challange_id: str, task_id: str) -> bool:
        """Delete flag based on assigned challange and task ids

        Args:
            challange_id (str): flag challange id
            task_id (str): flag task id

        Returns:
            bool: returns True if flag was deleted successfully
        """
        flag = self._storage_service.get_flag(challange_id, task_id)
        if flag is None:
            return False
        return self._storage_service.delete_flag(challange_id, flag.id)

    def update_flag(self, flag: Flag):
        """Based on flag details provided by user updated existing object in storage

        Args:
            flag (Flag): data provided by user

        Returns:
            Flag: returns None if there is an error otherwise returns saved flag dto
        """
        if flag.value is None:
            logging.debug("FLAG_SERVICE::Flag updated failed - flag value is none")
            return None
        is_valid_format = self._flag_validator.validate_flag_format(flag.value)
        if not is_valid_format:
            logging.debug("FLAG_SERVICE::Flag update failed - invalid flag format")
            return None

        existing_flag = self._storage_service.get_flag(flag.challange_id, flag.task_id)
        if existing_flag is None:
            logging.debug("FLAG_SERVICE::Flag update failed - flag does not exists")
            return None

        if existing_flag.challange_id != flag.challange_id:
            logging.debug(
                "FLAG_SERVICE::Flag update failed - challange id cannot be updated"
            )
            return None
        if existing_flag.task_id != flag.task_id:
            logging.debug(
                "FLAG_SERVICE::Flag update failed - task id cannot be updated"
            )
            return None

        existing_flag.value = Crypto.hash_to_md5(flag.value)
        flag_dto = self._storage_service.update_flag(existing_flag)
        if flag_dto is None:
            logging.debug("FLAG_SERVICE::Flag update failed")
            return None
        logging.debug("FLAG_SERVICE::Flag updated successfully")
        return Flag(
            value=flag_dto.value,
            challange_id=flag_dto.challange_id,
            task_id=flag_dto.task_id,
        )
