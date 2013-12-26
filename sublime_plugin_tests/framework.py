# Load in core dependencies
import os
import unittest

# Load in 3rd party dependencies
from sublime_plugin_tests_base import Base

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


class TestCase(unittest.TestCase):
    def __call__(self, result=None):
        # For each test
        loader = unittest.TestLoader()
        for test_name in loader.getTestCaseNames(self.__class__):
            # Wrap the function
            test_fn = getattr(self, test_name)
            wrapped_test = self._wrap_test(test_fn)
            setattr(self, test_name, wrapped_test)

        # Call the original function
        unittest.TestCase.__call__(self, result)

    def _get_base(self):
        base = getattr(self, 'base', None)
        if not base:
            base = Base(auto_kill_sublime=os.environ.get('SUBLIME_AUTO_KILL', False))
            self.base = base
        return base

    # TODO: Use functools.wrap
    def _wrap_test(self, test_fn):
        # Generate a wrapped function
        def wrapped_fn(*args, **kwargs):
            # Get the test info
            test_str = test_fn(*args, **kwargs)

            # Run the test and process the result
            result = self._get_base().run_test(test_str)
            success = result['success']
            failure_reason = result['meta_info'] or 'Test failed'

            # Assert we were successful
            self.assertTrue(success, failure_reason)

        # Return the wrapped function
        return wrapped_fn
