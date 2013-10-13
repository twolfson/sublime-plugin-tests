# Load in core dependencies
import os
import shutil
import subprocess
import time
import tempfile
import unittest

# Load in 3rd party dependencies
from jinja2 import Template

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))
SUBLIME_TEXT_VERSION = os.environ.get('SUBLIME_TEXT_VERSION', None)


# TODO: Consider using a proper logger
class Logger(object):
    def debug(self, msg):
        pass

    def info(self, msg):
        pass

    def warn(self, msg):
        pass
logger = Logger()


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
    if SUBLIME_TEXT_VERSION == '3.0':
        _plugin_test_dir = os.path.expanduser('~/.config/sublime-text-3/Packages/sublime-plugin-tests-tmp')

    # TODO: Fallback should be determined by sublime_info package
    _sublime_command = os.environ.get('SUBLIME_COMMAND', 'sublime_text')
    print _sublime_command

    @classmethod
    def _ensure_plugin_test_dir(cls):
        # If the plugin test directory does not exist, create it
        if not os.path.exists(cls._plugin_test_dir):
            os.makedirs(cls._plugin_test_dir)

    @classmethod
    def _ensure_utils(cls):
        # Ensure the plugin test directory exists
        cls._ensure_plugin_test_dir()

        # TODO: Use similar copy model minus the exception
        # TODO: If we overwrite utils, be sure to wait so that changes for import get picked up
        if not os.path.exists(cls._plugin_test_dir + '/utils'):
            shutil.copytree(__dir__ + '/utils', cls._plugin_test_dir + '/utils')

    @classmethod
    def _install_command_launcher(cls):
        # Guarantee the plugin test dir exists
        cls._ensure_plugin_test_dir()

        # If command launcher doesn't exist, copy it
        orig_command_path = __dir__ + '/launchers/command.py'
        dest_command_path = cls._plugin_test_dir + '/command_launcher.py'
        if not os.path.exists(dest_command_path):
            shutil.copyfile(orig_command_path, dest_command_path)
        else:
        # Otherwise...
            # If there are updates for command launcher
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

    _init_launcher_path = _plugin_test_dir + '/init_launcher.py'

    @classmethod
    def _remove_init_launcher(cls):
        # If the init launcher exists, delete it
        if os.path.exists(cls._init_launcher_path):
            os.unlink(cls._init_launcher_path)

    @classmethod
    def _install_init_launcher(cls):
        # Guarantee the plugin test dir exists
        cls._ensure_plugin_test_dir()

        # Clean up any past instances of init launcher
        cls._remove_init_launcher()

        # Install a new one
        # TODO: Verify this doesn't have any double invocation consequences
        orig_command_path = __dir__ + '/launchers/init.py'
        shutil.copyfile(orig_command_path, cls._init_launcher_path)

    @classmethod
    def _run_test(cls, test_str, auto_kill_sublime=False):
        # Guarantee there is an output directory and launcher
        cls._ensure_utils()

        # Reserve an output file
        output_file = tempfile.mkstemp()[1]

        # Template plugin
        plugin_runner = None
        f = open(__dir__ + '/templates/plugin_runner.py')
        runner_template = Template(f.read())
        plugin_runner = runner_template.render(output_file=output_file,
                                               auto_kill_sublime=auto_kill_sublime)
        f.close()

        # Output plugin_runner to directory
        f = open(cls._plugin_test_dir + '/plugin_runner.py', 'w')
        f.write(plugin_runner)
        f.close()

        # Output test to directory
        f = open(cls._plugin_test_dir + '/plugin.py', 'w')
        f.write(test_str)
        f.close()

        # TODO: These commands should go in a launching harness
        # If we are running Sublime Text 3 and it has not yet started, use `init`
        running_via_init = False
        if SUBLIME_TEXT_VERSION == '3.0':
            # TODO: Use tasklist for Windows
            # Get process list
            child = subprocess.Popen(["ps", "ax"], stdout=subprocess.PIPE)
            ps_list = child.stdout.read()

            # Kill the child
            child.kill()

            # Determine if Sublime Text is running
            # TODO: This could be subl, sublime_text, or other
            sublime_is_running = False
            for process in ps_list.split('\n'):
                if cls._sublime_command in process:
                    sublime_is_running = True
                    break

            # If sublime isn't running, use our init trigger
            logger.debug('Current process list: %s' % ps_list)
            if not sublime_is_running:
                # Install the init trigger
                cls._install_init_launcher()

                # and launch sublime_text
                logger.info('Launching %s via init' % cls._sublime_command)
                subprocess.call([cls._sublime_command])

                # Mark the init to prevent double launch
                running_via_init = True

        # Otherwise, use `--command` trigger
        # TODO: Can we consolidate these? `init` might work in *all* cases and allow us to move around the plugin locking in as with `--command`
        if not running_via_init:
            # Install the command launcher
            cls._install_command_launcher()

            # Start a subprocess to run the plugin
            logger.info('Launching %s via --command' % cls._sublime_command)
            subprocess.call([cls._sublime_command, '--command', 'sublime_plugin_test_tmp'])

        # Wait for the output file to exist
        while (not os.path.exists(output_file) or os.stat(output_file).st_size == 0):
            logger.debug('Waiting for %s to exist / have size' % output_file)
            time.sleep(0.1)

        # If we used the init command
        if running_via_init:
            # Clean up
            cls._remove_init_launcher()

            # and if Sublime was not running, wait for it to terminate
            if not sublime_is_running:
                while True:
                    sublime_is_still_running = False
                    # TODO: Modularize this
                    child = subprocess.Popen(["ps", "ax"], stdout=subprocess.PIPE)
                    ps_list = child.stdout.read()

                    # Kill the child
                    child.kill()

                    # TODO: Output ps_list to a debug file
                    logger.debug('Current process list: %s' % ps_list)

                    for process in ps_list.split('\n'):
                        if cls._sublime_command in process:
                            sublime_is_still_running = True

                    if not sublime_is_still_running:
                        break
                    else:
                        logger.debug('Waiting for %s to terminate' % cls._sublime_command)
                        time.sleep(0.1)

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
