# Producer-consumer problem
# Challenge: How to implement the same functionality, but no threads.
import time
from collections import deque
import heapq


class Scheduler:
    def __init__(self):
        self.ready = deque()  # Functions ready to execute
        self.sleeping = []  # Sleeping functions
        self.sequence = 0

    def call_soon(self, func):
        self.ready.append(func)

    def call_later(self, delay, func):
        self.sequence += 1
        deadline = time.time() + delay  # Expiration time
        # Priority queue
        heapq.heappush(self.sleeping, (deadline, self.sequence, func))

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                # Find the nearest deadline
                deadline, _, func = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(func)

            while self.ready:
                func = self.ready.popleft()
                func()


sched = Scheduler()  # Behind scenes scheduler object


# -------------

class AsyncQueue:
    def __init__(self):
        self.items = deque()
        self.waiting = deque()   # All getters waiting for data

    def put(self, item):
        self.items.append(item)
        if self.waiting:
            func = self.waiting.popleft()
            # Do we call it right away
            sched.call_soon(func)
            # func()  ----> might get deep calls, recursion , etc.

    def get(self, callback):
        # Wait until an item is available. Then return it
        # ???????
        if self.items:
            callback(self.items.popleft())
        else:
            self.waiting.append(lambda: self.get(callback))


def producer(q, count):
    for n in range(count):
        print("Producing", n)
        q.put(n)
        time.sleep(1)

    print("Producer done")
    q.put(None)  # "Sentinel" to shut down


def consumer(q):
    while True:
        item = q.get()  # <<<<<<<<<<< PROBLEM: Waiting
        if item is None:
            break
        print("Consuming", item)
    print("Consumer done")
