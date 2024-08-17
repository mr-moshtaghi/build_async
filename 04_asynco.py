import heapq
import time
from collections import deque


# Problem: How to achieve concurrency without threads?
# Issue: Figure out how to switch between tasks?


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
        self.sleeping.append((deadline, func))
        self.sleeping.sort()  # Sort by closest deadline

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


def countdown(n):
    if n > 0:
        print("Down", n)
        # time.sleep(4)  # Blocking call (nothing else can run)
        sched.call_later(4, lambda: countdown(n - 1))


def countup(stop):
    def _run(x):
        if x < stop:
            print("Up", x)
            # time.sleep(1)
            sched.call_later(1, lambda: _run(x + 1))

    _run(0)


sched.call_soon(lambda: countdown(5))
sched.call_soon(lambda: countup(20))
sched.run()

# lambda: countdown(5)
#                        They are similar
# def anonymous_function():
#     countdown(5)
