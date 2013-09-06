from os import path
import re
import sublime
import sublime_plugin

__dir__ = path.dirname(path.abspath(__file__))
Region = sublime.Region

class ScratchView:
    def __init__(self, window=None):
        # Fallback window to active window
        if not window:
            window = sublime.active_window()

        # Generate and save new view
        self.view = window.new_file()

    def run_command(self, *args, **kwargs):
        """ Run command `run_command` against view """
        return self.view.run_command(*args, **kwargs)

    def clear_content(self):
        """ Clear out view content """
        # Localize view
        view = self.view

        # Generate an edit to clear out the view
        edit = view.begin_edit()
        view.erase(edit, Region(0, view.size()))
        view.end_edit(edit)

    def set_content(self, content):
        """ Set the view content """
        # Localize view
        view = self.view

        # Clear out content
        self.clear_content()

        # Set the content
        edit = view.begin_edit()
        view.insert(edit, 0, content)
        view.end_edit(edit)

    def get_content(self):
        """ Get view content """
        # Localize view
        view = self.view

        # Generate a region for the entire file
        file_region = sublime.Region(0, view.size())

        # Return the text contained by the file region
        return view.substr(file_region)

    def clear_sel(self):
        """ Clear out view selection """
        self.view.sel().clear()

    def set_sel(self, regions):
        """ Set view selection via RegionSet """
        # Clear out selection
        self.clear_sel()

        # Add each region to selection RegionSet
        # DEV: Attribution to sublime-invert-selection
        sel = self.view.sel()
        for region in regions:
            sel.add(region)

    def get_sel(self):
        """ Get view selection """
        return self.view.sel()

    def destroy(self):
        """ Close view """
        # Clear out content
        # DEV: Empty the view to prevent a prompt on close
        self.clear_content()

        # Focus and close view
        view = self.view
        view.window().focus_view(view)
        view.window().run_command('close')


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

        # Break up target selection from content
        input_obj = self.__class__.split_sel(input)
        target_sel = input_obj['sel']
        content = input_obj['content']

        # Generate new scratch file
        scratch_view = ScratchView()

        # Output single.input to scratch
        scratch_view.set_content(content)

        # Update selection
        scratch_view.set_sel(target_sel)

        # Run command
        scratch_view.run_command('left_delete')

        # Load in single.output
        with open(__dir__ + '/example/left_delete/test_files/single.output.py') as f:
            expected_output = f.read()

        # Break up expected selection from content
        expected_obj = self.__class__.split_sel(expected_output)
        expected_sel = expected_obj['sel']
        expected_content = expected_obj['content']

        # Run assertions (catching errors)
        try:
            # Assert input to output
            actual_content = scratch_view.get_content()
            error_msg = 'Expected content "%s" does not match actual content "%s"' % (expected_content, actual_content)
            assert expected_content == actual_content, error_msg

            # Assert current selection to output selection
            actual_sel = scratch_view.get_sel()
            error_msg = 'Expected content "%s" does not match actual content "%s"' % (expected_content, actual_content)
            assert expected_sel[0] == actual_sel[0], error_msg
        except Exception as err:
        # If an error occurs, panic.
            # TODO: Panic
            print err
        finally:
        # Always, close the view
            scratch_view.destroy()
