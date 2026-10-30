"""
LRU Cache Implementation with O(1) get and put operations.

Uses a combination of:
- Hash map (dictionary) for O(1) key lookups
- Doubly linked list for O(1) insertion/deletion and tracking access order
"""


class Node:
    """Doubly linked list node to store key-value pairs."""

    def __init__(self, key=0, value=0):
        self.key = key
        self.value = value
        self.prev = None
        self.next = None


class LRUCache:
    """
    LRU (Least Recently Used) Cache with O(1) get and put operations.

    The cache maintains a fixed capacity and evicts the least recently used
    item when the capacity is exceeded.
    """

    def __init__(self, capacity: int):
        """
        Initialize the LRU cache with a fixed capacity.

        Args:
            capacity: Maximum number of items the cache can hold
        """
        self.capacity = capacity
        self.cache = {}  # Maps keys to nodes

        # Dummy head and tail nodes to simplify edge cases
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _remove(self, node: Node) -> None:
        """Remove a node from the doubly linked list."""
        prev_node = node.prev
        next_node = node.next
        prev_node.next = next_node
        next_node.prev = prev_node

    def _add_to_head(self, node: Node) -> None:
        """Add a node right after the head (most recently used position)."""
        node.prev = self.head
        node.next = self.head.next
        self.head.next.prev = node
        self.head.next = node

    def _move_to_head(self, node: Node) -> None:
        """Move an existing node to the head (mark as recently used)."""
        self._remove(node)
        self._add_to_head(node)

    def _remove_tail(self) -> Node:
        """Remove and return the node before the tail (least recently used)."""
        lru_node = self.tail.prev
        self._remove(lru_node)
        return lru_node

    def get(self, key: int) -> int:
        """
        Get the value of the key if it exists in the cache.

        Args:
            key: The key to look up

        Returns:
            The value associated with the key, or -1 if key doesn't exist

        Time Complexity: O(1)
        """
        if key not in self.cache:
            return -1

        node = self.cache[key]
        self._move_to_head(node)  # Mark as recently used
        return node.value

    def put(self, key: int, value: int) -> None:
        """
        Set or insert the value if the key is not already present.
        When the cache reaches its capacity, it should invalidate the
        least recently used item before inserting a new item.

        Args:
            key: The key to insert or update
            value: The value to associate with the key

        Time Complexity: O(1)
        """
        if key in self.cache:
            # Update existing key
            node = self.cache[key]
            node.value = value
            self._move_to_head(node)
        else:
            # Insert new key
            new_node = Node(key, value)
            self.cache[key] = new_node
            self._add_to_head(new_node)

            # Check capacity
            if len(self.cache) > self.capacity:
                # Remove least recently used item
                lru_node = self._remove_tail()
                del self.cache[lru_node.key]


# Unit Tests
def test_basic_operations():
    """Test basic get and put operations."""
    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    assert cache.get(1) == 1, "Should retrieve value 1 for key 1"

    cache.put(3, 3)  # Evicts key 2
    assert cache.get(2) == -1, "Key 2 should be evicted"

    cache.put(4, 4)  # Evicts key 1
    assert cache.get(1) == -1, "Key 1 should be evicted"
    assert cache.get(3) == 3, "Should retrieve value 3 for key 3"
    assert cache.get(4) == 4, "Should retrieve value 4 for key 4"

    print("✓ test_basic_operations passed")


def test_update_existing_key():
    """Test updating an existing key doesn't count as new insertion."""
    cache = LRUCache(2)

    cache.put(1, 1)
    cache.put(2, 2)
    cache.put(1, 10)  # Update key 1, moves it to front, doesn't evict anything

    assert cache.get(1) == 10, "Should retrieve updated value 10"
    # Don't access key 2 here, so it remains least recently used

    cache.put(3, 3)  # Evicts key 2 (least recently used)
    assert cache.get(2) == -1, "Key 2 should be evicted"
    assert cache.get(1) == 10, "Key 1 should still be present"
    assert cache.get(3) == 3, "Key 3 should be present"

    print("✓ test_update_existing_key passed")


def test_single_capacity():
    """Test cache with capacity of 1."""
    cache = LRUCache(1)

    cache.put(1, 1)
    assert cache.get(1) == 1, "Should retrieve value 1"

    cache.put(2, 2)  # Evicts key 1
    assert cache.get(1) == -1, "Key 1 should be evicted"
    assert cache.get(2) == 2, "Should retrieve value 2"

    cache.put(3, 3)  # Evicts key 2
    assert cache.get(2) == -1, "Key 2 should be evicted"
    assert cache.get(3) == 3, "Should retrieve value 3"

    print("✓ test_single_capacity passed")


if __name__ == "__main__":
    print("Running LRU Cache tests...\n")

    test_basic_operations()
    test_update_existing_key()
    test_single_capacity()

    print("\nAll tests passed! ✓")
