## depths first search
from networkx.algorithms.traversal import dfs_postorder_nodes


class Node:
    def __init__(self,key):
        self.value = key #store value of key
        self.left = None #left Child
        self.right = None # right child

class BinaryTree:
    def __init__(self):
        self.root = None # tree is empty

    def insert(self, key):
        """Insert node in level order"""
        if self.root is None:
            self.root = Node(key)
            return

        queue = [self.root]

        while queue:
            node = queue.pop(0) #get  first node in queue

            if node.left is None:
                node.left = Node(key)
                return
            else:
                queue.append(node.left)

            if node.right is None:
                node.right = Node(key)
                return
            else:
                queue.append(node.right)

    def dfs_preorder(self, node):
        """Preorder traversal (Root -> left -> right)"""
        if node:
            print(node.value, end=" ") #visit root
            self.dfs_preorder(node.left) #visit left
            self.dfs_preorder(node.right) #visit right

    def dfs_inorder(self, node):
        """Inorder Traversal (Left -> Root -> Right)"""
        if node:
            self.dfs_inorder(node.left) #visit left
            print(node.value, end=" ") #visit root
            self.dfs_inorder(node.right) #visit right

    def dfs_postorder(self, node):
        """Postorder Traversal (Left -> Right -> Root)"""
        if node:
            self.dfs_postorder(node.left) #visit left
            self.dfs_postorder(node.right) # visit right
            print(node.value, end=" ") # visit root

#try
dfs_tree = BinaryTree()  #similar to bfs
dfs_tree.insert(1)
dfs_tree.insert(2)
dfs_tree.insert(3)
dfs_tree.insert(4)
dfs_tree.insert(5)
dfs_tree.insert(6)
dfs_tree.insert(7)


print("DFS Preorder (Root → Left → Right):")
dfs_tree.dfs_preorder(dfs_tree.root)  # Output: 1 2 4 5 3 6 7

print("\nDFS Inorder (Left → Root → Right):")
dfs_tree.dfs_inorder(dfs_tree.root)  # Output: 4 2 5 1 6 3 7

print("\nDFS Postorder (Left → Right → Root):")
dfs_tree.dfs_postorder(dfs_tree.root)  # Output: 4 5 2 6 7 3 1