from unittest import TestCase
from unittest.mock import MagicMock
from random import random

from seamus.decorator import seamus
from seamus.exceptions import SeamusException
from seamus.seamus import Seamus


class ExtendedSeamus(Seamus):
    def publish(self, is_equal):
        print(is_equal)


class TestSeamus(TestCase):
    def setUp(self):
        self._seamus = Seamus()

    def test_use_function(self):
        self._seamus.use(self._original_func, *self._get_args(), **self._get_kwargs())
        self.assertEqual(self._seamus._original_func, self._original_func)
        self.assertEqual(self._seamus._original_func_args, (1, 2))
        self.assertEqual({'kwarg1': 'test', 'kwarg2': 12}, self._seamus._original_func_kwargs)

    def test_test_function(self):
        self._seamus.test(self._refactored_func, *self._get_args(), **self._get_kwargs())
        self.assertEqual(self._seamus._refactored_func, self._refactored_func)
        self.assertEqual(self._seamus._refactored_func_args, (1, 2))
        self.assertEqual({'kwarg1': 'test', 'kwarg2': 12}, self._seamus._refactored_func_kwargs)

    def test_run_function(self):
        self._seamus.use(self._original_func, *self._get_args(), **self._get_kwargs())
        self._seamus.test(self._refactored_func, *self._get_args(), **self._get_kwargs())
        result = self._seamus.run()
        self.assertEqual(result, 1)

    def test_decorator(self):
        self.assertEqual(self._decorated_function(*self._get_args(), **self._get_kwargs()), 1)

    def test_decorator_with_insufficient_args(self):
        self.assertRaises(SeamusException, self._ill_decorated_function, *self._get_args(), **self._get_kwargs())

    def test_publish(self):
        self._seamus.publish = MagicMock(return_value=3)
        self._seamus.use(self._original_func, *self._get_args(), **self._get_kwargs())
        self._seamus.test(self._refactored_func, *self._get_args(), **self._get_kwargs())
        self._seamus.run()
        self._seamus.publish.assert_called_with(True)

    def test_publish_for_extended_class(self):
        self._seamus = ExtendedSeamus()
        self._seamus.publish = MagicMock(return_value='test')
        self._seamus.use(self._original_func, *self._get_args(), **self._get_kwargs())
        self._seamus.test(self._refactored_func, *self._get_args(), **self._get_kwargs())
        self._seamus.run()
        self._seamus.publish.assert_called_with(True)

    def test_strategy(self):
        self.assertEqual(self._decorated_function_with_strategy(*self._get_args(), **self._get_kwargs()), 1)

    def test_publish_for_decorator_with_factory(self):
        self.assertEqual(self._decorated_function_with_factory(*self._get_args(), **self._get_kwargs()), 1)

    def test_comparator(self):
        self._seamus = Seamus(comparator=lambda x, y: x + 1 == y)
        self._seamus.publish = MagicMock(return_value='test')
        self._seamus.use(self._original_func, *self._get_args(), **self._get_kwargs())
        self._seamus.test(self._refactored_func, *self._get_args(), **self._get_kwargs())
        self._seamus.run()
        self._seamus.publish.assert_called_with(False)

    def _original_func(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    def _refactored_func(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    @seamus(refactored_func=_refactored_func)
    def _decorated_function(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    @seamus(abcd=_refactored_func)
    def _ill_decorated_function(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    @seamus(refactored_func=_refactored_func, factory=ExtendedSeamus)
    def _decorated_function_with_factory(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    @seamus(refactored_func=_refactored_func, run_strategy=lambda: random() > 0.5)
    def _decorated_function_with_strategy(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    def _get_kwargs(self):
        return {'kwarg1': 'test', 'kwarg2': 12}

    def _get_args(self):
        return 1, 2
