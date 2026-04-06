---
name: trendradar
description: TrendRadar 最小闭环技能。用于在 OpenClaw 中安装和调用本地热点抓取、筛选与简报生成能力，支持 MCP 和 CLI。
---

# TrendRadar 最小闭环技能

这个技能用于在 OpenClaw 中安装并使用 TrendRadar 的最小闭环能力。

## 目标能力

- 获取热点列表
- 按关键词筛选热点
- 生成热点简报
- 导出本地 Markdown 报告
- 通过 MCP 被 agent 调用

## 推荐架构

1. **Skill 层**：OpenClaw 安装入口，只描述能力和调用方式
2. **MCP 层**：对 agent 暴露工具接口
3. **Core 层**：实际处理热点、筛选、简报和导出
4. **Config 层**：集中管理平台、数量、关键词和输出目录

## 安装方式

### 前置依赖

请先安装项目依赖：

```bash
pip install -r requirements.txt
```

如果你暂时只想先跑 skill 的最小闭环，`feedparser` 是必需的；如果环境里没有安装，系统会自动回退到本地模拟热点。

### 方式一：CLI 本地调用

```bash
python -m src.trendradar.cli hotspots
python -m src.trendradar.cli brief --keyword AI
```

如果你在 Windows 终端中看到中文乱码，CLI 已尝试自动设置 UTF-8 输出；如果仍异常，建议使用支持 UTF-8 的终端执行。

### 方式二：MCP 调用

```bash
python -m src.trendradar.mcp
```

然后在 OpenClaw 的 MCP 配置里注册该服务。

### OpenClaw 注册示例

```json
{
  "mcpServers": {
    "trendradar": {
      "command": "python",
      "args": ["-m", "src.trendradar.mcp"],
      "env": {
        "CONFIG_PATH": "./config/trendradar.example.json"
      }
    }
  }
}
```

更完整的安装说明请见 `skills/trendradar/OPENCLAW_INSTALL.md`。

## MCP 工具

- `get_hotspots(config_path=None)`
- `search_hotspots(keyword=None, config_path=None)`
- `build_brief(keyword=None, config_path=None)`
- `export_brief(keyword=None, config_path=None)`

## 配置文件

推荐使用 JSON 配置文件：

```json
{
  "platform": "all",
  "count": 10,
  "days": 7,
  "keyword": "AI",
  "rss_feeds": [
    "https://news.ycombinator.com/rss",
    "https://www.reddit.com/r/technology/.rss",
    "https://www.reuters.com/rssFeed/topNews"
  ],
  "output_dir": "./output/trendradar"
}
```

也可以直接使用默认配置，不传 `config_path`。

## 数据源策略

1. 优先读取 `rss_feeds` 中的 RSS 源
2. 如果 RSS 失败或没有内容，则自动回退到本地模拟数据
3. 这样可以保证 skill 在本地始终可用，同时支持真实数据

## 真实数据模式

当前默认已经启用真实 RSS 数据模式。你只需要在配置中增加或替换 `rss_feeds` 即可。

如果 RSS 源不可访问、解析失败或返回空内容，系统会自动使用本地模拟热点兜底，确保 skill 仍可用。

## 多平台适配器

当前实现了通用 RSS 适配器和多个平台适配器占位：

- `xhs`
- `weibo`
- `zhihu`
- `bilibili`
- `reddit`
- `hackernews`

这些适配器当前共享 RSS 抓取逻辑，后续可以替换成平台专属抓取规则，而 skill 入口保持不变。

### 小红书适配说明

`xhs` 适配器会优先放大和小红书强相关的热点，例如：

- 小红书
- 笔记
- 种草
- 探店
- 穿搭
- 美妆
- 护肤
- AI 工具
- 内容创作

如果 RSS 结果不足，`xhs` 适配器会自动使用小红书方向的兜底热点。

## 输出规范

### 热点列表

每条热点输出字段：

- `title`
- `platform`
- `hot_value`
- `summary`
- `publish_time`

### 简报

简报输出为结构化 JSON 和可读 Markdown 文本。

推荐的结构化模型见 `src/trendradar/schemas.py`。

## 当前范围

当前只实现最小闭环：

- RSS 真实热点抓取
- 模拟热点兜底
- 多平台适配器
- 关键词筛选
- 简报生成
- 本地导出

## 本地测试

你可以直接运行：

```bash
python src/test/test_trendradar.py
```

该测试会检查：

- 热点列表是否正常返回
- 简报是否正常生成
- Markdown 文件是否成功导出

## 建议的扩展方向

- 增加平台专属适配器（如小红书/微博/知乎）
- 统一热度排序规则
- 加入更完整的抓取日志和告警
- 加入按时间窗口过滤

后续可继续扩展：

- 真实 RSS / 平台数据抓取
- AI 分析
- 通知推送
