import sublime_plugin


class TestPluginCommand(sublime_plugin.WindowCommand):
    def run(self):
        print 'Hello World!'
