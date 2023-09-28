from abc import ABC, abstractmethod
from collections import deque
from heapq import heappop, heappush
from itertools import count
from enum import IntEnum
from dataclasses import dataclass

class AbstractIterableMixin(ABC):
    def __len__(self):
        return len(self._items)
    
    def __iter__(self):
        while len(self) > 0:
            yield self.dequeue()

    @abstractmethod
    def enqueue(self):
        pass

    @abstractmethod
    def dequeue(self):
        pass

class MyQueue(AbstractIterableMixin):
    def __init__(self, *items):
        self._items = deque(items)

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        return self._items.popleft()
    
class MyStack(MyQueue):
    def __init__(self, *items):
        self._items = deque(items)

    def dequeue(self):
        return self._items.pop()
    
class MyPriorityQueue(AbstractIterableMixin):
    def __init__(self):
        self._items = []
        self._counter = count()

    def enqueue(self, priority, value):
        item = (priority, next(self._counter), value) # 
        heappush(self._items, item)

    def dequeue(self):
        return heappop(self._items)[-1]

@dataclass
class Message:
    event: str

class Priority(IntEnum):
    # Python's heap implementation uses min-heap
    # i.e. lower numbers = high priority, higher number = lower priority
    CRITICAL = 1
    IMPORTANT = 2
    NEUTRAL = 3

# testing priority queues
wipers = Message("Windshield wipers turned on")
hazard_lights = Message("Hazard lights turned on")
ABS = Message("ABS engaged")
brakes = Message("Brake pedal depressed")
radio = Message("Radio station tuned in")

messages = MyPriorityQueue()
messages.enqueue(Priority.IMPORTANT, hazard_lights)
messages.enqueue(Priority.NEUTRAL, wipers)
messages.enqueue(Priority.CRITICAL, ABS)
messages.enqueue(Priority.CRITICAL, brakes)
messages.enqueue(Priority.NEUTRAL, radio)

for message in messages:
    print(message)