import sublime
import sublime_plugin

class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # # Load in single.input
        # with open('example/left_delete/test_files/single.input.py') as f:
        #     content = f.read()
        content = 'abc'

        # # Generate new scratch file
        # scratch_view = sublime.active_window().new_file()
        scratch_view = sublime.active_window().active_view()

        # Output single.input to scratch
        insert_edit = scratch_view.begin_edit()
        scratch_view.insert(insert_edit, 0, content)
        scratch_view.end_edit(insert_edit)

        # TODO: Update selection
        # TODO: Run command
        # TODO: Load in single.output
        # TODO: Assert input to output
        # TODO: Assert current selection to output selection
        pass
