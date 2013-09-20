# Load in core dependencies
import os
import shutil
import subprocess
import tempfile
import unittest

# Load in 3rd party dependencies
from jinja2 import Template

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


# Set up helper fn
def template(tmpl_path):
    """ Decorator that templates the returned content. """
    # Pre-emptively read in the template
    tmpl = None
    with open(tmpl_path) as f:
        tmpl = Template(f.read())

    # Define our templating wrapper fn
    def decorator_fn(fn):
        def templator_fn(*args, **kwargs):
            # Run the normal function
            data = fn(*args, **kwargs)

            # Render the info
            return tmpl.render(**data)
        return templator_fn
    return decorator_fn


class Base(object):
    # Determine the plugins directory
    # TODO: Programmatically sniff for this (https://github.com/twolfson/sublime-plugin-tests/issues/4)
    _plugin_test_dir = os.path.expanduser('~/.config/sublime-text-2/Packages/sublime-plugin-tests-tmp')

    @classmethod
    def _ensure_plugin_test_dir(cls):
        # If the plugin test directory does not exist, create it
        if not os.path.exists(cls._plugin_test_dir):
            os.makedirs(cls._plugin_test_dir)

    @classmethod
    def _ensure_launcher(cls):
        # Ensure the plugin test directory exists
        cls._ensure_plugin_test_dir()

        # If command.py doesn't exist, copy it
        orig_command_path = __dir__ + '/command.py'
        dest_command_path = cls._plugin_test_dir + '/command.py'
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
                raise Exception('We had to update the test launcher plugin. You must close or restart Sublime to continue testing.')

        # TODO: Use similar copy model minus the exception
        # TODO: If we overwrite utils, be sure to wait so that changes for import get picked up
        if not os.path.exists(cls._plugin_test_dir + '/utils'):
            shutil.copytree(__dir__ + '/utils', cls._plugin_test_dir + '/utils')

        # Notify the user that the launcher exists
        return True

    @classmethod
    def _run_test(cls, test_str, auto_kill_sublime=False):
        # Guarantee there is an output directory and launcher
        cls._ensure_launcher()

        # Reserve an output file
        output_file = tempfile.mkstemp()[1]

        # Template plugin
        plugin_runner = None
        with open(__dir__ + '/templates/plugin_runner.py') as f:
            runner_template = Template(f.read())
            plugin_runner = runner_template.render(output_file=output_file,
                                                   auto_kill_sublime=auto_kill_sublime)

        # Output plugin_runner to directory
        with open(cls._plugin_test_dir + '/plugin_runner.py', 'w') as f:
            f.write(plugin_runner)

        # Output test to directory
        with open(cls._plugin_test_dir + '/plugin.py', 'w') as f:
            f.write(test_str)

        # Start a subprocess to run the plugin
        # TODO: We might want a development mode (runs commands inside local sublime window) and a testing mode (calls out to Vagrant box)
        # TODO: or at least 2 plugin hooks, one for CLI based testing and one for internal dev
        subprocess.call(['sublime_text', '--command', 'sublime_plugin_test_tmp'])

        # TODO: How does this work if `tmp_test` is theoretically run in parallel

        # Read in the output
        with open(output_file) as f:
            # Read, parse, and return the result
            result = f.read()
            result_lines = result.split('\n')
            return {
                'raw_result': result,
                'success': result_lines[0] == 'SUCCESS',
                'meta_info': '\n'.join(result_lines[1:])
            }


class TestCase(unittest.TestCase, Base):
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
        # Generate a wrapped function
        def wrapped_fn(*args, **kwargs):
            # Get the test info
            test_str = test_fn(*args, **kwargs)

            # Run the test and process the result
            result = self._run_test(test_str,
                                    auto_kill_sublime=os.environ.get('SUBLIME_TESTS_AUTO_KILL', False))
            success = result['success']
            failure_reason = result['meta_info'] or 'Test failed'

            # Assert we were successful
            self.assertTrue(success, failure_reason)

        # Return the wrapped function
        return wrapped_fn

