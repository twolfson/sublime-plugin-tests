# Load in core dependencies
import os
import sublime_plugin

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


class SublimePluginTestTmpCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # On every run, re-import the test class
        # DEV: If we overwrote command.py, Sublime would refuse to run `tmp_test`
        plugin_dict = {}
        execfile(__dir__ + '/plugin_runner.py', plugin_dict, plugin_dict)
        test = plugin_dict['Test']()
        test.run(__dir__)
