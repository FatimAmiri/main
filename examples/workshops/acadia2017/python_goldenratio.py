""""""
from __future__ import division


def fib_rec(n):
    if n == 0:
        return 0
    if n == 1:
        return 1
    if n == 2:
        return 1
    return fib_rec(n - 1) + fib_rec(n - 2)


def fib_iter(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


numbers_rec = [fib_rec(i) for i in range(20)]
numbers_iter = [fib_iter(i) for i in range(100)]

print numbers_rec
print numbers_iter

print numbers_rec[-2] / numbers_rec[-1]
