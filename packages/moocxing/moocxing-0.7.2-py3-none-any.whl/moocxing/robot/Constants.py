import os

PATH = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

APP_PATH = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), os.pardir))

PLUGIN_PATH = os.path.join(APP_PATH, "plugins/")
ROBOT_PATH = os.path.join(APP_PATH, "robot/")
STATIC_PATH = os.path.join(APP_PATH, ROBOT_PATH, "static/")
TEMP_PATH = os.path.join(APP_PATH, ROBOT_PATH, "temp/")
MUSIC_PATH = os.path.join(APP_PATH, "music/")

DEFAULT_CONFIG_NAME = 'default.yaml'
CUSTOM_CONFIG_NAME = 'config.yaml'

DEFAULT_CONFIG_PATH = os.path.join(STATIC_PATH, DEFAULT_CONFIG_NAME)
CUSTOM_CONFIG_PATH = os.path.join(STATIC_PATH, CUSTOM_CONFIG_NAME)

