from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import datetime
from pathlib import Path
from typing import List

import logging

from .trendconfig import TrendRadarConfig
from .adapters import (
    AdapterHotspot,
    BilibiliAdapter,
    GenericRssAdapter,
    HackerNewsAdapter,
    RedditAdapter,
    WeiboAdapter,
    XHSAdapter,
    ZhihuAdapter,
)
from .schemas import HotspotItem as HotspotSchema, TrendBrief


logger = logging.getLogger(__name__)


@dataclass
class HotspotItem:
    title: str
    platform: str
    hot_value: int
    summary: str
    publish_time: str


class TrendRadarService:
    def __init__(self, config: TrendRadarConfig | None = None) -> None:
        self.config = config or TrendRadarConfig()

    def _build_adapters(self) -> list[GenericRssAdapter]:
        platform = (self.config.platform or "all").lower()
        platform_feeds = self.config.platform_feeds or {}

        adapters: list[GenericRssAdapter] = []
        if platform in ("all", "generic", "rss"):
            adapters.append(GenericRssAdapter(self.config.rss_feeds))
        if platform in ("all", "xhs", "xiaohongshu"):
            adapters.append(XHSAdapter(platform_feeds.get("xhs", self.config.rss_feeds)))
        if platform in ("all", "weibo"):
            adapters.append(WeiboAdapter(platform_feeds.get("weibo", self.config.rss_feeds)))
        if platform in ("all", "zhihu"):
            adapters.append(ZhihuAdapter(platform_feeds.get("zhihu", self.config.rss_feeds)))
        if platform in ("all", "bilibili"):
            adapters.append(BilibiliAdapter(platform_feeds.get("bilibili", self.config.rss_feeds)))
        if platform in ("all", "reddit"):
            adapters.append(RedditAdapter(platform_feeds.get("reddit", self.config.rss_feeds)))
        if platform in ("all", "hackernews", "hn"):
            adapters.append(HackerNewsAdapter(platform_feeds.get("hackernews", self.config.rss_feeds)))
        return adapters

    def _platform_weight(self, platform: str) -> int:
        platform = (platform or "").lower()
        if platform in ("xhs", "xiaohongshu"):
            return 3000
        if platform in ("weibo", "zhihu", "bilibili"):
            return 1500
        if platform in ("reddit", "hackernews", "hn"):
            return 1000
        return 0

    def get_hotspots(self) -> List[HotspotItem]:
        items: List[HotspotItem] = []
        for adapter in self._build_adapters():
            try:
                collected = adapter.collect(self.config.count)
                items.extend(
                    HotspotItem(
                        title=item.title,
                        platform=item.platform,
                        hot_value=item.hot_value + self._platform_weight(item.platform),
                        summary=item.summary,
                        publish_time=item.publish_time,
                    )
                    for item in collected
                )
            except Exception as exc:
                logger.debug("适配器 %s 抓取失败: %s", getattr(adapter, "name", "unknown"), exc)

        # 2) 如果 RSS 没拿到内容，则使用本地模拟数据兜底
        if not items:
            items = [
                HotspotItem(
                    title="AI 搜索进入内容分发新阶段",
                    platform=self.config.platform,
                    hot_value=98230,
                    summary="AI 原生搜索正在改变内容分发逻辑，创作者需要同时优化给人和优化给模型。",
                    publish_time=datetime.now().strftime("%Y-%m-%d"),
                ),
                HotspotItem(
                    title="小红书内容自动化工具需求上涨",
                    platform=self.config.platform,
                    hot_value=87420,
                    summary="围绕选题、文案和封面生成的自动化工具，正在成为内容创作提效的重要方向。",
                    publish_time=datetime.now().strftime("%Y-%m-%d"),
                ),
                HotspotItem(
                    title="本地部署 AI 助手成为新趋势",
                    platform=self.config.platform,
                    hot_value=76510,
                    summary="越来越多用户希望把热点分析、知识检索和内容生成能力放在本地可控环境中。",
                    publish_time=datetime.now().strftime("%Y-%m-%d"),
                ),
            ]

        items.sort(key=lambda item: item.hot_value, reverse=True)
        return items[: max(1, min(self.config.count, len(items)))]

    def get_hotspots_schema(self) -> List[HotspotSchema]:
        return [HotspotSchema.model_validate(item.__dict__) for item in self.get_hotspots()]

    def search_hotspots(self, keyword: str | None = None) -> List[HotspotItem]:
        keyword = (keyword or self.config.keyword or "").strip()
        hotspots = self.get_hotspots()
        if not keyword:
            return hotspots
        lowered = keyword.lower()
        return [item for item in hotspots if lowered in item.title.lower() or lowered in item.summary.lower()]

    def build_brief(self, keyword: str | None = None) -> dict:
        items = self.search_hotspots(keyword=keyword)
        lines = [
            f"# TrendRadar 简报 ({datetime.now().strftime('%Y-%m-%d %H:%M')})",
            "",
        ]
        for idx, item in enumerate(items, 1):
            lines.append(f"{idx}. {item.title} [{item.platform}] 热度 {item.hot_value}")
            lines.append(f"   - {item.summary}")
        text = "\n".join(lines)
        return {
            "keyword": keyword or self.config.keyword or "",
            "count": len(items),
            "items": [asdict(item) for item in items],
            "brief": text,
        }

    def build_brief_schema(self, keyword: str | None = None) -> TrendBrief:
        data = self.build_brief(keyword=keyword)
        return TrendBrief(
            keyword=data["keyword"],
            count=data["count"],
            items=[HotspotSchema.model_validate(item) for item in data["items"]],
            brief=data["brief"],
        )

    def export_brief(self, keyword: str | None = None) -> str:
        brief = self.build_brief(keyword=keyword)
        out_dir = Path(self.config.output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)
        output_path = out_dir / f"brief_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        output_path.write_text(brief["brief"], encoding="utf-8")
        return str(output_path)
