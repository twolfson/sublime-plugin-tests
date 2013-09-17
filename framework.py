# Load in core dependencies
import os
import re
import random
import shutil
import subprocess
import sys
import tempfile
import time
import unittest

# Load in 3rd party dependencies
from jinja2 import Template

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))

# TODO: Break this up into the core (split_sel, run_test) and unittest.TestCase

class TestCase(unittest.TestCase):
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
                raise Exception('We had to update the test launcher plugin. You must close or restart Sublime to continue testing.')
                return False

        # Notify the user that the launcher exists
        return True

    @classmethod
    def ensure_output_dir(cls):
        if not os.path.exists(cls.output_dir):
            os.makedirs(cls.output_dir)

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

    def _wrap_test(self, test_fn):
        # Guarantee there is an output directory and launcher
        self.ensure_launcher()

        # Generate a wrapped function
        def wrapped_fn():
            # Get the test info
            test = test_fn()

            # Reserve an output file
            output_file = tempfile.mkstemp()[1]

            # Template plugin
            plugin = None
            with open('lib/plugin.template.py') as f:
                template = Template(f.read())
                plugin = template.render(target_sel=test['target_sel'],
                                         content=test['content'],
                                         expected_sel=test['expected_sel'],
                                         expected_content=test['expected_content'],
                                         output_file=output_file)

            # Output plugin to directory
            with open(self.scratch_dir + '/plugin.py', 'w') as f:
                # f.write(plugin)
                f.write("""
class Test():
    def run(self):
        print(%s)
                """ % random.randint(0, 1000))

            # Force a delay to allow f.write changes to be picked up
            # TODO: If the delay becomes too significant, attempt batch write -> delay -> batch test
            # TODO: Consider using read + eval

            # Start a subprocess to run the plugin
            # TODO: We might want a development mode (runs commands inside local sublime window) and a testing mode (calls out to Vagrant box)
            # TODO: or at least 2 plugin hooks, one for CLI based testing and one for internal dev
            subprocess.call(['sublime_text', '--command', 'tmp_test'])

            # TODO: How does this work if `tmp_test` is theoretically run in parallel
            # time.sleep(0.3)

            # Read in the output
            with open(output_file) as f:
                # Read and parse the result
                result = f.read()
                result_lines = result.split('\n')
                success = result_lines[0] == 'SUCCESS'
                failure_reason = '\n'.join(result_lines[1:] or ['Test failed'])

                # Assert we were successful
                # TODO: Rather than asserting, move this function elsewhere and return a reason to assert against
                # self.assertTrue(success, failure_reason)

        # Return the wrapped function
        return wrapped_fn

