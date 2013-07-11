import sublime_plugin


class WriteToFileCommand(sublime_plugin.WindowCommand):
    def run(self):
        with open('tmp.txt', 'w') as f:
            f.write('hello')


class TestPluginCommand(sublime_plugin.WindowCommand):
    def run(self):
        print 'Hello World!'
