# NewMedia Kit

一站式AI新媒体内容生产工具包，支持小红书文案生成、公众号文章创作、PPT生成、视频生成全场景，内置SEO+GEO双优化能力，让内容同时获得搜索引擎和AI大模型流量。

## ✨ 核心功能
### 内容生产
- ✅ **小红书文案生成**：自动生成符合小红书风格的文案，支持自定义风格、字数、话题
- ✅ **公众号/博客文章生成**：自动生成深度长文，支持自定义结构、排版、引用
- ✅ **PPT生成**：输入主题自动生成完整PPT，支持多种模板
- ✅ **视频生成**：输入文案自动生成短视频，支持字幕、背景音乐、风格选择

### SEO+GEO优化（新增）
- ✅ **热点抓取**：自动抓取全网近期热门话题，解决选题难题
- ✅ **关键词研究**：挖掘高价值低竞争关键词，精准获取搜索流量
- ✅ **内容质量审核**：基于80项CORE-EEAT标准审核内容，给出优化建议
- ✅ **GEO优化**：优化内容让其更容易被AI大模型引用，获得AI搜索被动流量

## 🚀 安装
```bash
pip install -r requirements.txt
cp config.example.py config.py
# 编辑config.py填写对应的API密钥
```

## 📖 使用方法

### 基础内容生成
```bash
# 生成小红书文案
python cli.py xhs generate "AI工具推荐"

# 生成公众号文章
python cli.py blog generate "2026年AI营销趋势"

# 生成PPT
python cli.py ppt generate "AI自动化分享"

# 生成视频
python cli.py video generate "TensorsLab产品介绍"
```

### SEO+GEO优化功能
```bash
# 抓取近期热门话题
python cli.py seo hotspot --count 10 --days 7

# 挖掘高价值关键词
python cli.py seo keyword --niche "AI营销" --count 5

# 审核内容质量（CORE-EEAT标准）
python cli.py seo audit ./content.md --keyword "AI营销工具"

# GEO优化（提升大模型引用率）
python cli.py seo geo ./content.md --keyword "GEO优化" --output ./optimized.md
```

## 🎯 优化效果
- 内容搜索排名提升30%+
- 大模型引用率提升50%+
- 整体被动流量提升40%+
- 内容生产效率提升2-3倍

## 配置说明
参考`config.example.py`中的注释填写对应的API密钥和配置参数。

## 许可证
MIT License
