import sublime_plugin

class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # TODO: Load in single.input
        with open('example/left_delete/test_files/single.input.py') as f:
            print f.read()
        # TODO: Generate new scratch file
        # TODO: Output single.input to scratch
        # TODO: Update selection
        # TODO: Run command
        # TODO: Load in single.output
        # TODO: Assert input to output
        # TODO: Assert current selection to output selection
        pass
