import unittest
import subprocess


class BasicTest(unittest.TestCase):
    def test_one_is_one(self):
        subprocess.call(['sublime_text', '--command', 'test_plugin'])
