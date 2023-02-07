import logging
import subprocess
import pathlib
import os
import requests
import shutil
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


@plugin.command(
    name="update",
    title="更新MDC lib",
    desc="拉取最新MDC核心库",
    icon="AlarmOn",
    run_in_background=True,
)
def update(ctx: PluginCommandContext):
    update_bin()

    _LOGGER.info("MDC更新成功")
    return PluginCommandResponse(True, "更新成功")


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


def mdc_main(path: str, config_ini: str = config.config_path):
    run_command(
        [
            "./mdc_ng",
            "-p",
            path,
            "-c",
            config_ini,
            "-s",
        ],
        True,
        cwd=pathlib.Path(__file__).parent.absolute(),
        env={"RUST_LOG": "mdc_ng=info"},
    )


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
