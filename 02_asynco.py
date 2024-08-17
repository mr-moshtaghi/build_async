import time
from collections import deque


# Problem: How to achieve concurrency without threads?
# Issue: Figure out how to switch between tasks?


class Scheduler:
    def __init__(self):
        self.ready = deque()  # Functions ready to execute

    def call_soon(self, func):
        self.ready.append(func)

    def run(self):
        while self.ready:
            func = self.ready.popleft()
            func()


sched = Scheduler()  # Behind scenes scheduler object


def countdown(n):
    if n > 0:
        print("Down", n)
        time.sleep(1)
        sched.call_soon(lambda: countdown(n - 1))


def countup(stop):
    def _run(x):
        if x < stop:
            print("Up", x)
            time.sleep(1)
            sched.call_soon(lambda: _run(x+1))
    _run(0)


sched.call_soon(lambda: countdown(5))
sched.call_soon(lambda: countup(5))
sched.run()

# lambda: countdown(5)
#                        They are similar
# def anonymous_function():
#     countdown(5)
