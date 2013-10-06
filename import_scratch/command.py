import os
import random
import sublime_plugin

__dir__ = os.path.dirname(os.path.abspath(__file__))

class SublimeImportDevCommand(sublime_plugin.ApplicationCommand):
	def run(self):
		# Generate and print a random number
		num = random.randint(0, 10000)
		print(num)

		# Write out a new python file that prints out said random number
		__script = """
hello = %s
""" % num
		__f = open(__dir__ + '/test.py', 'w')
		__f.write(__script)
		__f.close()

		# Import and run command
		# from .test import hello
		f = open(__dir__ + '/test.py')
		script = f.read()
		python_dict = {}
		exec(compile(script, 'test.py', 'exec'), python_dict, python_dict)
		print(python_dict['hello'])
		# import importlib
		# print(importlib)
		# print(hello)
