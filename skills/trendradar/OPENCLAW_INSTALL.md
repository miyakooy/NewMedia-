# TrendRadar OpenClaw 安装指南

## 1. 安装依赖

```bash
pip install -r requirements.txt
```

如果你只想安装 TrendRadar 相关依赖，至少要包含：

- `fastmcp`
- `pydantic`
- `requests`
- `PyYAML`
- `tenacity`
- `feedparser`

## 2. 配置文件

复制示例配置：

```bash
copy config\trendradar.example.json config\trendradar.json
```

如不需要筛选条件，也可以直接跳过配置文件，使用默认配置。

推荐在配置里添加 `rss_feeds`，优先使用真实 RSS 数据源；当源不可用时会自动回退到本地模拟数据，保证可用性。

如果你要替换数据源，只需要修改 `rss_feeds` 列表即可，不需要修改 skill 入口。

如果要做平台定制，可以在 `platform_feeds` 里为不同平台提供独立的 RSS 列表。

## 3. 以 MCP 方式注册到 OpenClaw

在 OpenClaw 的 MCP 配置中添加：

```json
{
  "mcpServers": {
    "trendradar": {
      "command": "python",
      "args": ["-m", "src.trendradar.mcp"],
      "env": {
        "CONFIG_PATH": "./config/trendradar.json"
      }
    }
  }
}
```

## 4. 可用工具

- `get_hotspots`
- `search_hotspots`
- `build_brief`
- `export_brief`

## 5. 本地 CLI

```bash
python -m src.trendradar.cli hotspots
python -m src.trendradar.cli brief --keyword AI
```

## 6. 本地测试

```bash
python src/test/test_trendradar.py
```

该测试会验证热点列表、简报生成和 Markdown 导出。
