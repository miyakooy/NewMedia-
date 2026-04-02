#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
示例：测试图片生成功能

演示如何使用 generate_image skill 生成 AI 图片。
包含两种调用方式：
  1. 通过独立脚本的 ImageGenerator 类
  2. 通过项目的 src.utils.tensorslab_api 模块
"""

import sys
import os
from pathlib import Path
from datetime import datetime


def example_via_skill_script():
    """方式一：使用 skill 自带的 ImageGenerator 类"""
    print("=" * 50)
    print("📌 示例 1：使用 ImageGenerator 类")
    print("=" * 50)

    # 导入 skill 脚本
    skill_scripts_dir = str(Path(__file__).resolve().parent.parent / "scripts")
    sys.path.insert(0, skill_scripts_dir)
    from generate_image import ImageGenerator

    # 创建生成器（API Key 自动从 config.py 或环境变量读取）
    generator = ImageGenerator()

    prompt = "一只可爱的卡通小猫正在玩毛线球，明亮的色彩，3D渲染风格"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    output_path = os.path.join(output_dir, f"example_cat_{timestamp}.jpg")

    print(f"🌟 提示词: {prompt}")
    print(f"📁 输出路径: {output_path}")
    print("-" * 50)

    try:
        result = generator.generate(
            prompt=prompt,
            aspect_ratio="1:1",
            output_path=output_path
        )
        print(f"\n🎉 生成成功: {result}")

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"✔️ 文件大小: {file_size:.2f} KB")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


def example_via_project_module():
    """方式二：使用项目的 src.utils 模块"""
    print("\n" + "=" * 50)
    print("📌 示例 2：使用项目 src.utils.tensorslab_api 模块")
    print("=" * 50)

    # 将项目根目录加入 path
    root_dir = str(Path(__file__).resolve().parent.parent.parent.parent)
    sys.path.insert(0, root_dir)
    from src.utils.tensorslab_api import generate_image

    prompt = "一朵盛开的向日葵，水彩画风格，柔和的光线"
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "output")
    output_path = os.path.join(output_dir, f"example_flower_{timestamp}.jpg")

    print(f"🌟 提示词: {prompt}")
    print(f"📁 输出路径: {output_path}")
    print("-" * 50)

    try:
        result = generate_image(
            prompt=prompt,
            aspect_ratio="1:1",
            output_path=output_path
        )
        print(f"\n🎉 生成成功: {result}")

        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path) / 1024
            print(f"✔️ 文件大小: {file_size:.2f} KB")
    except Exception as e:
        print(f"\n❌ 生成失败: {e}")


if __name__ == "__main__":
    print("🚀 TensorsLab SeeDreamV5 图片生成示例\n")

    # 运行示例 1
    example_via_skill_script()

    # 运行示例 2（需要项目根目录有 config.py）
    # example_via_project_module()
