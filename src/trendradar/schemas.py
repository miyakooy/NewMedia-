from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class HotspotItem(BaseModel):
    title: str = Field(..., description="热点标题")
    platform: str = Field(..., description="平台来源")
    hot_value: int = Field(..., description="热度值")
    summary: str = Field(..., description="热点摘要")
    publish_time: str = Field(..., description="发布时间")


class TrendBrief(BaseModel):
    keyword: str = Field(default="", description="筛选关键词")
    count: int = Field(..., description="命中数量")
    items: List[HotspotItem] = Field(default_factory=list, description="热点列表")
    brief: str = Field(..., description="Markdown 简报正文")
    generated_at: str = Field(default_factory=lambda: datetime.now().isoformat(), description="生成时间")
