# 🎨 TensorsLab NewMedia Kit - All-in-One AI New Media Content Production Toolkit

<p align="center">
  <img src="assets/logo.png" width="200" alt="TensorsLab NewMedia Kit Logo">
</p>

<p align="center">
  <strong>Powered by AI, boost your new media creation efficiency by 1000%</strong>
</p>

<p align="center">
  <a href="https://github.com/miyakooy/tensorslab-newmedia-kit/stargazers"><img src="https://img.shields.io/github/stars/miyakooy/tensorslab-newmedia-kit?style=flat-square" alt="GitHub Stars"></a>
  <a href="https://github.com/miyakooy/tensorslab-newmedia-kit/issues"><img src="https://img.shields.io/github/issues/miyakooy/tensorslab-newmedia-kit?style=flat-square" alt="GitHub Issues"></a>
  <a href="https://github.com/miyakooy/tensorslab-newmedia-kit/blob/main/LICENSE"><img src="https://img.shields.io/github/license/miyakooy/tensorslab-newmedia-kit?style=flat-square" alt="License"></a>
  <a href="https://pypi.org/project/tensorslab-newmedia-kit/"><img src="https://img.shields.io/pypi/v/tensorslab-newmedia-kit?style=flat-square" alt="PyPI Version"></a>
</p>

## ✨ Core Features

### 📕 Xiaohongshu (Little Red Book) Full Automatic Marketing Workflow
- ✅ Hotspot auto-crawling: Real-time capture of hot topics from Xiaohongshu, Douyin, Weibo based on Craw4AI
- ✅ AI copy generation: Fits Xiaohongshu style, with emojis, hashtags, interactive guides
- ✅ Smart image generation: 1:1 square cute/ins style images, automatically matching the copy theme
- ✅ Auto archiving: Automatically sync copy and images to Feishu Bitable, support scheduled batch production

### 📝 Official Account/Blog Full Automatic Creation Workflow
- ✅ Hot topic selection: Automatic crawling and analysis of whole network hotspots, generate high-quality topics
- ✅ Long article generation: Support 10,000-word in-depth articles, clear logic, conform to official account reading habits
- ✅ Smart illustration: Automatically generate matching illustrations according to article paragraphs, unified style
- ✅ Automatic typesetting: Follow Baoyu AI typesetting specifications, one-click export format suitable for official accounts/blogs
- ✅ Archive management: Automatically sync to Feishu Bitable, support version backtracking

### 🎬 PPT AI Automatic Generation Tool
- ✅ Content generation: Automatically generate PPT outline and content according to the theme
- ✅ Image generation: Call TensorsLab AI to generate covers and images matching the theme
- ✅ Multi-style templates: Support business, technology, cute, minimalist and other styles
- ✅ Export format: One-click export of HTML presentations, support online playback, PDF export

### 🎥 Short Video Automatic Generation Workflow
- ✅ Script generation: Automatically generate short video storyboard scripts according to the theme
- ✅ Video generation: Call TensorsLab AI video generation API, support text-to-video, image-to-video
- ✅ Automatic editing: Automatically add subtitles, BGM, transition effects
- ✅ Multi-platform adaptation: Support size export for Douyin/Video Account/Xiaohongshu and other platforms

## 🚀 Quick Start

### 1. Installation
```bash
pip install tensorslab-newmedia-kit
```

### 2. Configuration
Copy the configuration file template and fill in your API keys:
```bash
cp config.example.py config.py
```

Fill in `config.py`:
- `TENSORSLAB_API_KEY`: TensorsLab API key (get from https://tensorslab.ai)
- `FEISHU_APP_ID`/`FEISHU_APP_SECRET`: Feishu app key (optional, for archiving to Bitable)
- `CRAW4AI_API_KEY`: Craw4AI API key (optional, for hotspot crawling)

### 3. First Use

#### Generate Xiaohongshu content
```bash
tnm xhs generate --topic "AI tool recommendation" --count 5
```

#### Generate official account article
```bash
tnm blog generate --topic "2024 AI development trends" --word-count 3000
```

#### Generate PPT
```bash
tnm ppt generate --topic "AI new media operation plan" --style "business"
```

#### Generate short video
```bash
tnm video generate --topic "cute cat daily" --duration 15 --aspect-ratio 9:16
```

## 📚 Detailed Documentation
- [Tutorial](docs/tutorial_en.md)
- [API Documentation](docs/api_en.md)
- [FAQ](docs/faq_en.md)
- [Example Code](examples/)

## 🤝 Contributing
Issues and Pull Requests are welcome! Please read the [Contribution Guide](docs/contributing_en.md) first.

## 📄 License
MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments
- [TensorsLab](https://tensorslab.ai) provides powerful AI image/video generation capabilities
- [Craw4AI](https://craw4ai.com) provides hotspot crawling capabilities
- [Feishu](https://www.feishu.cn) provides Bitable archiving capabilities
