from os import path
import re
import sublime
import sublime_plugin

__dir__ = path.dirname(path.abspath(__file__))
Region = sublime.Region

class TmpTestCommand(sublime_plugin.ApplicationCommand):
    @classmethod
    def split_sel(cls, input):
        # Create a placeholder selection
        # TODO: Consider moving to RegionSet over list
        sel = []

        # Find all indications for selection
        while True:
            # Find the next matching selection
            # TODO: Robustify with multi-char selection and escaping
            match = re.search(r'\|', input)

            # If there was a match
            if match:
                # Save the selection
                start = match.start(0)
                sel.append(Region(start, start))

                # Remove the match from the input
                input = input[:start] + input[match.end(0):]

            # Otherwise, break
            else:
                break

        # Return a selection and content
        return {
            'sel': sel,
            'content': input
        }

    def run(self):
        # Load in single.input
        with open(__dir__ + '/example/left_delete/test_files/single.input.py') as f:
            input = f.read()

        print self.__class__.split_sel(input)

        # Break up target selection from content
        target_sel = [sublime.Region(7, 7)]
        # content = """def abc():
#     pass
# """

        return

        # Generate new scratch file
        # view = sublime.active_window().new_file()
        view = sublime.active_window().active_view()

        # # Output single.input to scratch
        # edit = view.begin_edit()
        # view.insert(edit, 0, content)
        # view.end_edit(edit)

        # # Update selection
        # # DEV: Attribution to sublime-invert-selection
        # view.sel().clear()
        # for region in target_sel:
        #     view.sel().add(region)

        # # Run command
        # view.run_command('left_delete')

        # Load in single.output
        with open(__dir__ + '/example/left_delete/test_files/single.output.py') as f:
            expected_content = f.read()

        # Break up expected selection from content
        expected_sel = [sublime.Region(6, 6)]
        expected_content = """def ab():
    pass
"""

        # Assert input to output
        file_region = sublime.Region(0, view.size())
        actual_content = view.substr(file_region)
        assert expected_content == actual_content

        # Assert current selection to output selection
        actual_sel = view.sel()
        assert expected_sel[0] == actual_sel[0]
