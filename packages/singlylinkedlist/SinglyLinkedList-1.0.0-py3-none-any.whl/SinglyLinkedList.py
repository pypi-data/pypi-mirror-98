class List:
    def __init__(self, *elements):
        self.head = None
        self.tail = None
        self.size = 0
        for element in elements:
            self.append(element)

    def append(self, obj):
        if self.head:
            self.tail.next = Node(obj)
            self.tail = self.tail.next
        else:
            self.head = Node(obj)
            self.tail = self.head
        self.size += 1

    def pop(self, index=None):
        if not index:
            index = self.size - 1
        node = Node(0, self.head)
        for _ in range(index):
            node = node.next
        deleted = node.next
        if node.next == self.head:
            self.head = self.head.next
        else:
            node.next = node.next.next
        self.size -= 1
        return deleted

    def insert(self, obj, index=None):
        if index != 0:
            node = Node(0, self.head)
            for idx in range(index):
                node = node.next
            node.next = Node(obj, node.next)
        else:
            self.head = Node(obj, self.head)
        self.size += 1

    def remove(self, x):
        node = Node(0, self.head)
        for _ in range(self.size):
            if node.next.data == x and type(node.next.data) == type(x):
                deleted = node.next
                if deleted == self.head:
                    self.head = self.head.next
                else:
                    node.next = node.next.next
                self.size -= 1
                return deleted
            node = node.next
        return None

    def clear(self):
        self.__init__()

    def __str__(self):
        result = ''
        node = self.head
        for _ in range(self.size):
            result += str(node) + ', '
            node = node.next
        return '[' + result[:-2] + ']'

    def __add__(self, other):
        if type(other) == List:
            self.tail.next = other.head
            self.tail = other.tail
            self.size += other.size
        else:
            return TypeError
        return self

    def __mul__(self, other):
        if other == 0:
            self.clear()
        else:
            copied_list = self.copy()
            for _ in range(other - 1):
                self += copied_list.copy()
        return self

    def __getitem__(self, item):
        if isinstance(item, slice):
            if not item.start:
                start = 0
            else:
                start = item.start
            if not item.stop:
                stop = self.size
            else:
                stop = item.stop
            if not item.step:
                step = 1
            else:
                step = item.step
            Slice = List()
            node = self.head
            idx = 0
            while idx < stop:
                if start <= idx < stop and (idx - start) % step == 0:
                    Slice.append(node)
                node = node.next
                idx += 1
            return Slice
        else:
            if type(item) != int:
                return TypeError
            item %= self.size
            node = self.head
            for idx in range(item):
                node = node.next
            return node.data

    def __setitem__(self, key, data):
        if type(key) == int:
            if 0 <= key < self.size:
                node = self.head
                for _ in range(key):
                    node = node.next
                node.data = data
            else:
                return IndexError
        else:
            return TypeError

    def __contains__(self, item):
        node = self.head
        for _ in range(self.size):
            if node.data == item and type(node.data) == type(item):
                return True
            node = node.next
        return False

    def __iter__(self):
        self.currentNode = self.head
        return self

    def __next__(self):
        if self.currentNode:
            x = self.currentNode.data
            self.currentNode = self.currentNode.next
            return x
        else:
            del self.currentNode
            raise StopIteration

    def sort(self):
        sorted_list = List()
        node = self.head
        for _ in range(self.size):
            if sorted_list.size == 0:
                sorted_list.append(node.data)
            elif node.data <= sorted_list.head.data:
                sorted_list.insert(node.data, 0)
            elif node.data >= sorted_list.tail.data:
                sorted_list.append(node.data)
            else:
                other_node = sorted_list.head
                while not (other_node.data <= node.data <= other_node.next.data):
                    other_node = other_node.next
                other_node.next = Node(node.data, other_node.next)
            node = node.next
        self.head = sorted_list.head
        self.tail = sorted_list.tail

    def index(self, x):
        node = self.head
        for idx in range(self.size):
            if node.data == x and type(node.data) == type(x):
                return idx
            node = node.next
        return None

    def count(self, x):
        result = 0
        node = self.head
        for _ in range(self.size):
            if node.data == x and type(node.data) == type(x):
                result += 1
            node = node.next
        return result

    def reverse(self):
        reversed_list = List()
        node = self.head
        for _ in range(self.size):
            reversed_list.insert(node.data, 0)
            node = node.next
        self.head = reversed_list.head
        self.tail = reversed_list.tail
        return self

    def copy(self):
        copied_list = List()
        node = self.head
        while node:
            copied_list.append(node.data)
            node = node.next
        return copied_list

    def __len__(self):
        if type(self) == List:
            return self.length()
        else:
            return True

    def length(self):
        return self.size


class Node(List):
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

    def __str__(self):
        if type(self.data) == str:
            return "'" + self.data + "'"
        else:
            return str(self.data)