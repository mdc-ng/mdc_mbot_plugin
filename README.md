# mdc_mbot_plugin
A moviebot plugin

## Usage
```python
# 其他插件中对 MDC 的调用方式示例
def mdc_command(video, config_path):
    from ..mdc_mbot_plugin import mdc_main
    
    # video:        必填，视频的绝对路径，如 /nas/media/xxx.mp4
    # config_path:  可选，自定义配置文件的绝对路径。不传递则会使用默认config.ini
    mdc_main(video, config_path)
```
