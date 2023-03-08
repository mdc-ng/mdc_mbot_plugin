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
        if os.path.isfile(bin_path):
            run_command(
                [
                    "./mdc_ng",
                    "-v",
                ],
                True,
                cwd=pathlib.Path(__file__).parent.absolute(),
            )
        else:
            _LOGGER.error("MDC基础库加载失败, 请尝试在插件管理页面配置代理、手动更新MDC lib")

        if os.path.isfile(backend_path):
            start_server()

    except Exception as e:
        _LOGGER.error(e)
        _LOGGER.error("MDC基础库加载失败, 请尝试在插件管理页面配置代理、手动更新MDC lib")
