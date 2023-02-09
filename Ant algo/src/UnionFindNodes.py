class UnionFindNodes:

    def __init__(self, collection):
        self.counter = len(collection)
        self.id = {}

        for node in collection:
            self.id[node] = node

    def find(self, p):
        node = p
        while node != self.id[node]:
            self.id[node] = self.id[self.id[node]]
            node = self.id[node]
        return node

    def union(self, p, q):
        pRoot = self.find(p)
        qroot = self.find(q)

        if(qroot != pRoot):
            self.id[pRoot] = qroot
            self.counter -= 1
            return True
        return False

    def connected(self, p, q):
        return self.find(p) == self.find(q)

    def count(self):
        return self.counter
