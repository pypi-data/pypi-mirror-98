from moocxing.plugins.sdk.AbstractPlugin import AbstractPlugin


class Plugin(AbstractPlugin):
    SLUG = "home"

    def handle(self, query):
        if "开" in query:
            order = "ON"
        elif "关" in query:
            order = "OFF"

        if "灯" in query:
            if "客厅" in query:
                self.mqtt.PUB("/anzhi/switch/state", order)

        if "空调" in query:
            self.mqtt.PUB("/anzhi/led/state", order)

    def isValid(self, query):
        return any(word in query for word in ["开", "关"])
