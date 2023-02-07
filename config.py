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

    if not config.has_section("common"):
        config.add_section("common")
    config["common"]["target_folder"] = web_config.get("target_folder") or ""

    if not config.has_section("proxy"):
        config.add_section("proxy")

    proxy = web_config.get("proxy") or ""
    config["proxy"]["proxy"] = proxy
    proxies["http"] = proxy
    proxies["https"] = proxy

    if not config.has_section("watermark"):
        config.add_section("watermark")

    config["watermark"]["enabled"] = str(web_config.get("watermark")) or "0"
    config["watermark"]["start"] = str(web_config.get("watermark_start")) or "0"
    config["watermark"]["clockwise"] = str(web_config.get("watermark_clockwise")) or "0"

    with open(config_path, "w") as cfg:
        config.write(cfg)


@plugin.config_changed
def config_changed(config: Dict[str, Any]):
    init_config(config)
