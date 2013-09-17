# Load in core dependencies
import os
import sublime_plugin

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # On every run, re-import the test class
        # DEV: If we overwrote command.py, Sublime would refuse to run `tmp_test`
        sublime_plugin.reload_plugin(__dir__ + '/plugin.py')
        from plugin import Test
        test = Test()
        test.run()
