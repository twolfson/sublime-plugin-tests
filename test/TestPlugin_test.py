import unittest
import subprocess


class BasicTest(unittest.TestCase):
    def test_one_is_one(self):
        cmd = '''
        with f as open('tmp.txt'):
            f.write('hello')
        '''
        print cmd
        subprocess.call(['sublime_text', '--command', 'exec {"cmd": "touch": "args": "abc"}' % cmd])
