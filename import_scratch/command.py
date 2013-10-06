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
import sys
print(globals()['sys'], __name__)
hello = %s
""" % num
		# write_file('world.py', 'x = 1')
		# write_file('test.py', __script)

		# Import and run command
		# from .test import hello
		# TODO: One hack we could do for globals is to `import` then send to exec + compile since they are unlikely to change but it still isn't perfect
		filepath = __dir__ + '/test.py'
		f = open(filepath)
		script = f.read()
		global_dict = {
			'__dir__': __dir__,
			'__file__': filepath,
			'__name__': '%s.test' % __package__,
			'__package__': __package__,
			'__builtins__': __builtins__,
			# '__loader__': __loader__,
		}
		# for key, val in globals().items():
		# 	print(key, val)
		local_dict = {}
		# print('www', exec(compile(script, filepath, 'exec'), global_dict, {}))
		import code
		code.runcode(compile(script, filepath, 'exec'))
		print('www', compile(script, filepath, 'exec').__class__)
		# print(local_dict['hello'], local_dict['x'])
		# import importlib
		# print(importlib)
		# print(hello)
