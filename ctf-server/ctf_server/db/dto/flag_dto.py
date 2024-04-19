"""Flag Data Transfer Object"""

from dataclasses import dataclass


@dataclass
class FlagDto:
    """Class for Flag DTO"""

    id: str
    value: str
    challenge_id: str
    task_id: str
    task_nr: int

    def to_dict(self):
        """Map flag dto to dictionary"""
        return self.__dict__

    @classmethod
    def from_dict(cls, dict_obj):
        """Convert dictionary to FlagDto object"""
        return cls(
            id=dict_obj["id"],
            value=dict_obj["value"],
            challenge_id=dict_obj["challenge_id"],
            task_id=dict_obj["task_id"],
            task_nr=dict_obj["task_nr"],
        )
