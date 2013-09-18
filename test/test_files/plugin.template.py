def run():
    # Generate new scratch file
    scratch_view = ScratchView()
    try:
        # Injection point for input variables
        # TODO: For linting, it might be good to place variables in separate template that are imported
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
        actual_content = scratch_view.get_content()
        error_msg = 'Expected content "%s" does not match actual content "%s"' % (expected_content, actual_content)
        assert expected_content == actual_content, error_msg

        # Assert current selection to output selection
        # TODO: To get full agreement, move to RegionSet?
        actual_sel = scratch_view.get_sel()
        error_msg = 'Expected selection "%s" does not match actual selection "%s"' % (expected_sel, actual_sel)
        assert Region(expected_sel[0][0], expected_sel[0][1]) == actual_sel[0], error_msg
    finally:
        # No matter what happens, close the view
        # TODO: I would like the case of sugar to take care of this automatically
        # TODO: Maybe we keep track of views on ScratchView at the class level and auto-clean on complete
        scratch_view.destroy()

