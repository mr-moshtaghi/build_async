def countdown(n):
    while n > 0:
        yield n
        n -= 1


for x in countdown(5):
    print("T-minus", x)

c = countdown(5)
print(next(c))
print(next(c))
