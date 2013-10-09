# Load in core dependencies
import code
import os
import sublime

# Set up constants
__dir__ = os.path.dirname(os.path.abspath(__file__))


def run():
    # On every run, re-import the test class
    # TODO: Determine if this is necessary
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

# TODO: Set timeout loop that checks if `run` has set a global variable
# TODO: This thought was along side a plugin hook so we can guarantee most plugins are loaded
sublime.set_timeout(run, 1000)
