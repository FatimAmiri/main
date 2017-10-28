.. _acadia2017_day1_python:

********************************************************************************
Python
********************************************************************************

.. note::

    The compas framework is based on Python.
    Python 3 is fully supported and the code is backwards compatible with Python +2.6.


Resources
=========

**Python**

* `Python 3: standard library <https://docs.python.org/3/library/index.html>`_
* `Python 3: how-to guides <https://docs.python.org/3/howto/index.html>`_

**Idiomatic Python**

* `Code Like a Pythonista: Idiomatic Python <http://python.net/~goodger/projects/pycon/2007/idiomatic/handout.html>`_
* `Transforming Code into Beautiful, Idiomatic Python <https://gist.github.com/JeffPaine/6213790>`_
* `Python 3 Patterns, Recipes and Idioms <https://python-3-patterns-idioms-test.readthedocs.io/en/latest/>`_

**Python 2 vs 3**

* `What's New in Python 3 <https://docs.python.org/3.0/whatsnew/3.0.html>`_
* `The key differences between Python 2.7.x and Python 3.x with examples <http://sebastianraschka.com/Articles/2014_python_2_3_key_diff.html>`_
* `Should I use Python 2 or Python 3 for my development activity? <https://wiki.python.org/moin/Python2orPython3>`_

**Other**

* `Python Reference (The Right Way) <http://python-reference.readthedocs.io/en/latest/index.html>`_


Built-in types and functions
============================

**Types**

* https://docs.python.org/3/library/stdtypes.html

================== ======================================== ====================
numeric types      :obj:`int`, :obj:`float`, :obj:`complex` ``int(1)``, ``float(1)``, ``complex(1)``
sequence types     :obj:`list`, :obj:`tuple`, :obj:`range`  ``[0, 1]``, ``(0, 1)``, ``range(1)``
text sequence type :obj:`str`                               ``'hello'``
set types          :obj:`set`, :obj:`frozenset`             ``set([0, 1, 2])``, ``frozenset([0, 1, 2])``
mapping types      :obj:`dict`                              ``dict(zero=0, one=1)``
================== ======================================== ====================


**Functions**

* https://docs.python.org/3/library/functions.html

.. code-block:: python

    # enumerate
    
    for i, item in enumerate(items):
        print(i, item)

    # format
    
    format(3.14159, '.3f')

    # len

    if len(vertices) == 2:
        print('not a valid face')

    # open

    f = open('faces.obj', 'r')

    # range

    numbers = range(10)

    # sorted

    sorted([str(i) for i in range(10)], key=int)

    # zip
    
    zip(* [[1, 2, 3], [1, 2, 3], [1, 2, 3]])


Containers
==========

* https://docs.python.org/3.6/tutorial/datastructures.html
* https://docs.python.org/3.6/library/collections.html
* https://docs.python.org/3.6/library/collections.abc.html

====== ============================ =============================================================== ==============
type   example                      description                                                     operations
====== ============================ =============================================================== ==============
list   [1, 2, 3, 4]                 Contains ordered arbitrary objects.                             iterate, index, slice, modify
tuple  (1, 2, 3, 4)                 Contains ordered arbitrary objects.                             iterate, index, slice
set    set([1, 2, 3, 4])            Contains unordered, distinct, hashable objects.                 iterate, modify
dict   dict(one=1, two=2, three=3)  Maps unordered distinct hashable objects to arbitrary objects.  iterate, modify 
====== ============================ =============================================================== ==============


List
----

https://docs.python.org/3/library/stdtypes.html#lists

.. code-block:: python

    items = [0, 1, 2, 3]

    # iterate

    for item in items:
        print(item)

    # index

    items[0]     # 0  
    items[-1]    # 3

    # slice

    items[:2]    # [0, 1]
    items[2:]    # [2, 3]

    items[::-1]  # [3, 2, 1, 0]
    items[::2]   # [0, 2]

    # modify

    items.append(4)          # [0, 1, 2, 3, 4]
    items.insert(0, -1)      # [-1, 0, 1, 2, 3, 4]
    items.extend([5, 6, 7])  # [-1, 0, 1, 2, 3, 4, 5, 6, 7]
    items.pop()              # 7
    items.remove(-1)         # [0, 1, 2, 3, 4, 5, 6]


List comprehensions
-------------------

Generate lists with an expression in brackets.

.. code-block:: python

    # list construction

    numbers = [n for n in range(10)]

    # filtering

    even = [n for n in numbers if n % 2 == 0]

    # function mapping

    squares = [pow(n, 2) for n in numbers]

    # flattening

    nested = [[1, 2, 3], [1, 2, 3], [1, 2, 3]]
    flat   = [n for numbers in nested for n in numbers]

    # geometry

    points = [[0.0, 0.0], [1.0, 0.0], [1.0, 1.0], [0.0, 1.0]]
    centroid = [sum(axis) / len(points) for axis in zip(* points)]


Tuple
-----

https://docs.python.org/3/library/stdtypes.html#tuples

.. code-block:: python

    rgb = 255, 0, 0

    # iterate

    for color in rgb:
        print(color)

    # index

    rgb[0]  # 255
    rgb[1]  # 0
    rgb[2]  # 0

    # slice

    rgb[1:]   # (0, 0)
    rgb[:-1]  # (255, 0)


Set
---

https://docs.python.org/3/library/stdtypes.html#set-types-set-frozenset

.. code-block:: python

    items = set([1, 1, 2, 3, 3, 4])

    # iterate

    for item in items:
        print(item)

    # modify

    items.add(5)
    items.add(5)
    items.remove(2)


Dictionary
----------

https://docs.python.org/3/library/stdtypes.html#mapping-types-dict

.. code-block:: python

    items = dict(one=1, two=2, three=3)

    # iterate

    for key in items:
        print(key, items[key])

    for key in items.keys():
        print(key, items[key])

    for key, value in items.items():
        print(key, value)

    for value in items.values():
        print(value)

    # modify

    items['zero'] = 0
    items.pop('zero')
    items.popitem()
    items.setdefault('four', 4)

    items.get('five', 5)


Dict comprehensions
-------------------

.. code-block:: python

    items = {index: value for index, value in enumerate(range(10))}


Exercise
--------

Compute the connectivity of a set of lines defined by pairs of point coordinates.


**Lines**

* :download:`lines.json </../../examples/workshops/acadia2017/lines.json>`
* :download:`lines_big.json </../../examples/workshops/acadia2017/lines_big.json>`
* :download:`lines_bigger.json </../../examples/workshops/acadia2017/lines_bigger.json>`


**Approach 1.** Compare the distances between points

* :download:`python_comparison.py </../../examples/workshops/acadia2017/python_comparison.py>`

.. code-block:: python

    import json

    with open('lines.json', 'r') as f:
        lines = json.load(f)

    print(len(lines))

    tol = 0.001

    vertices = []
    edges = []

    for sp, ep in lines:

        # do something magical here


    # verify the result

    print(len(lines) == len(edges))
    print(len(edges)) == len(set(edges))


**Approach 2.** Map points to locations

* :download:`python_geomap.py </../../examples/workshops/acadia2017/python_geomap.py>`

.. code-block:: python

    import json

    with open('lines.json', 'r') as f:
        lines = json.load(f)

    print(len(lines))

    tol = '3f'

    vertexdict = {}
    edges = []

    for sp, ep in lines:

        # do something magical here


    # verify the result

    print(len(lines) == len(edges))
    print(len(edges)) == len(set(edges))


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


Exercise
--------

Compute an approximation of the golden ratio using a reecursive fobonacci function.

* :download:`goldenratio.py </../../examples/workshops/acadia2017/python_goldenratio.py>`

.. code-block:: python

    def fib(n):
        if n == 0:
            return 0
        if n == 1:
            return 1
        if n == 2:
            return 1
        return fib(n - 1) + fib(n - 2)

    numbers = [fib(i) for i in range(10)]
    ratio = numbers[-2] / numbers[-1]


Classes
=======

.. code-block:: python

    class Vector(object):

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
