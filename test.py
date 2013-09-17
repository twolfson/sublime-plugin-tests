# TODO: Break out fixed content of `add_test` into test suite, allowing `add_test` to be dynamic
from framework import TestSuite

class TestLeftDelete(TestSuite):
    def add_single_test(self):
        # Load in single.input
        with open('example/left_delete/test_files/single.input.py') as f:
            input = f.read()

        # Break up target selection from content
        input_obj = self.__class__.split_sel(input)

        # Load in single.output
        with open('example/left_delete/test_files/single.output.py') as f:
            expected_output = f.read()

        # Break up expected selection from content
        expected_obj = self.__class__.split_sel(expected_output)

        # Save a test reference for later
        self.add_test({
            'target_sel': input_obj['sel'],
            'content': input_obj['content'],
            'expected_sel': expected_obj['sel'],
            'expected_content': expected_obj['content'],
        })


if __name__ == '__main__':
    suite = TestLeftDelete()
    suite.add_single_test()
    suite.run_tests()
