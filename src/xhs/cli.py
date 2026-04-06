from __future__ import annotations

import click
import config

from .service import XHSGenerationError, XHSService

@click.group(name="xhs")
def xhs_cli():
    """小红书主题生成工作流"""
    pass

@xhs_cli.command(name="generate")
@click.option("--topic", required=True, help="生成主题")
@click.option("--style", default=None, help="图片风格")
@click.option("--output-dir", default=None, help="输出目录")
@click.option("--no-archive", is_flag=True, default=False, help="跳过飞书归档")
def generate(topic, style, output_dir, no_archive):
    """生成小红书主题文案和配图"""
    try:
        service = XHSService()
        result = service.generate_from_topic(
            topic=topic,
            output_dir=output_dir,
            style=style,
            auto_archive=not no_archive,
        )

        click.echo(click.style("✅ 小红书内容生成完成", fg="green", bold=True))
        click.echo(f"主题：{result.topic}")
        click.echo(f"文案：{result.copy_path}")
        click.echo(f"配图：{result.image_path}")
        click.echo(f"生成时间：{result.generated_at}")
    except (ValueError, XHSGenerationError) as exc:
        raise click.ClickException(str(exc))
