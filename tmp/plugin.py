import sublime_plugin


class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        from plugin_dynamic import TmpTest
        tmp = TmpTest()
        tmp.run()
