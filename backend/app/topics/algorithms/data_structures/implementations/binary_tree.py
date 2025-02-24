class Node:
    def __init__(self, key):
        self.left = None  # Left child
        self.right = None  # Right child
        self.value = key  # Value of the node

class BinaryTree:
    def __init__(self):
        self.root = None  # Initially  tree is empty so the root is None

    def insert(self, key):
        # If the tree is empty, create a new node as the root
        if self.root is None:
            self.root = Node(key)
        else:
            # Otherwise, insert the key in the correct position
            self._insert_recursive(self.root, key)

    def _insert_recursive(self, node, key):
        # If  key is less than current node's value go to left child
        if key < node.value:
            if node.left is None:
                node.left = Node(key)  # Insert key as left child
            else:
                # Recursive insert key in left subtree
                self._insert_recursive(node.left, key)
        # If key is greater than current node's value go to right child
        elif key > node.value:
            if node.right is None:
                node.right = Node(key)  # Insert key as right child
            else:
                # Recursive insert key in right subtree
                self._insert_recursive(node.right, key)

    def inorder_traversal(self, node):
        # Traverse the left subtree
        if node:
            self.inorder_traversal(node.left)
            # Print the node's value
            print(node.value, end=" ")
            # Traverse the right subtree
            self.inorder_traversal(node.right)

    def display(self):
        # Start inorder traversal from root and print  tree values
        self.inorder_traversal(self.root)
        print()

# Example
tree = BinaryTree()  # Create a new empty binary tree
tree.insert(10)  # Insert values into the tree
tree.insert(20)
tree.insert(5)
tree.insert(15)
tree.insert(30)

tree.display()  # Display the tree in sorted order
