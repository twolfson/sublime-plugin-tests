import os
import sublime
import sys
import traceback


class Test():
    def run(self, __dir__):
        # Placeholder for success and error info
        success = True
        err = None

        # Attempt to perform actions and catch *any* exception
        try:
            # DEV: Due to `import` not immediately picking up changes, we use `execfile` to run what is on disk
            plugin_dict = {}
            execfile(__dir__ + '/plugin.py', plugin_dict, plugin_dict)
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
            with open('{{output_file}}', 'w') as f:
                f.write(output)

            {% if auto_kill_sublime %}
            # Automatically exit out of Sublime
            # DEV: If `sublime_text` is not currently running, then we need to automatically kill the process
            sublime.run_command('exit')
            {% endif %}
