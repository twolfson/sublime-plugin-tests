import sublime
import sublime_plugin

class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # Load in single.input
        with open('example/left_delete/test_files/single.input.py') as f:
            content = f.read()

        # Generate new scratch file
        # view = sublime.active_window().new_file()
        view = sublime.active_window().active_view()

        # # Output single.input to scratch
        # edit = view.begin_edit()
        # view.insert(edit, 0, content)
        # view.end_edit(edit)

        # Update selection
        target_sels = [sublime.Region(7, 7)]
        # content = """
        # def abc():
        #     pass
        # """
        # DEV: Attribution to sublime-invert-selection
        view.sel().clear()
        for target_sel in target_sels:
            view.sel().add(target_sel)

        # TODO: Run command
        # TODO: Load in single.output
        # TODO: Assert input to output
        # TODO: Assert current selection to output selection
        pass
