# Load in core dependencies
import os
import sublime
import sublime_plugin

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


class SublimePluginTestTmpCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # On every run, re-import the test class
        # DEV: Sublime Text does not recognize changes to command.py.
        # DEV: Once it is loaded and run once via CLI, it is locked in memory until Sublime Text is restarted
        plugin_dict = {
        }
        # DEV: In Python 2.x, use execfile. In 3.x, use compile + exec.
        # http://stackoverflow.com/a/437857
        # TODO: Make this feature detection
        # if getattr(__builtins__, 'execfile', None):
        if sublime.version() < '3000':
            execfile(__dir__ + '/plugin_runner.py', plugin_dict, plugin_dict)
        else:
            # TODO: This importer definitely lags behind
            from .plugin_runner import Test
            plugin_dict['Test'] = Test
        test = plugin_dict['Test']()
        test.run(__dir__)
