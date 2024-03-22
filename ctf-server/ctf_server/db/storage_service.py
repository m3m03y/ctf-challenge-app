"""Interface for storage services"""

from abc import ABC, abstractmethod
from ctf_server.db.dto.flag_dto import FlagDto


class StorageService(ABC):
    """Defines group of functions to manage flags"""

    @abstractmethod
    def get_flag(self, challenge_id: str, task_id: str) -> FlagDto:
        """Get flag from storage based on task and challenge ids"""

    @abstractmethod
    def get_all_flags(self) -> list[FlagDto]:
        """Get all flags from storage"""

    @abstractmethod
    def create_flag(self, flag: FlagDto) -> FlagDto:
        """Create flag for task and challenge"""

    @abstractmethod
    def update_flag(self, flag: FlagDto) -> FlagDto:
        """Update flag document based on flag id"""

    @abstractmethod
    def delete_flag(self, challenge_id: str, flag_id: str) -> bool:
        """Delete flag based on challenge and task ids"""
