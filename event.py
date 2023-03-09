import os
import logging
from mbot.core.event.models import EventType
from mbot.core.plugins import plugin
from mbot.core.plugins import PluginContext
from typing import Dict

from . import config
from .command import mdc_dir

_LOGGER = logging.getLogger(__name__)


# {
# 'name': '三体.ThreeBody.S01.2023.2160p.V2.WEB-DL.H265.AAC-HHWEB',
# 'hash': '96773744314c9a487462a86b9d04dbb90ca7ce14',
# 'save_path': '/nas/downloads/tv/',
# 'content_path': '/nas/downloads/tv/三体.ThreeBody.S01.2023.2160p.V2.WEB-DL.H265.AAC-HHWEB/ThreeBody.S01E16.2023.2160p.V2.WEB-DL.H265.AAC-HHWEB.mp4',
# 'progress': 100,
# 'size': 1081936959,
# 'size_str': '1.01 GB',
# 'dlspeed': 0,
# 'dlspeed_str': '0',
# 'upspeed': 0,
# 'upspeed_str': '0',
# 'uploaded': 3172779138,
# 'uploaded_str': '2.95 GB',
# 'seeding_time': 7512,
# 'downloaded': 1092912248,
# 'downloaded_str': '1.02 GB',
# 'ratio': 2.903050216342712,
# }
@plugin.on_event(bind_event=[EventType.DownloadCompleted], order=1)
def on_event(ctx: PluginContext, event_type: str, data: Dict):
    """
    触发绑定的事件后调用此函数
    函数接收参数固定。第一个为插件上下文信息，第二个事件类型，第三个事件携带的数据
    """

    save_path = data.get("source_path")
    _LOGGER.info("[MDC事件] source_path: %s " % save_path)
    if not save_path:
        return

    _LOGGER.info("[MDC事件] watch_folder: %s " % config.watch_folder)
    flag = False
    target_folder = None
    # 检查是否匹配监控目录配置
    for folders in config.watch_folder:
        dir = folders[0]
        if save_path.startswith(dir):
            flag = True
            if len(folders) > 1:
                target_folder = folders[1]
            break
    if not flag:
        return

    _LOGGER.info("[MDC事件] 下载地址与监控目录匹配: %s, 开始执行刮削" % save_path)

    mdc_dir(save_path, target_folder)
