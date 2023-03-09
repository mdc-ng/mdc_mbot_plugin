# mdc_mbot_plugin
Yet another MovieBot plugin

[![GitHub manifest version](https://img.shields.io/github/manifest-json/v/mdc-ng/mdc_mbot_plugin?label=plugin)](https://github.com/mdc-ng/mdc_mbot_plugin/releases)
[![GitHub release (latest SemVer)](https://img.shields.io/github/v/release/mdc-ng/mdc-ng?color=orange&label=mdc-ng)](https://github.com/mdc-ng/mdc-ng/releases)

## Features
- [x] 高性能刮削器
- [x] 监控下载目录，下载完成自动刮削入库
- [x] 支持图片添加标签水印
- [x] 存量整理
- [x] 可视化界面
- [ ] 演员图片

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
4. 进入 moviebot 的插件管理 - 我的插件页面，对 MDC 插件进行配置
5. 多个监控、刮削目录配置方法如下图。以图中的配置为例：
    1. 监控 /misc/downloads 和 /tmp 两个下载目录
    2. 下载到 /misc/downloads 的视频会刮削保存到/ misc/test
    3. 下载到 /tmp 的视频会刮削到 /tmp/adult
<img width="593" alt="image" src="https://user-images.githubusercontent.com/124132602/224089031-1900c61b-753b-4d40-88a9-f4001221d323.png">

注意：如果配置了监控目录，需要在MR的应用设置 - 下载设置 - 媒体文件夹中添加该目录，只要保持“下载路径装载到容器的路径”一项与MDC监控目录中的配置一致即可，其余随意填写无影响

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

## Web UI
v1.4.0版本后，插件整合了 MDC-NG Web UI 套件，增强了存量整理、可视化刮削以及配置管理等功能。在插件管理页面进行服务端的下载更新和启动：

<img src="https://user-images.githubusercontent.com/124132602/222326377-67bd2d14-6519-4e7e-be05-1eeb69a92aea.png" width="400" />

### Usage
1. MDC server 默认使用9208端口，需要先在MovieBot容器添加相应的端口映射
2. 点击”更新MDC“，插件会同时更新MDC lib与server组件
3. 更新完成后，点击”启动/停止服务端"进行服务启动
4. 在浏览器访问 <容器IP>:9208 进入 Web 界面
5. MDC server 支持容器化部署方式，最新动态请关注容器版本发布页：https://hub.docker.com/repository/docker/mdcng/mdc/general
6. 当前版本仍在开发阶段，可能存在不少bug，遇到问题请提issue
  

## 已知问题
1. 在当前版本MR(v1.9.xx)进行 **网页端** 搜索或订阅下载的视频，目标目录中会同时存在MR原样硬链过去的文件和插件刮削结果硬链，下载器直接提交的不受影响。MR后续会支持关闭指定媒体目录的自动硬链，此问题即可随之解决

## 支持一下
你可以送我一杯咖啡，以表示对这个项目的支持😉

<img src="https://user-images.githubusercontent.com/124132602/222636597-f8d48940-a528-41e8-9362-8d15f7517bf6.png" width="300" />
