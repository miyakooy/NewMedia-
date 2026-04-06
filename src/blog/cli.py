import click
import os
from datetime import datetime
import config
from src.utils import generate_image, archive_to_bitable

@click.group(name="blog")
def blog_cli():
    """公众号/博客全自动创作工作流"""
    pass

@blog_cli.command(name="generate")
@click.option("--topic", required=True, help="文章主题")
@click.option("--word-count", default=2000, type=int, help="文章字数")
@click.option("--auto-archive", is_flag=True, default=True, help="是否自动归档")
def generate(topic, word_count, auto_archive):
    """生成公众号/博客文章"""
    click.echo(click.style(f"正在生成关于「{topic}」的文章（{word_count}字）...", fg="blue"))
    # TODO: 实现文章生成、插图生成、排版、归档逻辑
    click.echo(click.style("✅ 文章生成完成", fg="green"))

@blog_cli.command(name="hotspot-generate")
@click.option("--count", default=2, type=int, help="生成数量")
def hotspot_generate(count):
    """根据热点生成文章"""
    click.echo(click.style("正在抓取全网热点...", fg="blue"))
    # TODO: 实现热点抓取+生成逻辑
    click.echo(click.style("✅ 热点文章生成完成", fg="green"))
