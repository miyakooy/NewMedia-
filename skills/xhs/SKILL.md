---
name: xhs
description: 小红书主题生成技能。优先使用 Gemini 2.5 Flash 生成文案，若未配置则回退到 OpenAI GPT-4o，并生成配图保存到本地。
---

# 小红书主题生成技能

你现在要完成的是**小红书主题生成**。只做这一件事：

1. 输入一个主题。
2. 生成小红书风格文案。
3. 生成匹配的配图并保存到本地。
4. 输出结果路径。

## 执行优先级

文案模型按以下顺序选择：

1. **Gemini 优先**
   - 如果配置了 `GEMINI_API_KEY`，优先使用 `GEMINI_MODEL`
   - 默认模型：`gemini-3-flash-preview`
2. **OpenAI 回退**
   - 如果没有 Gemini 配置，则使用 `OPENAI_API_KEY` + `OPENAI_MODEL`
   - 默认模型：`gpt-4o`
3. **都没有**
   - 直接报错，提示至少配置一个可用模型

## 必要配置

最小可用配置：

- `TENSORSLAB_API_KEY`
- `TENSORSLAB_API_BASE`
- `DEFAULT_OUTPUT_DIR`
- `GEMINI_API_KEY` 或 `OPENAI_API_KEY`

推荐配置：

- `GEMINI_MODEL`
- `OPENAI_MODEL`
- `DEFAULT_IMAGE_STYLE`
- `XHS_COPY_WORD_RANGE_MIN`
- `XHS_COPY_WORD_RANGE_MAX`
- `XHS_IMAGE_RATIO`

## 标准流程

当用户要求生成小红书内容时，按这个顺序执行：

1. 校验 `topic` 是否为空
2. 组装小红书文案 prompt
3. 优先调用 Gemini；失败或未配置时回退 OpenAI
4. 将生成文案保存为 `.md`
5. 组装配图 prompt
6. 调用 TensorsLab 生成图片并保存到本地
7. 返回以下结果：
   - `topic`
   - `copy_path`
   - `image_path`
   - `generated_at`

## 文案要求

- 标题要吸引人，带 emoji
- 内容口语化、轻互动
- 结尾带 5-8 个话题标签
- 字数控制在 300-500 字左右
- 不要写成正式报告或论文

## 图片要求

- 默认方形 `1:1`
- 风格跟随 `DEFAULT_IMAGE_STYLE`
- 明亮、清晰、适合小红书封面
- 尽量不要带文字
- 必须保存到本地输出目录

## 代码调用方式

优先直接调用现有代码：

```bash
python cli.py xhs generate --topic "AI工具推荐"
```

也可以在代码中使用：

- `src.xhs.XHSService`
- `src.xhs.XHSGenerationResult`

## 结果标准

成功时必须输出：

- 主题
- 文案文件路径
- 图片文件路径
- 生成时间

## 失败处理

如果出现以下情况，要直接报错并给出清晰信息：

- 未配置可用模型
- 文案生成失败
- 文案写入失败
- 图片生成失败

## 当前范围

当前 skill **只处理主题生成**，暂不包含：

- 热点抓取
- 飞书归档
- 批量生产
