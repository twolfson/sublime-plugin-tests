import sublime_plugin


class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        # On every run, re-import the test class
        # DEV: If we overwrote command.py, Sublime would refuse to run `tmp_test`
        from plugin import Test
        test = Test()
        test.run()
