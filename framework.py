# Load in core dependencies
import os
import random
import re
import shutil
import subprocess
import sys
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

    def add_test(self, test):
        # TODO: Assert content exists for template?
        # TODO: Maybe template now to allow for running *anything* as test?
        # TODO: Scratch that. We *need* to be able to specify output_file as the test itself is run in parallel
        self.tests.append(test)

    def run_tests(self):
        # Guarantee there is an output directory
        self.__class__.ensure_output_dir()

        # For each of the tests
        results = []
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

            # TODO: How does this work if `tmp_test` is theoretically run in parallel

            # Read in the output
            with open(output_file) as f:
                # Read and parse the result
                result = f.read()
                result_lines = result.split('\n')
                success = result_lines[0] == 'SUCCESS'

                # Save the info
                results.append({
                    # 'name': test['name'],
                    'name': 'left_delete/test_files/single',
                    'success_str': result_lines[0],
                    'success': success,
                    'meta_info': result_lines[1:],
                    'raw_result': result,
                })

                # TODO: If the result is bad
                    # TODO: Consider breaking early (might be option for run_tests)

        # TODO: The following behavior should be conditional on options. We can return results for further exploration
        # TODO: It would be practical to use a reporter here (e.g. TAP, xunit)
        # Output success/error for each case
        for i, result in enumerate(results):
            # Output the result and its info
            print '%s: %s' % (result['success_str'], result['name'])
            for line in result['meta_info']:
                print '  %s' % line

        # TODO: Exit appropriately based on results
        result_failures = map(lambda x: not result['success'], results)
        exit_code = 1 if any(result_failures) else 0
        sys.exit(exit_code)
