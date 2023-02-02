from mbot.core.plugins import (
    plugin,
    PluginCommandContext,
    PluginCommandResponse,
    PluginMeta,
)
from mbot.openapi import mbot_api
import logging
import os
from typing import Dict, Any

server = mbot_api
_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libmdc_ng.so")
lib_path_new = lib_path + ".new"


@plugin.after_setup
def after_setup(plugin_meta: PluginMeta, config: Dict[str, Any]):
    if not os.path.isfile(lib_path):
        update_lib()

    from plugins.mdc_mbot_plugin import libmdc_ng

    _LOGGER.info("MDC基础库加载成功, 当前版本: %s" % libmdc_ng.version())


@plugin.command(
    name="update",
    title="更新MDC",
    desc="拉取最新MDC lib",
    icon="AlarmOn",
    run_in_background=True,
)
def update(ctx: PluginCommandContext):
    update_lib()

    _LOGGER.info("MDC基础库更新成功, 重启容器后生效")
    return PluginCommandResponse(True, "更新成功")


def update_lib():
    download_file(
        "https://github.com/mdc-ng/mdc-ng/releases/download/latest/libmdc_ng.so",
        lib_path_new,
    )
    try:
        os.remove(lib_path)
    except:
        pass
    os.rename(lib_path_new, lib_path)


config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.ini")


def mdc_main(path: str, config: str = config_path):
    from plugins.mdc_mbot_plugin import libmdc_ng

    libmdc_ng.main(path, config)


import requests
import shutil


def download_file(url, name):
    with requests.get(url, stream=True) as r:
        with open(name, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return name
