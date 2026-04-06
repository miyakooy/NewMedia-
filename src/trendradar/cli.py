from __future__ import annotations

import json
import sys

import click

from .trendconfig import load_config
from .core import TrendRadarService


if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8")


@click.group(name="trendradar")
def trendradar_cli():
    """TrendRadar 最小闭环 CLI"""
    pass


@trendradar_cli.command(name="hotspots")
@click.option("--config", "config_path", default=None, help="JSON 配置文件")
def hotspots(config_path: str | None):
    cfg = load_config(config_path)
    service = TrendRadarService(cfg)
    click.echo(json.dumps([item.__dict__ for item in service.get_hotspots()], ensure_ascii=False, indent=2))


@trendradar_cli.command(name="brief")
@click.option("--keyword", default=None, help="筛选关键词")
@click.option("--config", "config_path", default=None, help="JSON 配置文件")
def brief(keyword: str | None, config_path: str | None):
    cfg = load_config(config_path)
    service = TrendRadarService(cfg)
    click.echo(service.build_brief(keyword=keyword)["brief"])


if __name__ == "__main__":
    trendradar_cli()
