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
