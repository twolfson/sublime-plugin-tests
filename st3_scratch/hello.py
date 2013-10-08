import sublime_plugin

class TmpTestHeyCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        f = open('/tmp/hey', 'w')
        f.write('hello')
        f.close()
