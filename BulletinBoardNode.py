from typing import List, Set

from Post import Post
from VectorClock import VectorClock


class BulletinBoardNode:
    """A node in the distributed bulletin board system."""

    def __init__(self, node_id: str, all_nodes: List[str]) -> None:
        self.node_id: str = node_id
        self.vector_clock: VectorClock = VectorClock(node_id, all_nodes)
        self.posts: List[Post] = []
        self.post_ids: Set[int] = set()

    def create_post(self, message: str, post_id: int) -> Post:
        self.vector_clock.increment()
        post = Post(
            message=message,
            author=self.node_id,
            pid_to_timestamp_map=self.vector_clock.get_pid_to_timestamp_map_copy(),
            post_id=post_id
        )
        self.posts.append(post)
        self.post_ids.add(post_id)
        return post

    def receive_post(self, post: Post) -> None:
        self.vector_clock.increment()
        if post.post_id not in self.post_ids:
            self.vector_clock.update(post.pid_to_timestamp_map)
            self.posts.append(post)
            self.post_ids.add(post.post_id)
