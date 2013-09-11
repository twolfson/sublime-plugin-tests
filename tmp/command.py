import sublime_plugin


class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        from plugin import Test
        test = Test()
        test.run()
