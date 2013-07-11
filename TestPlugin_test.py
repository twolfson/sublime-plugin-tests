import sublime_plugin


# TODO: This will be a test itself
# TODO: Figure out how to run tests here. we might need our own assertion suite?
class MyTestCommand(sublime_plugin.WindowCommand):
    def run(self):
        with open('tmp.txt', 'w') as f:
            f.write('hello')
