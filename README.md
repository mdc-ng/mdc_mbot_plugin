# mdc_mbot_plugin
Yet another MovieBot plugin

[![GitHub manifest version](https://img.shields.io/github/manifest-json/v/mdc-ng/mdc_mbot_plugin?label=plugin)](https://github.com/mdc-ng/mdc_mbot_plugin/releases)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/mdc-ng/mdc-ng?color=orange&label=mdc-ng)](https://github.com/mdc-ng/mdc-ng/releases)

## Features
- 高性能刮削器
- 监控下载目录，下载完成自动刮削入库
- 支持图片添加标签水印

## Usage
### 工作流程
硬链后刮削，无需担心做种问题，全流程如下：
1. 识别影片ID
2. 抓取元数据
3. 创建目标目录
4. 下载、处理图片
5. 硬链接视频以及自带的字幕文件到目标目录
6. 生成nfo文件

### 安装与使用
1. 在 [Release](https://github.com/mdc-ng/mdc_mbot_plugin/releases) 页面下载最新版本插件压缩包 mdc_mbot_plugin-${version}.zip
2. 解压缩并将插件文件夹重命名为 mdc_mbot_plugin，丢到容器的 plugins 目录
3. 重启容器
4. 进入 moviebot 的插件管理 - 我的插件页面，对 MDC 插件进行配置：
![image](https://user-images.githubusercontent.com/124132602/217214050-941124b0-99f2-41da-8f06-e147f79f7974.png)

    注意：如果配置了监控目录，需要在MR的应用设置 - 下载设置 - 媒体文件夹中添加该目录，只要保持“下载保存路径”一项与MDC监控目录中的配置一致即可，其余随意填写无影响

    ![image](https://user-images.githubusercontent.com/124132602/217214907-69b8a329-b4b9-4af2-b301-b113d5f77779.png)

5. 代理配好后，在插件管理 - 快捷功能中执行“更新MDC”，等待执行成功
6. 若更新MDC失败，通常是与github网络连接性问题，请检查代理是否配置正确
7. 日志中若出现 “MDC version: xxx”：恭喜你，插件配置完成！
8. MDC的主要功能由核心库提供: https://github.com/mdc-ng/mdc-ng/releases
   
   请关注核心库的版本发布。可执行5~7步骤单独更新内核，以获得MDC的最新特性

### 作为基础库
```python
# 其他插件中对 MDC 的调用方式示例
def mdc_command(video, config_path):
    from ..mdc_mbot_plugin import mdc_main
    
    # video:        必填，视频的绝对路径，如 /nas/media/xxx.mp4
    # config_path:  可选，自定义配置文件的绝对路径。不传递则会使用默认config.ini
    mdc_main(video, config_path)
```

## 已知问题
1. 目前版本MR(v1.9.25)对于网页端搜索、订阅下载的视频，会将未识别的视频进行原名硬链。使用此插件会导致目标目录中同时存在一份MR硬链目录、一份刮削结果硬链目录。MR后续会支持关闭此自动硬链功能，此问题即可解决
