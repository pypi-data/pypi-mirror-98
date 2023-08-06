from moocxing.robot import LoadPlugin
from moocxing.robot import Constants


class Brain():
    def __init__(self, SKILL, PLUGIN_PATH=None):
        if PLUGIN_PATH is not None:
            Constants.PLUGIN_PATH = PLUGIN_PATH
    
        self.plugins = LoadPlugin.loadPlugin(SKILL)

    def query(self, text, _print=False):
        if _print:
            print(text)
        for plugin in self.plugins:
            if not plugin.isValid(text):
                continue
            plugin.handle(text)
            return True
        return False
