from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import json
from typing import Any


DEFAULT_RSS_FEEDS = [
    "https://news.ycombinator.com/rss",
    "https://www.reddit.com/r/technology/.rss",
    "https://www.reuters.com/rssFeed/topNews",
]


@dataclass
class TrendRadarConfig:
    platform: str = "all"
    count: int = 10
    days: int = 7
    keyword: str = ""
    output_dir: str = "./output/trendradar"
    rss_feeds: list[str] = field(default_factory=lambda: DEFAULT_RSS_FEEDS.copy())
    platform_feeds: dict[str, list[str]] = field(default_factory=dict)


def load_config(path: str | None = None) -> TrendRadarConfig:
    if not path:
        return TrendRadarConfig()

    config_path = Path(path)
    if not config_path.exists():
        raise FileNotFoundError(f"配置文件不存在: {path}")

    if config_path.suffix.lower() == ".json":
        data: dict[str, Any] = json.loads(config_path.read_text(encoding="utf-8"))
    else:
        raise ValueError("当前最小闭环仅支持 JSON 配置文件")

    return TrendRadarConfig(
        platform=str(data.get("platform", "all")),
        count=int(data.get("count", 10)),
        days=int(data.get("days", 7)),
        keyword=str(data.get("keyword", "")),
        output_dir=str(data.get("output_dir", "./output/trendradar")),
        rss_feeds=list(data.get("rss_feeds", [])) or DEFAULT_RSS_FEEDS.copy(),
        platform_feeds={k: list(v) for k, v in dict(data.get("platform_feeds", {})).items()},
    )
