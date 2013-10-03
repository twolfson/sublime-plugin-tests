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
        self.set_content('')

    def set_content(self, content):
        """ Set the view content """
        # Localize view
        view = self.view

        # Set the content
        view.run_command('plugin_tests_replace_all', {'content': content})

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
