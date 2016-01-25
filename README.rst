seamus
======
.. image:: https://api.travis-ci.org/nerandell/seamus.svg?branch=master
    :target: https://travis-ci.org/nerandell/seamus
.. image:: https://badge.fury.io/py/seamus.svg
    :target: https://pypi.python.org/pypi/seamus
.. image:: https://coveralls.io/repos/nerandell/seamus/badge.svg?branch=master&service=github 
    :target: https://coveralls.io/github/nerandell/seamus?branch=master
.. image:: https://readthedocs.org/projects/seamus/badge/?version=latest
    :target: http://seamus.readthedocs.org/en/latest/?badge=latest
    :alt: Documentation Status

Python library that makes testing refactored code super simple. Inspired by scientist_ from github. The goal of `seamus` is to make testing of refactored code easy. Let's say that you decide to refactor a method in your code.
But if your code is running in production environment, it is too risky to roll out the refactored code directly. `seamus` comes to rescue here. You can use it with plenty of options offered to strategically test your refactored code in background leaving your end users unaffected. Once you are sure that the refactored code is behaving as expected, then you can roll it out.

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
any callable which returns an extended ``Seamus`` class or atleast quack like ``Seamus`` class (at your own risk).

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
            
By default, to compare the result returned by actual and the refactored function, ``seamus`` uses ``==`` operator. 
However you can easily override it by passing comparator as an argument and it can return a ``true`` or a ``false`` value based on your own logic.

.. code-block:: python

    from seamus import Seamus
    
    class SeamusExample:
    
        def add_numbers(self, num1, num2):
            result = self._original_func(num1, num2)
            return result
    
        @seamus(refactored_func=_refactored_func, comparator=lambda x, y: x + 1 == y)
        def _original_func(self, num1, num2):
            return num1 + 2 * num2 - num2 
    
        def _refactored_func(self, num1, num2):
            return num1 + num2
            
By default, both the functions are run everytime, but what if you have to run the refactored version only a few times?
You can do that by providing a strategy.

.. code-block:: python

    from seamus import Seamus
    
    class SeamusExample:
    
        def add_numbers(self, num1, num2):
            result = self._original_func(num1, num2)
            return result
    
        @seamus(refactored_func=_refactored_func, run_strategy=lambda: random() > 0.5)
        def _original_func(self, num1, num2):
            return num1 + 2 * num2 - num2 
    
        def _refactored_func(self, num1, num2):
            return num1 + num2

In the above exmaple, the refactored version will only run 50% of the time.

Documentation
-------------
Documentation is available here_

.. _here : http://seamus.readthedocs.org

License
-------
``seamus`` is offered under the MIT license.

Source code
-----------
The latest developer version is available in a github repository:
https://github.com/nerandell/seamus
