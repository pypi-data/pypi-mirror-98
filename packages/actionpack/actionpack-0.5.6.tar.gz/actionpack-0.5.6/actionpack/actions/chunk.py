from actionpack import Action
from actionpack.utils import Container

from collections import deque
from typing import Callable
from typing import Iterator
from typing import Iterable


class Chunk(Action):

    def __init__(self, iterable: Iterable, size: int):
    #def __init__(self, iterable: Callable[[], Iterable], size: int):
        self.container = Container(iterable)
        self.size = size
        self.exhausted = False

    def instruction(self):
        if self.exhausted:
            raise StopIteration(f'{self} iterator exhausted.')

        iterator = iter(self.container)
        while iterator:
            collection = []
            for _ in range(self.size):
                try:
                    collection.append(next(iterator))
                except StopIteration:
                    self.exhausted = True
                    if collection:
                        yield iter(collection)
                    return
            yield iter(collection)

    #def __iter__(self):
    #    return self.iterator

    #def __next__(self):
    #    try:
    #        print(type(self.collection))
    #        return next(self.collection)
    #    except StopIteration:
    #        self.exhausted = True

