from unittest import TestCase

from seamus.decorator import seamus
from seamus.exceptions import SeamusException
from seamus.seamus import Seamus


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

    def _original_func(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    def _refactored_func(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg2

    @seamus(refactored_func=_refactored_func)
    def _decorated_function(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    @seamus(abcd=_refactored_func)
    def _ill_decorated_function(self, arg1, arg2, kwarg1=None, kwarg2=1):
        return arg1

    def _get_kwargs(self):
        return {'kwarg1': 'test', 'kwarg2': 12}

    def _get_args(self):
        return 1, 2
