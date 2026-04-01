# 🎨 TensorsLab NewMedia Kit - 一站式AI新媒体内容生产工具包

<p align="center">
  <img src="assets/logo.png" width="200" alt="TensorsLab NewMedia Kit Logo">
</p>

<p align="center">
  <strong>AI赋能，让新媒体创作效率提升1000%</strong>
</p>

<p align="center">
  <a href="https://github.com/miyakooy/tensorslab-newmedia-kit/stargazers"><img src="https://img.shields.io/github/stars/miyakooy/tensorslab-newmedia-kit?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/miyakooy/tensorslab-newmedia-kit/issues"><img src="https://img.shields.io/github/issues/miyakooy/tensorslab-newmedia-kit?style=flat-square" alt="GitHub Issues"></a>
  <a href="https://github.com/miyakooy/tensorslab-newmedia-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/miyakooy/tensorslab-newmedia-kit?style=flat-square" alt="License"></a>
  <a href="https://pypi.org/project/tensorslab-newmedia-kit/"><img src="https://img.shields.io/pypi/v/tensorslab-newmedia-kit?style=flat-square" alt="PyPI Version"></a>
</p>

## ✨ 核心功能

### 📕 小红书全自动营销工作流
- ✅ 热点自动抓取：基于Craw4AI实时抓取小红书、抖音、微博热点
- ✅ AI文案生成：贴合小红书风格，自带emoji、话题标签、互动引导
- ✅ 智能配图生成：1:1方形可爱风/ins风配图，自动匹配文案主题
- ✅ 自动归档：自动同步文案、配图到飞书多维表格，支持定时批量生产

### 📝 公众号/博客全自动创作工作流
- ✅ 热点选题：全网热点自动抓取分析，生成优质选题
- ✅ 长文生成：支持万字深度文章，逻辑清晰，符合公众号阅读习惯
- ✅ 智能插图：根据文章段落自动生成配套插图，风格统一
- ✅ 自动排版：遵循Baoyu AI排版规范，一键导出适配公众号/博客的格式
- ✅ 归档管理：自动同步到飞书多维表格，支持版本回溯

### 🎬 PPT AI自动生成工具
- ✅ 内容生成：根据主题自动生成PPT大纲和内容
- ✅ 配图生成：调用TensorsLab AI生成符合主题的封面、配图
- ✅ 多风格模板：支持商务、科技、可爱、简约等多种风格
- ✅ 导出格式：一键导出HTML演示文稿，支持在线播放、PDF导出

### 🎥 短视频自动生成工作流
- ✅ 脚本生成：根据主题自动生成短视频分镜脚本
- ✅ 视频生成：调用TensorsLab AI视频生成API，支持文本转视频、图片转视频
- ✅ 自动剪辑：自动添加字幕、BGM、转场效果
- ✅ 多平台适配：支持抖音/视频号/小红书等多平台尺寸导出

## 🚀 快速开始

### 1. 安装
```bash
pip install tensorslab-newmedia-kit
```

### 2. 配置
复制配置文件模板并填写你的API密钥：
```bash
cp config.example.py config.py
```

在`config.py`中填写：
- `TENSORSLAB_API_KEY`: TensorsLab API密钥（https://tensorslab.ai 获取）
- `FEISHU_APP_ID`/`FEISHU_APP_SECRET`: 飞书应用密钥（可选，用于归档到多维表格）
- `CRAW4AI_API_KEY`: Craw4AI API密钥（可选，用于热点抓取）

### 3. 首次使用

#### 生成小红书内容
```bash
tnm xhs generate --topic "AI工具推荐" --count 5
```

#### 生成公众号文章
```bash
tnm blog generate --topic "2024年AI发展趋势" --word-count 3000
```

#### 生成PPT
```bash
tnm ppt generate --topic "AI新媒体运营方案" --style "business"
```

#### 生成短视频
```bash
tnm video generate --topic "可爱猫咪日常" --duration 15 --aspect-ratio 9:16
```

## 📚 详细文档
- [使用教程](docs/tutorial.md)
- [API文档](docs/api.md)
- [常见问题](docs/faq.md)
- [示例代码](examples/)

## 🤝 贡献
欢迎提交Issue和Pull Request！请先阅读[贡献指南](docs/contributing.md)。

## 📄 许可证
MIT License - 详见 [LICENSE](LICENSE) 文件。

## 🙏 致谢
- [TensorsLab](https://tensorslab.ai) 提供强大的AI图片/视频生成能力
- [Craw4AI](https://craw4ai.com) 提供热点抓取能力
- [Feishu](https://www.feishu.cn) 提供多维表格归档能力
