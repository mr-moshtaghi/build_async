import time
from collections import deque


class Scheduler:
    def __init__(self):
        self.ready = deque()
        self.current = None  # Currently executing generator

    def new_task(self, coro):
        self.ready.append(coro)

    def run(self):
        while self.ready:
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
        time.sleep(1)
        await switch()  # Switch tasks
        n -= 1


async def countup(stop):
    x = 0
    while x < stop:
        print("Up", x)
        time.sleep(1)
        await switch()  # Switch tasks
        x += 1


sched.new_task(countdown(5))
sched.new_task(countup(5))
sched.run()
