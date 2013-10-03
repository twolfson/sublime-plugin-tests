import os
import sublime
import sys
import traceback

class Test():
    def run(self, __dir__):
        # Placeholder for success and error info
        success = True
        err = None

        print('waaa')

        # Attempt to perform actions and catch *any* exception
        try:
            # DEV: Due to `import` not immediately picking up changes, we use `execfile` to run what is on disk
            plugin_dict = {
                '__name__': 'plugin',
                '__file__': './plugin.pyc',
                '__package__': None
            }
            # TODO: Make this feature detection
            # TODO: Something something try imputil, something something http://www.afpy.org/doc/python/2.7/library/imputil.html
            # if getattr(__builtins__, 'execfile', None):
            if sublime.version() < '3000':
                execfile(__dir__ + '/plugin.py', plugin_dict, plugin_dict)
            else:
                print('om nom')
                f = open(__dir__ + '/plugin.py')
                plugin_py = compile(f.read(), __dir__ + '/plugin.py', 'exec')
                f.close()
                eval(plugin_py, plugin_dict, plugin_dict)
                print('om 2nom')
            plugin_dict['run']()
        except Exception:
        # If an error occurs, record it
            success = False
            exc_type, exc_value, exc_traceback = sys.exc_info()
            err = ''.join(traceback.format_exception(exc_type,
                                                     exc_value,
                                                     exc_traceback))
        finally:
        # Always...
            # Write out success/failure and any meta data
            output = 'SUCCESS' if success else 'FAILURE'
            if err:
                output += '\n%s' % err
            f = open('{{output_file}}', 'w')
            f.write(output)
            f.close()

            {% if auto_kill_sublime %}
            # Automatically exit out of Sublime
            # DEV: If `sublime_text` is not currently running, then we need to automatically kill the process
            sublime.run_command('exit')
            {% endif %}
