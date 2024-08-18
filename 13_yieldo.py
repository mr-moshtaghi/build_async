import time
from collections import deque
import heapq


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.sleeping = []
        self.current = None  # Currently executing generator
        self.sequence = 0

    async def sleep(self, delay):
        # The current "coroutine" wants to sleep. How ??
        deadline = time.time() + delay
        self.sequence += 1
        heapq.heappush(self.sleeping, (deadline, self.sequence, self.current))
        self.current = None
        await switch()  # Switch tasks

    def new_task(self, coro):
        self.ready.append(coro)

    def run(self):
        while self.ready or self.sleeping:
            if not self.ready:
                deadline, _, coro = heapq.heappop(self.sleeping)
                delta = deadline - time.time()
                if delta > 0:
                    time.sleep(delta)
                self.ready.append(coro)
            self.current = self.ready.popleft()
            # Drive as a generator
            try:
                self.current.send(None)  # Send to a coroutine . In Python, when a generator or coroutine is suspended,
                # we can send a value to it using the send method and resume it. To activate a coroutine, we must first
                # send a value with send. If this value is None, the coroutine continues its activity,
                # starting from where it stopped.
                if self.current:
                    self.ready.append(self.current)
            except StopIteration:
                pass


sched = Scheduler()  # Background scheduler object


class Awaitable:
    def __await__(self):  # This method tells Python that this object is awaited and that it can use await .
        yield  # This yield creates a generator object that allows Python to delay code execution and then suspend.


def switch():
    return Awaitable()


"""

In Python, awaitable objects are objects that can be awaited using the await keyword inside an async function.
For an object to be awaitable, it must meet one of the following two conditions:

    1. Implement the __await__ Method: The object must implement the __await__ method,
     which returns a generator or an awaitable object.
    2. Implement the __aenter__ and __aexit__ Methods: For objects that are used as context managers in async with,
     these methods must be implemented.

"""


async def countdown(n):
    while n > 0:
        print("Down", n)
        await sched.sleep(4)
        n -= 1


async def countup(stop):
    x = 0
    while x < stop:
        print("Up", x)
        await sched.sleep(1)
        x += 1


sched.new_task(countdown(5))
sched.new_task(countup(5))
sched.run()
