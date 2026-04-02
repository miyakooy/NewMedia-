# generate_image - AI 图片生成 Skill

基于 TensorsLab SeeDreamV5 Lite 模型的 AI 图片生成能力。

## 目录结构

```
generate_image/
├── SKILL.md                # Skill 核心定义（YAML 元数据 + 使用指令）
├── README.md               # 本文件 - Skill 说明文档
├── scripts/
│   └── generate_image.py   # 独立可执行的图片生成脚本
├── resources/
│   └── config_template.py  # API 配置模板
└── examples/
    ├── test_image.py        # 示例：测试图片生成
    └── example_prompts.md   # 示例：常用提示词参考
```

## 快速开始

### 1. 配置 API 密钥

复制 `resources/config_template.py` 到项目根目录的 `config.py`，填入你的 TensorsLab API Key：

```bash
cp resources/config_template.py ../../config.py
```

### 2. 安装依赖

```bash
pip install requests tqdm
```

### 3. 运行示例

```bash
# 使用独立脚本生成图片
python scripts/generate_image.py --prompt "一只可爱的卡通小猫" --output ./output/cat.jpg

# 运行测试示例
python examples/test_image.py
```

## API 申请

前往 https://tensorai.tensorslab.com 注册并获取 API Key。
