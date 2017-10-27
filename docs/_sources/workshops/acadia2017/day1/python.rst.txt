.. _acadia2017_day1_python:

********************************************************************************
Python
********************************************************************************

The compas framework is based on Python.
Python 3 is fully supported and the code is backwards compatible with Python +2.6.


* https://docs.python.org/3/library/index.html
* https://docs.python.org/3/howto/index.html


* http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html
* https://jeffknupp.com/blog/2012/10/04/writing-idiomatic-python/
* https://gist.github.com/JeffPaine/6213790


* https://python-3-patterns-idioms-test.readthedocs.io/en/latest/
* http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html
* https://docs.python.org/3.0/whatsnew/3.0.html
* https://wiki.python.org/moin/Python2orPython3


Built-in types and functions
============================

* https://docs.python.org/3/library/stdtypes.html
* https://docs.python.org/3/library/functions.html

**Types**

* numeric types: :obj:`int`, :obj:`float`, :obj:`complex`
* sequence types: :obj:`list`, :obj:`tuple`, :obj:`range`
* text sequence type: :obj:`str`
* set types: :obj:`set`, :obj:`frozenset`
* mapping types: :obj:`dict`

**Functions**

* enumerate: ``for i, item in enumerate(items): print(i, item)``
* format
* iter
* len: ``if len(items) == 2: print('not a valid face')``
* next
* open
* range ``for i in range(len(items)): print(i, items[i])``
* sorted


Containers
==========

List
----

https://docs.python.org/3/library/stdtypes.html#lists

* Ordered items of any type.
* **Mutable**

.. code-block:: python

    items = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

.. code-block:: python

    # indexing & slicing

    items[0]     # 0  
    items[-1]    # 9

    items[:5]    # [0, 1, 2, 3, 4]
    items[5:]    # [5, 6, 7, 8, 9]

    items[::-1]  # [9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    items[::2]   # [0, 2, 4, 6, 8]

.. code-block:: python

    # methods

    items = [0, 1, 2, 3, 4, 5]

    items.append(6)                  # [1, 2, 3, 4, 5, 6]
    items.insert(0, 0)               # [0, 1, 2, 3, 4, 5, 6]
    items.extend([7, 8, 9, 10, 11])  # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]
    items.pop()                      # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    items.remove(-1)                 # [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]


List comprehensions
-------------------

Generate lists with an expression in brackets.

.. code-block:: python

    # list construction

    numbers = [n for n in range(10)]
    odd     = [n for n in range(10) if n % 2 == 1]
    even    = [n for n in range(10) if n % 2 == 0]
    squares = [n ** 2 for n in range(10)]
    even    = [n if n % 2 == 0 else None for n in range(10)]

.. code-block:: python

    # flattening



.. code-block:: python

    # vector length

    vector = [1.0, 0.0]
    length = sum([x ** 2 for x in vector]) ** 0.5

.. code-block:: python

    # dot product

    vectors = [[1.0, 0.0], [0.0, 1.0]]
    dot = sum([a * b for a, b in zip(* vectors)])

.. code-block:: python

    # centroid

    points = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    centroid = [sum(axis) / len(vertices) for axis in zip(* vertices)]


Tuple
-----

https://docs.python.org/3/library/stdtypes.html#tuples

* Ordered items of any type.
* **Immutable**

.. code-block:: python

    rgb = 255, 0, 0

    r = rgb[0]  # 255
    g = rgb[1]  # 0
    b = rgb[2]  # 0

.. code-block:: python

    rgb[0] = 0
    rgb[1] = 255


Set
---

https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

* Unordered, distinct, hashable objects.
* **Mutable**

.. code-block:: python

    items = set([1, 2, 3, 4])


Dictionary
----------

https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

* Maps unordered, distinct, hashable values (*keys*) to arbitrary objects
* **Mutable**

.. code-block:: python

    items = {'1': 1, '2': 2, '3': 3, '4': 4}

    for key in items:
        print key, items[key]

    for key in items.keys():
        print key, items[key]

    for key, value in items.items():
        print key, value

    for value in items.values():
        print value

.. code-block:: python

    # pop
    # popitem
    # setdefault
    # get

.. code-block:: python

    # sort dictionary based on values


Dict comprehensions
-------------------

.. code-block:: python

    items = {index: value for index, value in enumerate(range(10))}


Examples
--------


Functions
=========

.. code-block:: python

    def f():
        pass

    def f(a):
        pass

    def f(a, b):
        pass

    def f(a, b=None):
        print(a, b)

    # f('a')      => 'a', None
    # f('a', 'b') => 'a', 'b' 

    def f(*args):
        print(args)

    # f('a')           => ['a']
    # f('a', 'b', 'c') => ['a', 'b', 'c']

    def f(**kwargs):
        pass

    def f(a, b, *args):
        pass

    def f(a, b, *args, **kwargs):
        pass

Example
-------


Classes
=======

.. code-block:: python

    class Vector():

        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z


Script, Module, Package
=======================

.. code-block:: python

    # simple script

    a = 1
    b = 2
    c = a + b

    print c


.. code-block:: python

    # script vs. module

    def f1():
        ...

    def f2():
        ...

    if __name__ == '__main__':
        # this part is only executed when the module is run as a script
        # this part does not get executed when the module is imported
        # all other code will get executed when the module is imported!

        f1()
        f2()
