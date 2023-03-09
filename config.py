import logging
from typing import Dict, Any
from mbot.core.plugins import (
    plugin,
)

_LOGGER = logging.getLogger(__name__)

proxies = {
    "http": "",
    "https": "",
}

watch_folder = []

target_folder = ""


def init_config(web_config: dict[str, str]):
    global watch_folder, target_folder, proxies

    to_watch = web_config.get("watch_folder")
    if to_watch:
        watch_folder = [folder.split(":") for folder in to_watch.split(",")]
        logging.info("MDC插件已启用, 监视文件夹: %s" % watch_folder)

    target_folder = web_config.get("target_folder") or ""

    proxy = web_config.get("proxy") or ""
    proxies["http"] = proxy
    proxies["https"] = proxy


@plugin.config_changed
def config_changed(config: Dict[str, Any]):
    init_config(config)
