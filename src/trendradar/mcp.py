from __future__ import annotations

import os

try:
    from fastmcp import FastMCP
except Exception as exc:  # pragma: no cover
    raise RuntimeError("请先安装 fastmcp 才能运行 TrendRadar MCP Server") from exc

from .trendconfig import TrendRadarConfig, load_config
from .core import TrendRadarService


mcp = FastMCP("trendradar")


def _service(config_path: str | None = None) -> TrendRadarService:
    config_path = config_path or os.getenv("CONFIG_PATH")
    cfg = load_config(config_path)
    return TrendRadarService(cfg)


@mcp.tool()
def get_hotspots(config_path: str | None = None):
    """获取热点列表"""
    service = _service(config_path)
    return [item.model_dump() for item in service.get_hotspots_schema()]


@mcp.tool()
def search_hotspots(keyword: str | None = None, config_path: str | None = None):
    """按关键词搜索热点"""
    service = _service(config_path)
    import dataclasses
    return [dataclasses.asdict(item) for item in service.search_hotspots(keyword=keyword)]


@mcp.tool()
def build_brief(keyword: str | None = None, config_path: str | None = None):
    """生成热点简报"""
    service = _service(config_path)
    return service.build_brief_schema(keyword=keyword).model_dump()


@mcp.tool()
def export_brief(keyword: str | None = None, config_path: str | None = None):
    """导出热点简报到本地文件"""
    service = _service(config_path)
    return {"output_path": service.export_brief(keyword=keyword)}


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    main()
