import sublime_plugin
import random


class TmpTestCommand(sublime_plugin.ApplicationCommand):
    def run(self):
        print random.randint(0, 10000)
        # from plugin import Test
        # test = Test()
        # test.run()
