import click
import os
import sys

# 加载配置
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import config
except ImportError:
    click.echo(click.style("⚠️  配置文件不存在，请先复制 config.example.py 为 config.py 并填写配置", fg="yellow"))
    sys.exit(1)

from src.xhs import xhs_cli
from src.blog import blog_cli
from src.ppt import ppt_cli
from src.video import video_cli

@click.group()
@click.version_option(version="0.1.0")
def cli():
    """TensorsLab NewMedia Kit - 一站式AI新媒体内容生产工具包"""
    pass

# 注册子命令
cli.add_command(xhs_cli, name="xhs")
cli.add_command(blog_cli, name="blog")
cli.add_command(ppt_cli, name="ppt")
cli.add_command(video_cli, name="video")

if __name__ == "__main__":
    cli()
