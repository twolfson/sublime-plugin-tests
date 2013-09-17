# TODO: Break out fixed content of `add_test` into test suite, allowing `add_test` to be dynamic
# TODO: I strongly dislike not having a loose single file BDD framework (e.g. mocha, jasmine)
from framework import TestCase

class TestLeftDelete(TestCase):
    def parse_io_files(self, base_path):
        # Load in input
        with open('%s.input.py' % base_path) as f:
            input = f.read()

        # Break up target selection from content
        input_obj = self.split_sel(input)

        # Load in single.output
        with open('%s.output.py' % base_path) as f:
            expected_output = f.read()

        # Break up expected selection from content
        expected_obj = self.split_sel(expected_output)

        # Return collected information
        return {
            'target_sel': input_obj['sel'],
            'content': input_obj['content'],
            'expected_sel': expected_obj['sel'],
            'expected_content': expected_obj['content'],
        }

    def test_left_delete_single(self):
        return self.parse_io_files('example/left_delete/test_files/single')

