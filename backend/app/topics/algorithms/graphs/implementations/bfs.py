#BreathFrist Search

from collections import deque

class Node:
    def __init__(self, key):
        self.value = key  # Store value of node
        self.left = None  # Left child
        self.right = None  # Right child

class BinaryTree:
    def __init__(self):
        self.root = None  # tree is initially empty

    def insert(self, key):
        """Insert a new node in level order (BFS insert)"""
        if self.root is None:
            self.root = Node(key)  # If tree is empty then set root
            return

        queue = deque([self.root])  # Use queue to traverse level by level

        while queue:
            node = queue.popleft()  # Get first node in the queue

            # Insert in first empty left or right position
            if node.left is None:
                node.left = Node(key)
                return
            else:
                queue.append(node.left)  # Add left child to queue

            if node.right is None:
                node.right = Node(key)
                return
            else:
                queue.append(node.right)  # Add right child to queue

    def bfs_traversal(self):
        """Perform Breadth-First Search (BFS) or Level Order Traversal"""
        if not self.root:
            return  # If tree is empty, exit

        queue = deque([self.root])  # Initialize queue with root node

        while queue:
            node = queue.popleft()  # Dequeue the first node
            print(node.value, end=" ")  # Print node's value with space

            if node.left:
                queue.append(node.left)  # Enqueue left child
            if node.right:
                queue.append(node.right)  # Enqueue right child

# Example Usage
tree = BinaryTree()
tree.insert(1)
tree.insert(2)
tree.insert(3)
tree.insert(4)
tree.insert(5)
tree.insert(6)
tree.insert(7)

print("BFS Traversal (Level Order):")
tree.bfs_traversal()  # Expected: 1 2 3 4 5 6 7
