from typing import List, Dict

from BulletinBoardNode import BulletinBoardNode
from Post import Post


class BulletinBoard:
    """
    A distributed bulletin board implementation using vector clocks.
    """

    def __init__(self, processes: List[str]):
        """
        Initialize a bulletin board with a set of processes.

        Args:
            processes: List of all process IDs that can post to the board
        """
        self.processes: List[str] = processes
        self.nodes: Dict[str, BulletinBoardNode] = {
            process_id: BulletinBoardNode(process_id, processes)
            for process_id in processes
        }
        self.next_post_id: int = 1

    def post_message(self, process_id: str, message: str) -> Post:
        """
        Post a new message from a specific process.

        Args:
            process_id: ID of the process posting the message
            message: Content of the post

        Returns:
            The created Post object
        """
        node = self.nodes[process_id]
        post = node.create_post(message, self.next_post_id)
        self.next_post_id += 1
        return post

    def sync_nodes(self, node1_id: str, node2_id: str) -> None:
        """
        Synchronize two nodes by exchanging posts and updating vector clocks.

        Args:
            node1_id: ID of the first node to sync
            node2_id: ID of the second node to sync
        """
        node1 = self.nodes[node1_id]
        node2 = self.nodes[node2_id]

        # Update node1 with posts from node2
        for post in node2.posts:
            if post.post_id not in node1.post_ids:
                node1.receive_post(post)

        # Update node2 with posts from node1
        for post in node1.posts:
            if post.post_id not in node2.post_ids:
                node2.receive_post(post)

    def display_board(self, process_id: str) -> None:
        """
        Display all posts from a specific process's perspective.

        Args:
            process_id: ID of the process/node to display posts from
        """
        node = self.nodes[process_id]

        print(f"\n=== Bulletin Board as seen by {process_id} ===")
        print(f"Current vector clock: {node.vector_clock}")
        print(f"Number of posts: {len(node.posts)}")

        # Sort posts by post_id for consistent display
        sorted_posts = sorted(node.posts, key=lambda p: p.post_id)

        for post in sorted_posts:
            # Add causality information relative to this node's clock
            causality_info = ""

            # Create temporary vector clock from post's timestamp for comparison
            if node.vector_clock < post.pid_to_timestamp_map:
                causality_info = "happened after current state"
            elif node.vector_clock > post.pid_to_timestamp_map:
                causality_info = "happened before current state"
            elif node.vector_clock == post.pid_to_timestamp_map:
                causality_info = "identical to current state"
            else:
                causality_info = "concurrent with current state"

            print(f"Post #{post.post_id} by {post.author} at {post.pid_to_timestamp_map}:")
            print(f"{post.message}")
            print(f"Causality: {causality_info}\n")

        print("=" * 50)
