import os
import configparser
from typing import Dict, Any
from mbot.core.plugins import (
    plugin,
)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")
config = configparser.ConfigParser()

proxies = {
    "http": "",
    "https": "",
}


def init_config(web_config: dict):
    config.read(config_path)
    config["common"]["target_folder"] = web_config.get("target_folder")
    config["proxy"]["proxy"] = web_config.get("proxy")

    proxies["http"] = web_config.get("proxy")
    proxies["https"] = web_config.get("proxy")

    with open(config_path, "w") as cfg:
        config.write(cfg)


@plugin.config_changed
def config_changed(config: Dict[str, Any]):
    init_config(config)
