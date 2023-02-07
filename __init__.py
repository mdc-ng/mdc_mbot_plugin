import logging
from mbot.core.plugins import (
    plugin,
    PluginMeta,
)
from typing import Dict, Any
from .command import *
from .config import *
from .event import *

_LOGGER = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


@plugin.after_setup
def after_setup(plugin_meta: PluginMeta, config: Dict[str, Any]):
    init_config(config)

    try:
        if not os.path.isfile(lib_path):
            update_lib()

        from plugins.mdc_mbot_plugin import libmdc_ng

        _LOGGER.info("MDC基础库加载成功, 当前版本: %s" % libmdc_ng.version())
    except Exception as e:
        _LOGGER.error(e)
        _LOGGER.error("MDC基础库加载失败, 请尝试在插件管理页面配置代理、手动更新MDC lib, 成功后重启容器")
