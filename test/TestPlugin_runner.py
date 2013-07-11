import unittest
import subprocess

# TODO: Current vision...
# nosetests loads a test runner file
# could require users to have test hook command
# but... why not define our own commands inside of test framework? o_o
# which import ...
# never mind, the plugin should be accessible inside of sublime text already
# so we can do all of our run commands if necessary
# TODO: we still need to think about how to handle prompts. probably override them somehow.
# whether it is at the sublime level or class level (getattr, setattr)
# this is necessary because I don't think we can force selection in a quick panel listing


# TODO: This will be part of the framework
class BasicTest(unittest.TestCase):
    def test_one_is_one(self):
        subprocess.call(['sublime_text', '--command', 'my_test'])
