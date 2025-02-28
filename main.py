from BulletinBoard import BulletinBoard


def run_bulletin_board_demo():
    """Run a demonstration of the bulletin board with vector clocks"""
    # Create a bulletin board with three processes
    processes = ["Alice", "Bob", "Charlie"]
    board = BulletinBoard(processes)

    print("=== Vector Clock Bulletin Board Demonstration ===")
    print("This demo shows how vector clocks track causality in a distributed system.\n")

    # Step 1: Alice posts a message
    print("Step 1: Alice posts a message")
    board.post_message("Alice", "Hello everyone!")
    board.display_board("Alice")

    # Step 2: Bob posts a message independently (concurrent with Alice's post)
    print("\nStep 2: Bob posts a message (independent of Alice)")
    board.post_message("Bob", "Greetings from Bob!")
    board.display_board("Bob")

    # Step 3: Alice and Bob sync - now both have each other's posts
    print("\nStep 3: Alice and Bob synchronize their boards")
    board.sync_nodes("Alice", "Bob")
    print("Alice's board after sync:")
    board.display_board("Alice")
    print("Bob's board after sync:")
    board.display_board("Bob")

    # Step 4: Alice posts after sync with Bob (causally after Bob's post)
    print("\nStep 4: Alice posts after syncing with Bob")
    board.post_message("Alice", "I just synced with Bob!")
    board.display_board("Alice")

    # Step 5: Charlie posts (hasn't synced with anyone - concurrent to all previous posts)
    print("\nStep 5: Charlie posts a message (hasn't synced with anyone)")
    board.post_message("Charlie", "Hi from Charlie!")
    board.display_board("Charlie")

    # Step 6: Bob and Charlie sync
    print("\nStep 6: Bob and Charlie synchronize their boards")
    board.sync_nodes("Bob", "Charlie")
    print("Bob's board after sync with Charlie:")
    board.display_board("Bob")
    print("Charlie's board after sync with Bob:")
    board.display_board("Charlie")

    # Step 7: Charlie posts after sync with Bob
    print("\nStep 7: Charlie posts after syncing with Bob")
    board.post_message("Charlie", "I've synced with Bob but not Alice yet!")
    board.display_board("Charlie")

    # Step 8: Final sync of all nodes
    print("\nStep 8: Final synchronization of all nodes")
    board.sync_nodes("Alice", "Charlie")

    # Step 9: Display final state of all boards
    print("\nStep 9: Final state of all bulletin boards")
    for process in processes:
        board.display_board(process)

    print("\n=== Demonstration Complete ===")
    print("This demonstration showed how vector clocks maintain causality information")
    print("in a distributed system, even when processes operate independently and")
    print("synchronize at different times.")


if __name__ == "__main__":
    run_bulletin_board_demo()
