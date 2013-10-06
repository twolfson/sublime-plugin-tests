import os
import random
import sublime_plugin

__dir__ = os.path.dirname(os.path.abspath(__file__))

def write_file(filename, content):
	f = open(__dir__ + '/' + filename, 'w')
	f.write(content)
	f.close()

class SublimeImportDevCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		# Generate and print a random number
		num = random.randint(0, 10000)
		print(num)

		# Write out a new python file that prints out said random number
		__script = """
from .world import x
hello = %s
""" % num
		write_file('world.py', 'x = 1')
		write_file('test.py', __script)

		# Import and run command
		# from .test import hello
		filepath = __dir__ + '/test.py'
		f = open(filepath)
		script = f.read()
		_globals = globals()
		global_dict['__dir__'] = __dir__
		global_dict['__file__'] = filepath
		global_dict['__name__'] = 'import-scratch-dev.test'
		global_dict['__package__'] = 'import-scratch-dev'
		del global_dict['SublimeImportDevCommand']

		for key, val in global_dict.items():
			print(key, val)
		local_dict = {
		}
		exec(compile(script, 'test.py', 'exec'), global_dict, local_dict)
		print(local_dict['hello'])
		# import importlib
		# print(importlib)
		# print(hello)
