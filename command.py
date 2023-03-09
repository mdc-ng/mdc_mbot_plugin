import logging
import subprocess
import pathlib
import os
import requests
import shutil
from mbot.core.params import ArgSchema, ArgType
from mbot.core.plugins import (
    plugin,
    PluginCommandContext,
    PluginCommandResponse,
)
from mbot.openapi import mbot_api
from . import config


server = mbot_api
_LOGGER = logging.getLogger(__name__)

bin_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "mdc_ng")
bin_path_new = bin_path + ".new"

backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "backend")
backend_path_new = backend_path + ".new"

mdc_server = None


@plugin.command(
    name="update",
    title="更新MDC",
    desc="拉取最新MDC核心库和后端服务",
    icon="AlarmOn",
    run_in_background=True,
)
def update(ctx: PluginCommandContext):
    update_bin()
    update_server()

    _LOGGER.info("MDC更新成功")
    return PluginCommandResponse(True, "更新成功")


@plugin.command(
    name="start_mdc_server",
    title="启动/停止MDC服务端",
    desc="启动/停止MDC服务端",
    icon="AlarmOn",
    run_in_background=True,
)
def start_mdc_server(ctx: PluginCommandContext):
    global mdc_server

    if not mdc_server:
        start_server()
    else:
        stop_server()

    return PluginCommandResponse(True, "启动成功，请通过9208端口访问Web UI")


@plugin.command(
    name="mdc_manual",
    title="MDC手动执行",
    desc="指定目录或视频文件进行刮削",
    icon="",
    run_in_background=True,
)
def mdc_test(ctx: PluginCommandContext, path: ArgSchema(ArgType.String, "刮削路径", "")):
    try:
        mdc_dir(path)
    except Exception as e:
        _LOGGER.error(e, exc_info=True)
        return PluginCommandResponse(False, f"一键刮削成功")
    return PluginCommandResponse(True, f"一键刮削失败")


def update_bin():
    download_file(
        "https://github.com/mdc-ng/mdc-ng/releases/download/latest/mdc_ng",
        bin_path_new,
    )
    try:
        os.remove(bin_path)
    except:
        pass
    os.rename(bin_path_new, bin_path)
    run_command(
        [
            "chmod",
            "+x",
            "mdc_ng",
        ],
        False,
        cwd=pathlib.Path(__file__).parent.absolute(),
    )
    run_command(
        [
            "./mdc_ng",
            "-v",
        ],
        True,
        cwd=pathlib.Path(__file__).parent.absolute(),
    )


def update_server():
    download_file(
        "https://github.com/mdc-ng/mdc-ng/releases/download/latest/backend",
        backend_path_new,
    )
    try:
        os.remove(backend_path)
    except:
        pass
    os.rename(backend_path_new, backend_path)
    run_command(
        [
            "chmod",
            "+x",
            "backend",
        ],
        False,
        cwd=pathlib.Path(__file__).parent.absolute(),
    )
    run_command(
        [
            "./backend",
            "-v",
        ],
        True,
        cwd=pathlib.Path(__file__).parent.absolute(),
    )


def mdc_main(
    path: str,
    config_ini=None,
    target_folder=None,
):

    if not target_folder:
        target_folder = config.target_folder
    proxy = config.proxies["http"]

    command = ["./mdc_ng", "-p", path]

    if config_ini:
        command.extend(["-c", config_ini])
    if target_folder:
        command.extend(["-t", target_folder])
    if proxy:
        command.extend(["--proxy", proxy])

    _LOGGER.info(command)

    run_command(
        command,
        True,
        cwd=pathlib.Path(__file__).parent.absolute(),
        env={"RUST_LOG": "mdc_ng=info"},
    )


def mdc_dir(path: str, target_folder=None):
    videos = collect_videos(path)
    if len(videos) > 0:
        _LOGGER.info("[MDC] 视频文件检测到: %s" % videos)

        if len(videos) > 10:
            _LOGGER.info("[MDC] 视频文件数量多于10个，不处理")

        for video in videos:
            _LOGGER.info("[MDC] 开始处理视频文件: %s" % video)
            try:
                mdc_main(video, target_folder=target_folder)
            except Exception as e:
                _LOGGER.error("[MDC] 处理视频文件出错: %s" % video)
                _LOGGER.error(e)
                continue
            _LOGGER.info("[MDC] 处理视频文件完成: %s" % video)


def collect_videos(path: str):
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
        ".ts",
    ]:
        return [path]
    else:
        return []


def download_file(url, name):
    with requests.get(url, proxies=config.proxies, stream=True) as r:
        with open(name, "wb") as f:
            shutil.copyfileobj(r.raw, f)

    return name


def run_command(command, capture, **kwargs):
    """Run a command while printing the live output"""
    process = subprocess.Popen(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        **kwargs,
    )
    while True:  # Could be more pythonic with := in Python3.8+
        line = process.stdout.readline()
        if not line and process.poll() is not None:
            break
        if capture:
            _LOGGER.info(line.decode().strip())


def start_server():
    global mdc_server
    if not mdc_server:
        mdc_server = subprocess.Popen(
            [
                "./backend",
                "-p",
                "9208",
            ],
            cwd=pathlib.Path(__file__).parent.absolute(),
        )


def stop_server():
    global mdc_server
    if mdc_server:
        mdc_server.terminate()
    mdc_server = None
