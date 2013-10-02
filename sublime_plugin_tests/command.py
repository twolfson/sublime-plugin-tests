# Load in core dependencies
import os
import sublime_plugin

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


class SublimePluginTestTmpCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # On every run, re-import the test class
        # DEV: Sublime Text does not recognize changes to command.py.
        # DEV: Once it is loaded and run once via CLI, it is locked in memory until Sublime Text is restarted
        plugin_dict = {}
        execfile(__dir__ + '/plugin_runner.py', plugin_dict, plugin_dict)
        test = plugin_dict['Test']()
        test.run(__dir__)
