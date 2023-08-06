import yaml
from moocxing.robot import Constants
import logging
from os import path

log = logging.getLogger(__name__)


DEFAULT = {
    'loglevel': 20,
    'mqtt': {'host': 'mqtt.16302.com', 'post': 1883},
    'minecraft': {'host': 'localhost', 'post': 4711}
}

if not path.isfile(Constants.DEFAULT_CONFIG_PATH):
    f = open(Constants.DEFAULT_CONFIG_PATH, "w")
    yaml.dump(DEFAULT, f)
    f.close()


with open(Constants.DEFAULT_CONFIG_PATH) as f:
    allConfig = yaml.safe_load(f)
    if allConfig is None:
        allConfig = {}


def get(items):
    config = allConfig

    for item in items.split("/"):
        config = config.get(item)

    if config:
        return config
    else:
        log.warning(f"参数不存在：{Constants.DEFAULT_CONFIG_NAME}中没有找到{items}参数")
