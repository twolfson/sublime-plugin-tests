# Load in core dependencies
import os
import random
import re
import shutil
import subprocess
import time

# Load in 3rd party dependencies
from jinja2 import Template

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))

class TestSuite():
    # TODO: It would be nice to pull directory location from Sublime but it isn't critical
    # Determine the scratch plugin directory
    scratch_dir = os.path.expanduser('~/.config/sublime-text-2/Packages/tmp-plugin-tests')
    output_dir = __dir__ + '/output'

    @classmethod
    def split_sel(cls, input):
        """ Break up input string with selection delimiters into selection and content. """

        # Create a placeholder selection
        sel = []

        # Find all indications for selection
        while True:
            # Find the next matching selection
            # TODO: Robustify with multi-char selection and escaping
            match = re.search(r'\|', input)

            # If there was a match
            if match:
                # Save the selection
                start = match.start(0)
                sel.append((start, start))

                # Remove the match from the input
                input = input[:start] + input[match.end(0):]

            # Otherwise, break
            else:
                break

        # Return a selection and content
        return {
            'sel': sel,
            'content': input
        }

    @classmethod
    def ensure_scratch_dir(cls):
        # If the scratch plugins directory does not exist, create it
        if not os.path.exists(cls.scratch_dir):
            os.makedirs(cls.scratch_dir)

    @classmethod
    def ensure_launcher(cls):
        # Ensure the scratch directory exists
        cls.ensure_scratch_dir()

        # If command.py doesn't exist, copy it
        orig_command_path = __dir__ + '/lib/command.py'
        dest_command_path = cls.scratch_dir + '/command.py'
        if not os.path.exists(dest_command_path):
            shutil.copyfile(orig_command_path, dest_command_path)
        else:
        # Otherwise...
            # If there are updates for command.py
            expected_command = None
            with open(orig_command_path) as f:
                expected_command = f.read()
            actual_command = None
            with open(dest_command_path) as f:
                actual_command = f.read()
            if expected_command != actual_command:
                # Update the file
                shutil.copyfile(orig_command_path, dest_command_path)

                # and notify the user we must restart Sublime
                # TODO: We might want to make this even more loud
                print 'We had to update the test launcher plugin. You must close or restart Sublime to continue testing.'
                return False

        # Notify the user that the launcher exists
        return True

    @classmethod
    def ensure_output_dir(cls):
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)

    def __init__(self):
        # Create a placeholder for tests
        self.tests = []

    def add_test(self):
        # TODO: This needs more thought...
        # TODO: Break up framework from add_test. The tests and the framework should be separate notions
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
        self.tests.append({
            'target_sel': input_obj['sel'],
            'content': input_obj['content'],
            'expected_sel': expected_obj['sel'],
            'expected_content': expected_obj['content'],
        })

    def run_tests(self):
        # Guarantee there is an output directory
        self.__class__.ensure_output_dir()

        # For each of the tests
        for i, test in enumerate(self.tests):
            # TODO: Move to tempfile (couldn't get working in first draft)
            # TODO: It should work now with sleep to detect file changes
            # output_file = '%s/%d.txt' % (self.__class__.output_dir, random.randint(0, 10000))
            output_file = '%s/%04d.txt' % (self.__class__.output_dir, i)

            # Template plugin
            plugin = None
            with open('lib/plugin.template.py') as f:
                template = Template(f.read())
                plugin = template.render(target_sel=test['target_sel'],
                                         content=test['content'],
                                         expected_sel=test['expected_sel'],
                                         expected_content=test['expected_content'],
                                         output_file=output_file)

            # # Output plugin to directory
            with open(self.__class__.scratch_dir + '/plugin.py', 'w') as f:
                f.write(plugin)

            # Force a delay to allow f.write changes to be picked up
            # TODO: If the delay becomes too significant, attempt batch write -> delay -> batch test
            time.sleep(0.1)

            # Start a subprocess to run the plugin
            # TODO: We might want a development mode (runs commands inside local sublime window) and a testing mode (calls out to Vagrant box)
            # TODO: or at least 2 plugin hooks, one for CLI based testing and one for internal dev
            subprocess.call(['sublime_text', '--command', 'tmp_test'])

            # Read in the output
            with open(output_file) as f:
                # TODO: Interpret result
                print f.read()

                # TODO: If the result is bad
                    # TODO: Consider breaking early (might be option for run_tests)

        # TODO: Output success/error for each case

        # TODO: Exit appropriately based on results

        # TODO: Break out fixed content of `add_test` into test suite, allowing `add_test` to be dynamic

if __name__ == '__main__':
    suite = TestSuite()
    suite.add_test()
    suite.run_tests()
