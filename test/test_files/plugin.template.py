import sublime

from utils.scratch_view import ScratchView

Region = sublime.Region

def run():
    # Generate new scratch file
    scratch_view = ScratchView()
    try:
        # Injection point for input variables
        content = """{{content}}"""
        target_sel = {{target_sel}}

        # Output single.input to scratch
        scratch_view.set_content(content)

        # Update selection
        scratch_view.set_sel(target_sel)

        # Run command
        scratch_view.run_command('left_delete')

        # Injection point for assertion variables
        expected_content = """{{expected_content}}"""
        expected_sel = {{expected_sel}}

        # Assert input to output
        # TODO: Move to self.assertEqual
        # TODO: One method - Move run to class + run, inherit from unittest.TestCase
        actual_content = scratch_view.get_content()
        error_msg = 'Expected content "%s" does not match actual content "%s"' % (expected_content, actual_content)
        assert expected_content == actual_content, error_msg

        # Assert current selection to output selection
        # TODO: To get full agreement, move to RegionSet?
        # TODO: Make this into a util? (e.g. sublime_utils.to_region_set)
        actual_sel = scratch_view.get_sel()
        error_msg = 'Expected selection "%s" does not match actual selection "%s"' % (expected_sel, actual_sel)
        assert Region(expected_sel[0][0], expected_sel[0][1]) == actual_sel[0], error_msg
    finally:
        # No matter what happens, close the view
        scratch_view.destroy()

