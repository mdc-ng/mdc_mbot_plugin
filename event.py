import os
import logging
from mbot.core.event.models import EventType
from mbot.core.plugins import plugin
from mbot.core.plugins import PluginContext
from typing import Dict

from . import config
from .command import mdc_main

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
    # 检查是否匹配监控目录配置
    for dir in config.watch_folder:
        if save_path.startswith(dir):
            flag = True
            break
    if not flag:
        return

    _LOGGER.info("[MDC事件] 下载地址与监控目录匹配: %s, 开始执行刮削" % save_path)

    videos = collect_videos(save_path)
    if len(videos) > 0:
        _LOGGER.info("[MDC事件] 视频文件检测到: %s" % videos)

        if len(videos) > 10:
            _LOGGER.info("[MDC事件] 视频文件数量多于10个，不处理")

        for video in videos:
            _LOGGER.info("[MDC事件] 开始处理视频文件: %s" % video)
            try:
                mdc_main(video)
            except Exception as e:
                _LOGGER.error("[MDC事件] 处理视频文件出错: %s" % video)
                _LOGGER.error(e)
                continue
            _LOGGER.info("[MDC事件] 处理视频文件完成: %s" % video)


def collect_videos(path):
    if not path:
        return []
    videos = []
    if os.path.isdir(path):
        for file in os.listdir(path):
            videos.extend(collect_videos(os.path.join(path, file)))
        return videos
    elif os.path.splitext(path)[1].lower() in [
        ".mp4",
        ".avi",
        ".rmvb",
        ".wmv",
        ".mov",
        ".mkv",
        ".webm",
        ".iso",
        ".mpg",
        ".m4v",
    ]:
        return [path]
    else:
        return []
