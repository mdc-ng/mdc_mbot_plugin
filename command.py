import logging
import os
import requests
import shutil
from mbot.core.plugins import (
    plugin,
    PluginCommandContext,
    PluginCommandResponse,
)
from mbot.openapi import mbot_api
from .config import *


server = mbot_api
_LOGGER = logging.getLogger(__name__)

lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "libmdc_ng.so")
lib_path_new = lib_path + ".new"


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


def mdc_main(path: str, config: str = config_path):
    from plugins.mdc_mbot_plugin import libmdc_ng

    libmdc_ng.main(path, config)


def download_file(url, name):
    with requests.get(url, proxies=proxies, stream=True) as r:
        with open(name, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return name
