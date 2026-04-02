#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
热点抓取模块
自动抓取新媒体、营销领域近期热门话题
"""
import requests
from typing import List, Dict
from datetime import datetime, timedelta


class HotspotCrawler:
    """热点抓取类"""
    
    def __init__(self, platform: str = "all"):
        """
        初始化抓取器
        platform: 抓取平台，可选all/xiaohongshu/wechat/douyin
        """
        self.platform = platform
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }
    
    def get_latest_hotspots(self, count: int = 10, days: int = 7) -> List[Dict]:
        """
        获取最近days天的热门话题
        返回：[{title, hot_value, platform, publish_time, summary}]
        """
        # 模拟热点数据，实际可接入各平台热点API
        hotspots = [
            {
                "title": "2026营销底层逻辑变化：从投广告到养AI",
                "hot_value": 986500,
                "platform": "全网",
                "publish_time": (datetime.now() - timedelta(days=3)).strftime("%Y-%m-%d"),
                "summary": "现在内容不仅要给人看，还要优化给大模型看，进入AI语料库获得被动流量"
            },
            {
                "title": "小红书GEO优化方法爆火",
                "hot_value": 752300,
                "platform": "小红书",
                "publish_time": (datetime.now() - timedelta(days=2)).strftime("%Y-%m-%d"),
                "summary": "优化内容让AI回答时主动引用，获得额外流量"
            },
            {
                "title": "AI全链路内容自动化工作流",
                "hot_value": 621800,
                "platform": "微信",
                "publish_time": (datetime.now() - timedelta(days=5)).strftime("%Y-%m-%d"),
                "summary": "从热点抓取到内容生成发布全流程自动化，效率提升3倍"
            },
            {
                "title": "CORE-EEAT内容质量标准普及",
                "hot_value": 589200,
                "platform": "技术社区",
                "publish_time": (datetime.now() - timedelta(days=4)).strftime("%Y-%m-%d"),
                "summary": "80项内容质量审核标准，大幅提升内容排名和AI引用率"
            },
            {
                "title": "AI工具成新媒体人标配",
                "hot_value": 815400,
                "platform": "抖音",
                "publish_time": (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d"),
                "summary": "80%新媒体人已经在用AI工具生成内容，效率提升明显"
            }
        ]
        
        # 按热度排序
        hotspots.sort(key=lambda x: x["hot_value"], reverse=True)
        return hotspots[:count]
    
    def get_hotspot_keywords(self) -> List[str]:
        """获取热门关键词列表"""
        hotspots = self.get_latest_hotspots()
        keywords = []
        for hs in hotspots:
            # 简单提取关键词
            if "AI" in hs["title"]:
                keywords.append("AI营销")
            if "GEO" in hs["title"]:
                keywords.append("GEO优化")
            if "自动化" in hs["title"]:
                keywords.append("内容自动化")
            if "小红书" in hs["title"]:
                keywords.append("小红书运营")
        return list(set(keywords))
    
    def recommend_topic(self) -> Dict:
        """推荐当前最适合创作的热点话题"""
        hotspots = self.get_latest_hotspots(count=3)
        # 优先推荐热度高、竞争低的话题
        for hs in hotspots:
            if hs["hot_value"] > 500000 and "AI" in hs["title"]:
                return hs
        return hotspots[0]
