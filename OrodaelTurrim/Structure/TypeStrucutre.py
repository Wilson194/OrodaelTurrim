from typing import Any, Union


class TwoWayDict(dict):
    def __setitem__(self, key, value):
        # Remove any previous connections with these values
        if key in self:
            del self[key]
        if value in self:
            del self[value]
        dict.__setitem__(self, key, value)
        dict.__setitem__(self, value, key)


    def __delitem__(self, key):
        dict.__delitem__(self, self[key])
        dict.__delitem__(self, key)


    def __len__(self):
        """Returns the number of connections"""
        return dict.__len__(self) // 2


class DoubleLinkedList:
    def __init__(self):
        self.__head = None  # type: Node
        self.__tail = None  # type: Node
        self.__pointer = None  # type: Node
        self.__size = 0  # type: int


    def push_back(self, value: Any) -> None:
        node = Node(value)

        if self.__size == 0:
            self.__head = node
            self.__tail = node
        else:
            node.previous = self.__head
            node.previous.next = node
            self.__head = node

        self.__size += 1


    def push_front(self, value: Any) -> None:
        node = Node(value)
        node.next = self.__tail
        self.__tail = node

        self.__size += 1


    def empty(self) -> bool:
        return self.__size == 0


    @property
    def head(self) -> "Node":
        return self.__head


    @property
    def tail(self) -> "Node":
        return self.__tail


    @property
    def value(self):
        if self.__pointer is None:
            raise KeyError('Pointer not set')
        return self.__pointer.value


    def next(self):
        self.__pointer = self.__pointer.next


    def previous(self):
        self.__pointer = self.__pointer.previous


    @property
    def pointer(self):
        return self.__pointer


    @pointer.setter
    def pointer(self, value):
        self.__pointer = value


    def __sizeof__(self):
        return self.__size


    def __bool__(self):
        return not self.empty()


class Node:
    def __init__(self, data: Any = None):
        self.__data = data
        self.__next = None
        self.__previous = None


    @property
    def value(self) -> Any:
        return self.__data


    @property
    def next(self) -> Union["Node", None]:
        return self.__next


    @next.setter
    def next(self, value: "Node"):
        self.__next = value


    @property
    def previous(self) -> Union["Node", None]:
        return self.__previous


    @previous.setter
    def previous(self, value: "Node"):
        self.__previous = value
