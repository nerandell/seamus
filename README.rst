seamus
======
.. image:: https://api.travis-ci.org/nerandell/seamus.svg?branch=master
    :target: https://travis-ci.org/nerandell/seamus
.. image:: https://badge.fury.io/py/seamus.svg
    :target: https://pypi.python.org/pypi/seamus

Python library that makes testing refactored code super simple. Inspired by scientist_ from github. The goal of `seamus` is to make testing of refactored code easy. Let's say that you decide to refactor a method in your code.
But if your code is running in production environment, it is too risky to roll out the refactored code directly. `seamus` comes to rescue here. You can use it with plenty of options offered to stragically test your refactored code in background leaving your end users unaffected. Once you are sure that the refactored code is behaving as expected, then you can roll it out.

.. _scientist: https://github.com/github/scientist

Requirements
------------
- Python >= 3.2

Installation
------------

`seamus` can be installed via pip

.. code-block:: bash

    $ pip install seamus

It can also be installed from source:

.. code-block:: bash

    $ git clone https://github.com/nerandell/seamus
    $ cd seamus && python setup.py install
    
Usage
-----
Here is a simple example : 

.. code-block:: python

    from seamus import Seamus
    
    class SeamusExample:
    
        def add_numbers(self, num1, num2):
            seamus = Seamus()
            seamus.use(self._original_func, num1, num2)
            seamus.test(self._refactored_func, num1, num2)
            result = seamus.run()
            return result
    
        def _original_func(self, num1, num2):
            return num1 + 2 * num2 - num2 
    
        def _refactored_func(self, num1, num2):
            return num1 + num2
    
It is that simple. The result returned is always the actual result. However the refactored code is run by `seamus` in background and variety of inferences can be made on the basis of information obtained.

However there is still a lot of boilerplate code here. To make things simpler, you can also use the decorator:

.. code-block:: python

    from seamus import seamus
    
    class SeamusExample:
    
        def add_numbers(self, num1, num2):
            result = self._original_func(num1, num2)
            return result
    
        @seamus(refactored_func=_refactored_func)
        def _original_func(self, num1, num2):
            return num1 + 2 * num2 - num2 
    
        def _refactored_func(self, num1, num2):
            return num1 + num2

This makes the code concise. However currenly, ``seamus`` doesn't do a lot with the result. To make some use of the result, you have to override the publish method provided by ``Seamus`` class. 

.. code-block:: python
    
    from seamus import Seamus
    
    class ExtendedSeamus(Seamus):

        def publish(self, is_equal):
            print(is_equal)
    
    class SeamusExample:

        def add_numbers(self, num1, num2):
            seamus = ExtendedSeamus()
            seamus.use(self._original_func, num1, num2)
            seamus.test(self._refactored_func, num1, num2)
            result = seamus.run()
            return result
    
        def _original_func(self, num1, num2):
            return num1 + 2 * num2 - num2 
    
        def _refactored_func(self, num1, num2):
            return num1 + num2

You can also use the decorator with ``factory`` argument. ``factory`` can be just about
any callable which returns an extended ``Seamus`` class or atleast duck-type ``Seamus`` class (at your own risk).

.. code-block:: python

    from seamus import Seamus
    
    class ExtendedSeamus(Seamus):

        def publish(self, is_equal):
            print(is_equal)
    
    class SeamusExample:
    
        def add_numbers(self, num1, num2):
            result = self._original_func(num1, num2)
            return result
    
        @seamus(refactored_func=_refactored_func, factory=ExtendedSeamus)
        def _original_func(self, num1, num2):
            return num1 + 2 * num2 - num2 
    
        def _refactored_func(self, num1, num2):
            return num1 + num2

License
-------
``seamus`` is offered under the MIT license.

Source code
-----------
The latest developer version is available in a github repository:
https://github.com/nerandell/seamus
