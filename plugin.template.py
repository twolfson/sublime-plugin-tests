import sys
import traceback
import sublime
import sublime_plugin

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
            # If the region is not a region, upcast it as one
            if isinstance(region, (tuple, list)):
                region = Region(region[0], region[1])

            # Add the region
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


class Test():
    def run(self):
        # Generate new scratch file
        scratch_view = ScratchView()

        # Injection point for input variables
        content = """{{content}}"""
        target_sel = {{target_sel}}

        # Output single.input to scratch
        scratch_view.set_content(content)

        # Update selection
        scratch_view.set_sel(target_sel)
        print 'hi2'
        # Run command
        scratch_view.run_command('left_delete')

        # Injection point for assertion variables
        expected_content = """{{expected_content}}"""
        expected_sel = {{expected_sel}}

        # Run assertions (catching errors)
        success = True
        err = None
        try:
            # Assert input to output
            actual_content = scratch_view.get_content()
            error_msg = 'Expected content "%s" does not match actual content "%s"' % (expected_content, actual_content)
            assert expected_content == actual_content, error_msg

            # Assert current selection to output selection
            # TODO: To get full agreement, move to RegionSet?
            actual_sel = scratch_view.get_sel()
            error_msg = 'Expected selection "%s" does not match actual selection "%s"' % (expected_sel, actual_sel)
            assert Region(expected_sel[0][0], expected_sel[0][1]) == actual_sel[0], error_msg
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
            with open("{{output_file}}", 'w') as f:
                f.write(output)

            # Close the view
            scratch_view.destroy()
