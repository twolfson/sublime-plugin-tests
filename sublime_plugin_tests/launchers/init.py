# Load in core dependencies
import code
import os
import sublime
import sublime_plugin

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


# Set up hook for set timeout loop
plugin_host_loaded = False


class SublimePluginTestTmpCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        global plugin_host_loaded
        plugin_host_loaded = True
        # On every run, re-import the test class
        # DEV: Sublime Text does not recognize changes to command.py.
        # DEV: Once it is loaded and run once via CLI, it is locked in memory until Sublime Text is restarted
        filepath = __dir__ + '/plugin_runner.py'
        plugin_dict = {
            '__dir__': __dir__,
            '__file__': filepath,
            '__name__': '%s.plugin_runner' % __package__,
            '__package__': __package__,
            '__builtins__': __builtins__,
        }

        # DEV: In Python 2.x, use execfile. In 3.x, use compile + exec.
        # if getattr(__builtins__, 'execfile', None):
        if sublime.version() < '3000':
            execfile(filepath, plugin_dict, plugin_dict)
        else:
            f = open(filepath)
            script = f.read()
            interpretter = code.InteractiveInterpreter(plugin_dict)
            interpretter.runcode(compile(script, filepath, 'exec'))
        test = plugin_dict['Test']()
        test.run(__dir__)


def run():
    # Attempt to run our plugin
    sublime.run_command('sublime_plugin_test_tmp')

    # If it did not run (plugin_host has not loaded), then try again in 100ms
    global plugin_host_loaded
    if not plugin_host_loaded:
        sublime.set_timeout(run, 100)
run()
