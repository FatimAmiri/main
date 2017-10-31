""""""
from __future__ import division


def fib_rec(n):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    return fib_rec(n - 1) + fib_rec(n - 2)


def fib_itr(n):
    a, b = 0, 1
    for i in range(n):
        a, b = b, a + b
    return a


def fib_mem(n, memo={}):
    if n == 0:
        return 0
    if n == 1 or n == 2:
        return 1
    if n not in memo:
        memo[n] = fib_mem(n - 1, memo) + fib_mem(n - 2, memo)
    return memo[n]


numbers_rec = [fib_rec(i) for i in range(10)]
numbers_itr = [fib_itr(i) for i in range(50)]
numbers_mem = [fib_mem(i) for i in range(50)]

print numbers_rec
print numbers_itr
print numbers_mem

ratio = numbers_mem[0] / numbers_mem[1]

for i in range(2, 49):
    r = numbers_mem[i] / numbers_mem[i + 1]
    if r == ratio:
        print i, ratio
        break
    ratio = r
