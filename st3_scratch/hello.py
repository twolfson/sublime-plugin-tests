import sublime_plugin

f = open('/tmp/hey2', 'w')
f.write('hello')
f.close()

class TmpTestHeyCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        f = open('/tmp/hey', 'w')
        f.write('hello')
        f.close()
