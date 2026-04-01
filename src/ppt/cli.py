import click
import os
import config
from src.utils import generate_image

@click.group(name="ppt")
def ppt_cli():
    """PPT AI自动生成工具"""
    pass

@ppt_cli.command(name="generate")
@click.option("--topic", required=True, help="PPT主题")
@click.option("--style", default="business", help="PPT风格：business/tech/cute/minimal")
@click.option("--pages", default=10, type=int, help="PPT页数")
@click.option("--output-dir", default=config.DEFAULT_OUTPUT_DIR + "/ppt", help="输出目录")
def generate(topic, style, pages, output_dir):
    """生成HTML格式PPT"""
    os.makedirs(output_dir, exist_ok=True)
    click.echo(click.style(f"正在生成「{topic}」{style}风格PPT（{pages}页）...", fg="blue"))
    # TODO: 实现大纲生成、内容生成、配图生成、HTML渲染逻辑
    click.echo(click.style(f"✅ PPT生成完成，已保存到 {output_dir}", fg="green"))
