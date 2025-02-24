class Node:
    def __init__(self, data):
        self.data = data  # Store data in node
        self.next = None  # Pointer to next node

class LinkedList:
    def __init__(self):
        self.head = None  # Initially list is empty so  head is None

    def append(self, data):
        # Create new node with given data
        new_node = Node(data)

        # If list empty, new node = head
        if not self.head:
            self.head = new_node
            return

        # Otherwise traverse to last node
        last_node = self.head
        while last_node.next:
            last_node = last_node.next

        # Set  next of last node to new node
        last_node.next = new_node

    def display(self):
        # Start from head and traverse through list
        current_node = self.head
        while current_node:
            print(current_node.data, end=" -> ")  # Print current node's data
            current_node = current_node.next  # Move to next node
        print("None")  #  end of list

    def delete(self, key):
        # If  list is empty return
        if not self.head:
            return

        # If node to delete = head node
        if self.head.data == key:
            self.head = self.head.next  # Move head to next node
            return

        # Otherwise find node to delete
        current_node = self.head
        while current_node.next:
            if current_node.next.data == key:
                current_node.next = current_node.next.next  # Remove node from list
                return
            current_node = current_node.next

# Example
ll = LinkedList()  # Create new empty linked list
ll.append(10)  # Add nodes to linked list
ll.append(20)
ll.append(30)

ll.display()  # Output: 10 -> 20 -> 30 -> None

ll.delete(20)  # Delete node with data 20
ll.display()  # Output: 10 -> 30 -> None
