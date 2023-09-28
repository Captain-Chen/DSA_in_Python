class Node():
    def __init__(self, data):
        self.data = data
        self.next = None
        self.prev = None

    def __repr__(self):
        return self.data

class MyDoublyLinkedList():
    def __init__(self, nodes=None):
        self.head = None
        self.tail = None

        if nodes is not None:
            node = Node(data=nodes.pop(0))
            self.head = node

            for item in nodes:
                node.next = Node(data=item)
                node.next.prev = node
                node = node.next
    
    def __iter__(self):
        node = self.head
        while node is not None:
            yield node
            node = node.next

    def __repr__(self):
        node = self.head
        nodes = []

        while node is not None:
            nodes.append(node.data)
            node = node.next
        nodes.append("None")
        return " <-> ".join(nodes) 
    
    def __len__(self):
        node_count = 0
        for node in self:
            node_count += 1
        return node_count

    def add_first(self, node):
        node.next = self.head
        self.head = node

    def add_last(self, node):
        if self.head is None:
            self.head = node
            return
        for current_node in self:
            pass
        current_node.next = node
        node.prev = current_node

    def add_before(self, target_node_data, new_node):
        if self.head == None:
            raise Exception("Cannot add to an empty list")
        
        if self.head.data == target_node_data:
            return self.add_first(new_node)
        
        prev_node = self.head
        for curr_node in self:
            if curr_node.data == target_node_data:
                prev_node.next = new_node
                new_node.prev = prev_node
                new_node.next = curr_node
                curr_node.prev = new_node
                return
            prev_node = curr_node
            
        raise Exception("Node with '%s' was not found" % target_node_data)

    def add_after(self, target_node_data, new_node):
        if self.head == None:
            raise Exception("Cannot add to an empty list")
        
        for curr_node in self:
            if curr_node.data == target_node_data:
                new_node.next = curr_node.next
                new_node.prev = curr_node
                curr_node.next = new_node
                return
            
        raise Exception("Node with data '%s' was not found" % target_node_data)
    
    def remove(self, target_node_data):
        if self.head == None:
            raise Exception("Cannot delete from an empty list")
        
        if self.head.data == target_node_data:
            self.head = self.head.next
            return
        
        prev_node = self.head
        for curr_node in self:
            if curr_node.data == target_node_data:
                prev_node.next = curr_node.next
                curr_node.next.prev = prev_node
                return
            prev_node = curr_node

        raise Exception("Node with data '%s' was not found" % target_node_data)