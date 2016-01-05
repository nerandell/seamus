class Seamus:
    """
    Main class responsible for handling the test.
    """
    def __init__(self, comparator=None, run_strategy=None):
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

        if run_strategy is None:
            # Always run the test
            self._strategy = lambda: True
        else:
            self._strategy = run_strategy
        print(self._strategy)

    def use(self, original_func, *args, **kwargs):
        """
        Sets the function that is actually run. The return value
        of this function is what will actually be returned when the
        test is run
        :param original_func: The function that is supposed to return the final result
        :param args: Will be passed to the original_func as arguments
        :param kwargs: Will be passed to the original_func as keyword arguments
        """
        self._original_func = original_func
        self._original_func_args = args
        self._original_func_kwargs = kwargs

    def test(self, refactored_func, *args, **kwargs):
        """
        Sets the test function that will actually be run. The return value of this function
        will be compared to the actual result and publish called with the comparison made.j
        :param refactored_func: The function that is supposed to return the final result
        :param args: Will be passed to the refactored_func as arguments
        :param kwargs: Will be passed to the refactored_func as keyword arguments
        """
        self._refactored_func = refactored_func
        self._refactored_func_args = args
        self._refactored_func_kwargs = kwargs

    def run(self):
        """
        Run the test
        :return: Result of original_func
        """
        actual_result = self._original_func(*self._original_func_args, **self._original_func_kwargs)
        if self._strategy():
            test_result = self._refactored_func(*self._refactored_func_args, **self._original_func_kwargs)
            self._create_report(actual_result, test_result)
        return actual_result

    def _create_report(self, actual_result, test_result):
        is_equal = self._comparator(actual_result, test_result)
        self.publish(is_equal)

    @staticmethod
    def _default_comparator(actual_result, test_result):
        return actual_result == test_result

    def publish(self, is_equal):
        """
        :param is_equal: The value returned by self._comparator which compares values
        returned by _original_func and _refactored_func
        """
        pass
