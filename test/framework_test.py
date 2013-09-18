# Load in core dependencies
import os

# Load in local dependencies
from sublime_plugin_tests import framework
from sublime_plugin_tests.utils.selection import split_selection

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


# Define our class
class TestLeftDelete(framework.TestCase):
    @framework.template(__dir__ + '/test_files/plugin.template.py')
    def parse_io_files(self, base_path):
        # Load in input
        with open('%s.input.py' % base_path) as f:
            input = f.read()

        # Break up target selection from content
        input_obj = split_selection(input)

        # Load in single.output
        with open('%s.output.py' % base_path) as f:
            expected_output = f.read()

        # Break up expected selection from content
        expected_obj = split_selection(expected_output)

        # Return collected information
        return {
            'target_sel': input_obj['sel'],
            'content': input_obj['content'],
            'expected_sel': expected_obj['sel'],
            'expected_content': expected_obj['content'],
        }

    def test_left_delete_single(self):
        return self.parse_io_files(__dir__ + '/test_files/single')

    def test_left_delete_multi(self):
        return self.parse_io_files(__dir__ + '/test_files/multi')

    def test_left_delete_multi_collapse(self):
        return self.parse_io_files(__dir__ + '/test_files/multi_collapse')

