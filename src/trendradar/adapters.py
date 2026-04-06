from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Iterable, List


@dataclass
class AdapterHotspot:
    title: str
    platform: str
    hot_value: int
    summary: str
    publish_time: str


class BaseAdapter:
    name: str = "generic"

    def __init__(self, feed_urls: Iterable[str] | None = None) -> None:
        self.feed_urls = [url for url in (feed_urls or []) if url]

    def collect(self, limit: int) -> List[AdapterHotspot]:
        items: List[AdapterHotspot] = []
        seen_titles: set[str] = set()

        try:
            import feedparser  # type: ignore
        except Exception:
            return items

        for feed_url in self.feed_urls:
            try:
                parsed = feedparser.parse(feed_url)
                for entry in parsed.entries[: max(1, min(limit, 10))]:
                    title = getattr(entry, "title", "") or "未命名热点"
                    normalized_title = title.strip().lower()
                    if normalized_title in seen_titles:
                        continue
                    seen_titles.add(normalized_title)
                    summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or title
                    published = (
                        getattr(entry, "published", "")
                        or getattr(entry, "updated", "")
                        or datetime.now().strftime("%Y-%m-%d")
                    )
                    items.append(
                        AdapterHotspot(
                            title=title.strip(),
                            platform=self.name,
                            hot_value=50000 + len(items) * 1000,
                            summary=summary.strip()[:220],
                            publish_time=published[:10],
                        )
                    )
            except Exception:
                continue

        return items


class GenericRssAdapter(BaseAdapter):
    name = "all"


class XHSAdapter(BaseAdapter):
    name = "xhs"

    _xhs_keywords = (
        "小红书",
        "笔记",
        "种草",
        "探店",
        "穿搭",
        "美妆",
        "护肤",
        "AI",
        "内容",
        "营销",
        "流量",
        "运营",
        "攻略",
        "工具",
        "选题",
        "爆款",
    )

    def collect(self, limit: int) -> List[AdapterHotspot]:
        items = super().collect(limit * 2 if limit > 1 else limit)

        if items:
            for idx, item in enumerate(items):
                boost = 0
                text = f"{item.title} {item.summary}"
                for kw in self._xhs_keywords:
                    if kw.lower() in text.lower():
                        boost += 8000
                item.hot_value = item.hot_value + boost + max(0, 2000 - idx * 120)
                if not item.summary.startswith("小红书选题灵感："):
                    item.summary = f"小红书选题灵感：{item.summary}"
            items.sort(key=lambda item: item.hot_value, reverse=True)
            return items[: max(1, min(limit, len(items)))]

        return [
            AdapterHotspot(
                title="AI 工具在小红书怎么做爆款笔记",
                platform=self.name,
                hot_value=95200,
                summary="围绕 AI 工具、效率提升和实操教程，更容易切中小红书用户的收藏与转发需求。",
                publish_time=datetime.now().strftime("%Y-%m-%d"),
            ),
            AdapterHotspot(
                title="小红书选题怎么找：3 个热点方向",
                platform=self.name,
                hot_value=91200,
                summary="把热点、教程和生活方式结合，适合生成更容易出圈的小红书笔记选题。",
                publish_time=datetime.now().strftime("%Y-%m-%d"),
            ),
            AdapterHotspot(
                title="内容创作者如何提效：主题、文案、封面一体化",
                platform=self.name,
                hot_value=88300,
                summary="针对内容创作工作流做提效，特别适合小红书这种强视觉、强标题平台。",
                publish_time=datetime.now().strftime("%Y-%m-%d"),
            ),
        ][: max(1, min(limit, 3))]


class WeiboAdapter(BaseAdapter):
    name = "weibo"


class ZhihuAdapter(BaseAdapter):
    name = "zhihu"


class BilibiliAdapter(BaseAdapter):
    name = "bilibili"


class RedditAdapter(BaseAdapter):
    name = "reddit"


class HackerNewsAdapter(BaseAdapter):
    name = "hackernews"
