"""Flag Data Transfer Object"""
from dataclasses import dataclass


@dataclass
class FlagDto:
    """Class for Flag DTO"""
    id: str
    value: str
    challange_id: str
    task_id: str
