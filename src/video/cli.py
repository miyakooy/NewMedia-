import click
import os
import config
from src.utils import generate_video

@click.group(name="video")
def video_cli():
    """短视频自动生成工作流"""
    pass

@video_cli.command(name="generate")
@click.option("--topic", required=True, help="视频主题")
@click.option("--duration", default=15, type=int, help="视频时长（秒）")
@click.option("--aspect-ratio", default=config.DEFAULT_VIDEO_ASPECT_RATIO, help="视频比例：9:16/16:9/1:1")
@click.option("--image-url", help="首帧图片URL（图片转视频时使用）")
@click.option("--output-dir", default=config.DEFAULT_OUTPUT_DIR + "/video", help="输出目录")
def generate(topic, duration, aspect_ratio, image_url, output_dir):
    """生成短视频"""
    os.makedirs(output_dir, exist_ok=True)
    click.echo(click.style(f"正在生成「{topic}」{duration}秒短视频...", fg="blue"))
    # TODO: 实现脚本生成、视频生成、自动加字幕BGM、导出逻辑
    video_path = generate_video(prompt=topic, image_url=image_url, duration=duration, aspect_ratio=aspect_ratio, output_path=f"{output_dir}/{topic}.mp4")
    click.echo(click.style(f"✅ 视频生成完成，已保存到 {video_path}", fg="green"))
