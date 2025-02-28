from dataclasses import dataclass
from typing import Dict

from VectorClock import VectorClock


@dataclass
class Post:
    message: str
    author: str
    pid_to_timestamp_map: Dict[str, int]  # Map of process IDs to their clock values
    post_id: int
