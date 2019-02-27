class NodeData:
    def __init__(self, key, data):
        self.key = key
        self.data = data

    def __lt__(self, other):
        return self.key < other.key
    def __gt__(self, other):
        return self.key > other.key
    def __str__(self):
        return str(self.key)+':'+str(self.data)
    def __repr__(self):
        return str(self)

class Node:
    def __init__(self, data):

        self.left = None
        self.right = None
        self.data = data

    def insert(self, data):
# Compare the new value with the parent node
        if self.data:
            if data < self.data:
                if self.left is None:
                    self.left = Node(data)
                else:
                    self.left.insert(data)
            elif data > self.data:
                if self.right is None:
                    self.right = Node(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print( self.data),
        if self.right:
            self.right.PrintTree()
    
    def SortedUntil(self, K, sorted):
        if K == 0:
            return K
        if self.left:
            K = self.left.SortedUntil(K, sorted) 
        if K > 0:
            sorted.append(self.data)
            K -= 1
        if self.right:
            K = self.right.SortedUntil(K, sorted)
        return K