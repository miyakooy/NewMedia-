---
name: generate_image
description: 使用 TensorsLab SeeDreamV5 Lite API 生成 AI 图片。支持多种风格和分辨率，自动轮询异步任务并下载图片到本地。
---

# AI 图片生成 (Generate Image)

使用 TensorsLab SeeDreamV5 Lite 模型，根据文本提示词（prompt）生成高质量 AI 图片。

## 功能概述

- 根据文字描述生成图片（文生图）
- 支持多种分辨率/宽高比：1:1（方形）、9:16（竖屏）、16:9（横屏）
- 自动异步轮询任务状态，直到生成完成
- 可选将生成的图片下载保存到本地指定路径

## 前置条件

1. **Python 环境**：Python >= 3.10
2. **依赖安装**：在项目根目录运行 `pip install -r requirements.txt`
3. **API 密钥配置**：在项目根目录的 `config.py` 中配置：
   - `TENSORSLAB_API_KEY`：TensorsLab API 密钥（必填，从 https://tensorai.tensorslab.com 获取）
   - `TENSORSLAB_API_BASE`：API 基础地址（默认 `https://api.tensorslab.com/v1`）

## 使用方式

### 方式一：Python 代码调用

```python
import sys
sys.path.insert(0, "<项目根目录路径>")

from src.utils.tensorslab_api import generate_image

# 基本用法 - 返回图片 URL
image_url = generate_image(prompt="一只可爱的卡通小猫正在玩毛线球，明亮的色彩，3D渲染风格")
print(image_url)

# 指定分辨率和输出路径 - 返回本地文件路径
local_path = generate_image(
    prompt="一只可爱的卡通小猫正在玩毛线球，明亮的色彩，3D渲染风格",
    aspect_ratio="1:1",        # 可选: "1:1", "9:16", "16:9"
    output_path="./output/cat.jpg"  # 指定本地保存路径
)
print(local_path)  # "./output/cat.jpg"
```

## 函数签名

```python
def generate_image(
    prompt: str,              # 图片描述提示词（必填）
    aspect_ratio: str = "1:1", # 宽高比（可选）: 1:1, 9:16, 16:9
    output_path: str = None   # 本地保存路径（可选, 不传则只返回 URL）
) -> str:
    """
    返回值：
    - 如果指定了 output_path：返回本地文件路径
    - 如果未指定 output_path：返回图片的在线 URL
    
    异常：
    - Exception: API 调用失败或图片生成失败时抛出
    """
```

## API 工作流程

1. 向 `{base_url}/images/seedreamv5` 发送 `multipart/form-data` 格式的 POST 请求
2. 获取 `taskid`，然后向 `{base_url}/images/infobytaskid` 轮询任务状态
3. 当 `image_status == 3` 时表示生成成功，从 `url` 字段获取图片地址
4. 当 `image_status == 4` 时表示生成失败

## 关键文件

| 文件 | 说明 |
|------|------|
| `src/utils/tensorslab_api.py` | TensorsLabAPI 类及 `generate_image()` 函数 |
| `src/utils/__init__.py` | 导出 `generate_image` 快捷函数 |
| `config.py` | API 密钥和基础配置 |
| `src/test/test_image.py` | 图片生成测试脚本 |

## 测试验证

运行测试脚本验证功能是否正常：
```bash
python src/test/test_image.py
```

## 注意事项

- 图片生成为异步任务，通常需要 10-30 秒完成
- 轮询间隔为 2 秒
- 生成的图片会保存为 JPG/PNG 格式
- API 密钥需要有足够的调用额度
