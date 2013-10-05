import os
import sublime
import sublime_plugin
import sys
import traceback


class PluginTestsReplaceAllCommand(sublime_plugin.TextCommand):
    def run(self, edit, content=''):
        view = self.view
        view.replace(edit, sublime.Region(0, view.size()), content)


class Test():
    def run(self, __dir__):
        # Placeholder for success and error info
        success = True
        err = None

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
                import importlib
                importlib.invalidate_caches()
                from .plugin import run
                plugin_dict['run'] = run
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
            print('www', output)
            if err:
                output += '\n%s' % err
            f = open('{{output_file}}', 'w')
            f.write(output)
            f.close()


            import time
            time.sleep(1)

            {% if auto_kill_sublime %}
            # Automatically exit out of Sublime
            # DEV: If `sublime_text` is not currently running, then we need to automatically kill the process
            sublime.run_command('exit')
            {% endif %}
