class Seamus:
    def __init__(self, comparator=None):
        self._original_func = None
        self._original_func_args = None
        self._original_func_kwargs = None
        self._refactored_func = None
        self._refactored_func_args = None
        self._refactored_func_kwargs = None
        if comparator is None:
            self._comparator = self._default_comparator
        else:
            self._comparator = comparator

    def use(self, original_func, *args, **kwargs):
        self._original_func = original_func
        self._original_func_args = args
        self._original_func_kwargs = kwargs

    def test(self, refactored_func, *args, **kwargs):
        self._refactored_func = refactored_func
        self._refactored_func_args = args
        self._refactored_func_kwargs = kwargs

    def run(self):
        actual_result = self._original_func(*self._original_func_args, **self._original_func_kwargs)
        test_result = self._refactored_func(*self._refactored_func_args, **self._original_func_kwargs)
        self._create_report(actual_result, test_result)
        return actual_result

    def _create_report(self, actual_result, test_result):
        is_equal = self._comparator(actual_result, test_result)
        self._publish(is_equal)

    @staticmethod
    def _default_comparator(actual_result, test_result):
        return actual_result == test_result

    def _publish(self, is_equal):
        pass
