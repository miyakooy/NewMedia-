#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
AI 图片生成脚本 (TensorsLab SeeDreamV5 Lite)

独立可执行脚本，支持命令行调用和模块导入两种方式。
调用 TensorsLab SeeDreamV5 API 根据文本提示词生成图片。

使用方式：
    # 命令行调用
    python generate_image.py --prompt "一只可爱的小猫" --output ./cat.jpg
    python generate_image.py --prompt "商务办公场景" --ratio 16:9

    # 模块导入
    from generate_image import ImageGenerator
    gen = ImageGenerator(api_key="your_key")
    url = gen.generate("一只可爱的小猫")
"""

import requests
import os
import sys
import time
import argparse
from pathlib import Path


class ImageGenerator:
    """TensorsLab SeeDreamV5 Lite 图片生成器"""

    def __init__(self, api_key: str = None, api_base: str = None):
        """
        初始化图片生成器

        Args:
            api_key:  TensorsLab API 密钥。如不传，会尝试从 config.py 或环境变量读取。
            api_base: API 基础地址。默认 https://api.tensorslab.com/v1
        """
        self.api_key = api_key or self._load_api_key()
        self.api_base = api_base or self._load_api_base()
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

    def _load_api_key(self) -> str:
        """从 config.py 或环境变量加载 API Key"""
        # 优先从环境变量读取
        key = os.environ.get("TENSORSLAB_API_KEY")
        if key:
            return key

        # 尝试从项目根目录的 config.py 读取
        try:
            root_dir = str(Path(__file__).resolve().parent.parent.parent.parent)
            sys.path.insert(0, root_dir)
            import config
            return config.TENSORSLAB_API_KEY
        except (ImportError, AttributeError):
            raise ValueError(
                "未找到 API Key。请通过以下方式之一提供：\n"
                "  1. 构造函数参数: ImageGenerator(api_key='your_key')\n"
                "  2. 环境变量: export TENSORSLAB_API_KEY=your_key\n"
                "  3. 项目根目录 config.py: TENSORSLAB_API_KEY = 'your_key'"
            )

    def _load_api_base(self) -> str:
        """从 config.py 或环境变量加载 API Base URL"""
        base = os.environ.get("TENSORSLAB_API_BASE")
        if base:
            return base
        try:
            import config
            return getattr(config, "TENSORSLAB_API_BASE", "https://api.tensorslab.com/v1")
        except ImportError:
            return "https://api.tensorslab.com/v1"

    def generate(
        self,
        prompt: str,
        aspect_ratio: str = "1:1",
        output_path: str = None,
        poll_interval: int = 2,
        verbose: bool = True
    ) -> str:
        """
        生成图片

        Args:
            prompt:        图片描述提示词（必填）
            aspect_ratio:  宽高比，可选 "1:1", "9:16", "16:9"（默认 "1:1"）
            output_path:   本地保存路径。不传则只返回 URL。
            poll_interval: 轮询间隔秒数（默认 2 秒）
            verbose:       是否输出进度信息（默认 True）

        Returns:
            str: 图片 URL 或本地文件路径（取决于是否传了 output_path）

        Raises:
            Exception: API 调用失败或图片生成失败
        """
        # ---- Step 1: 提交生成任务 ----
        endpoint = f"{self.api_base}/images/seedreamv5"

        payload = {
            "category": "seedreamv5",
            "prompt": prompt,
            "batchsize": "1",
            "resolution": aspect_ratio
        }

        req_headers = self.headers.copy()
        req_headers.pop("Content-Type", None)
        files = {k: (None, str(v)) for k, v in payload.items()}

        if verbose:
            print(f"📤 正在提交图片生成任务...")
            print(f"   提示词: {prompt}")
            print(f"   宽高比: {aspect_ratio}")

        response = requests.post(endpoint, files=files, headers=req_headers)
        response.raise_for_status()

        res_data = response.json()
        if res_data.get("code") != 1000:
            raise Exception(f"图片生成请求失败: {res_data.get('msg', '未知错误')}")

        data = res_data.get("data", {})
        image_url = data.get("url")
        task_id = data.get("taskid")

        # ---- Step 2: 轮询任务状态 ----
        if not image_url and task_id:
            if verbose:
                print(f"⏳ 任务已提交 (taskid: {task_id})，等待生成完成...")

            poll_endpoint = f"{self.api_base}/images/infobytaskid"
            elapsed = 0

            while True:
                status_payload = {"taskid": task_id}
                status_response = requests.post(
                    poll_endpoint, json=status_payload, headers=self.headers
                )
                status_response.raise_for_status()
                status_res = status_response.json()

                if status_res.get("code") != 1000:
                    raise Exception(f"查询任务状态失败: {status_res.get('msg', '未知错误')}")

                status_data = status_res.get("data", {})
                image_status = status_data.get("image_status")

                if str(image_status) == "3":
                    # 生成成功
                    urls = status_data.get("url", [])
                    if isinstance(urls, list) and len(urls) > 0:
                        image_url = urls[0]
                    else:
                        image_url = urls
                    if verbose:
                        print(f"✅ 图片生成成功！(耗时约 {elapsed} 秒)")
                    break
                elif str(image_status) == "4":
                    raise Exception(f"图片生成失败: {status_res.get('msg', '未知错误')}")

                time.sleep(poll_interval)
                elapsed += poll_interval
                if verbose:
                    print(f"   ⏳ 已等待 {elapsed} 秒...")

        # ---- Step 3: 下载到本地（可选） ----
        if output_path:
            os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
            if verbose:
                print(f"📥 正在下载图片到: {output_path}")
            image_response = requests.get(image_url)
            with open(output_path, "wb") as f:
                f.write(image_response.content)
            if verbose:
                file_size = os.path.getsize(output_path) / 1024
                print(f"✅ 图片已保存: {output_path} ({file_size:.1f} KB)")
            return output_path

        return image_url


def main():
    """命令行入口"""
    parser = argparse.ArgumentParser(
        description="TensorsLab SeeDreamV5 Lite AI 图片生成",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python generate_image.py --prompt "一只可爱的卡通小猫，3D渲染风格"
  python generate_image.py --prompt "商务办公场景" --ratio 16:9 --output ./office.jpg
  python generate_image.py --prompt "美丽风景" --key YOUR_API_KEY
        """
    )
    parser.add_argument("--prompt", "-p", required=True, help="图片描述提示词")
    parser.add_argument("--ratio", "-r", default="1:1", choices=["1:1", "9:16", "16:9"],
                        help="宽高比 (默认: 1:1)")
    parser.add_argument("--output", "-o", default=None, help="本地保存路径")
    parser.add_argument("--key", "-k", default=None, help="TensorsLab API Key")
    parser.add_argument("--base-url", default=None, help="API Base URL")
    parser.add_argument("--quiet", "-q", action="store_true", help="静默模式")

    args = parser.parse_args()

    generator = ImageGenerator(api_key=args.key, api_base=args.base_url)
    result = generator.generate(
        prompt=args.prompt,
        aspect_ratio=args.ratio,
        output_path=args.output,
        verbose=not args.quiet
    )
    print(f"\n🎉 结果: {result}")


if __name__ == "__main__":
    main()
