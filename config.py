import logging
import os
import configparser
from typing import Dict, Any
from mbot.core.plugins import (
    plugin,
)

_LOGGER = logging.getLogger(__name__)

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")

proxies = {
    "http": "",
    "https": "",
}

watch_folder = []


def init_config(web_config: dict):
    global watch_folder, proxies
    config = configparser.ConfigParser()
    config.read(config_path)

    to_watch = web_config.get("watch_folder")
    if to_watch:
        watch_folder = to_watch.split(",")
        logging.info("MDC插件已启用, 监视文件夹: %s" % watch_folder)

    if not config.has_section("common"):
        config.add_section("common")
    config["common"]["target_folder"] = web_config.get("target_folder") or ""

    if not config.has_section("proxy"):
        config.add_section("proxy")

    proxy = web_config.get("proxy") or ""
    config["proxy"]["proxy"] = proxy
    proxies["http"] = proxy
    proxies["https"] = proxy

    with open(config_path, "w") as cfg:
        config.write(cfg)


@plugin.config_changed
def config_changed(config: Dict[str, Any]):
    init_config(config)
