from moocxing.plugins.sdk.AbstractPlugin import AbstractPlugin


class Plugin(AbstractPlugin):
    SLUG = "test"

    def handle(self, query):
        if "剪刀" in query:
            self.say("你好，正在为你准备剪刀")
            # self.serial.send("")
        if "锯子" in query:
            self.say("你好，正在为你准备锯子")
            # self.serial.send("")

    def isValid(self, query):
        return any(word in query for word in ["借", "给", "要"])
