import copy
from typing import List, Dict, Union


class VectorClock:
    def __init__(self, pid: str, processes: List[str]) -> None:
        self.pid: str = pid
        self.pid_to_timestamp_map: Dict[str, int] = {process: 0 for process in processes}

    def increment(self) -> None:
        self.pid_to_timestamp_map[self.pid] += 1

    def update(self, other_pid_to_timestamp_map: Dict[str, int]) -> None:
        # Update each entry to be the maximum of the two pid_to_timestamp_maps
        for process in self.pid_to_timestamp_map:
            self.pid_to_timestamp_map[process] = max(self.pid_to_timestamp_map[process],
                                                     other_pid_to_timestamp_map.get(process, 0))

    def get_pid_to_timestamp_map_copy(self):
        return copy.deepcopy(self.pid_to_timestamp_map)

    def concurrent_with(self, other: "VectorClock") -> bool:
        return not (self < other or self > other or self == other)

    def __str__(self) -> str:
        return str(self.pid_to_timestamp_map)

    def __lt__(self, other: Union["VectorClock", Dict[str, int]]) -> bool:
        """
        Check if this pid_to_timestamp_map happens before other pid_to_timestamp_map (strict ordering).
        For vector pid_to_timestamp_maps, A < B if A[i] <= B[i] for all i, and A[j] < B[j] for at least one j.
        """
        if isinstance(other, VectorClock):
            other_pid_to_timestamp_map = other.pid_to_timestamp_map
        else:
            other_pid_to_timestamp_map = other  # Assume it's a compatible dict

        # Check if all entries in self are <= corresponding entries in other
        less_or_equal = all(self.pid_to_timestamp_map.get(p, 0) <= other_pid_to_timestamp_map.get(p, 0)
                            for p in
                            set(self.pid_to_timestamp_map.keys()).union(
                                other_pid_to_timestamp_map.keys()))
        # Check if at least one entry in self is < corresponding entry in other
        strictly_less = any(self.pid_to_timestamp_map.get(p, 0) < other_pid_to_timestamp_map.get(p, 0)
                            for p in
                            set(self.pid_to_timestamp_map.keys()).union(
                                other_pid_to_timestamp_map.keys()))

        return less_or_equal and strictly_less

    def __gt__(self, other: Union["VectorClock", Dict[str, int]]) -> bool:
        """Check if this pid_to_timestamp_map happens after other pid_to_timestamp_map (strict ordering)"""
        if isinstance(other, VectorClock):
            other_pid_to_timestamp_map = other.pid_to_timestamp_map
        else:
            other_pid_to_timestamp_map = other

        # Check if all entries in self are >= corresponding entries in other
        greater_or_equal = all(self.pid_to_timestamp_map.get(p, 0) >= other_pid_to_timestamp_map.get(p, 0)
                               for p in
                               set(self.pid_to_timestamp_map.keys()).union(
                                   other_pid_to_timestamp_map.keys()))
        # Check if at least one entry in self is > corresponding entry in other
        strictly_greater = any(self.pid_to_timestamp_map.get(p, 0) > other_pid_to_timestamp_map.get(p, 0)
                               for p in
                               set(self.pid_to_timestamp_map.keys()).union(
                                   other_pid_to_timestamp_map.keys()))

        return greater_or_equal and strictly_greater

    def __eq__(self, other: Union["VectorClock", Dict[str, int]]) -> bool:
        """Check if two pid_to_timestamp_maps are identical"""
        if isinstance(other, VectorClock):
            other_pid_to_timestamp_map = other.pid_to_timestamp_map
        else:
            other_pid_to_timestamp_map = other

        # pid_to_timestamp_maps are equal if all entries match
        return all(self.pid_to_timestamp_map.get(p, 0) == other_pid_to_timestamp_map.get(p, 0)
                   for p in
                   set(self.pid_to_timestamp_map.keys()).union(other_pid_to_timestamp_map.keys()))
