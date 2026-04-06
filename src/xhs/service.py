from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
import time

import config

from src.utils import generate_image

from .prompts import build_topic_copy_prompt


@dataclass
class XHSGenerationResult:
    topic: str
    copy_path: str
    image_path: str
    generated_at: str


class XHSGenerationError(RuntimeError):
    """小红书主题生成失败。"""

    pass


class XHSService:
    def __init__(self) -> None:
        self.gemini_api_key = getattr(config, "GEMINI_API_KEY", None)
        self.gemini_model = getattr(config, "GEMINI_MODEL", "gemini-2.5-flash")
        self.openai_api_key = getattr(config, "OPENAI_API_KEY", None)
        self.openai_model = getattr(config, "OPENAI_MODEL", "gpt-4o")
        self.timeout = getattr(config, "OPENAI_TIMEOUT", 60)
        self.max_tokens = getattr(config, "OPENAI_MAX_TOKENS", 1200)
        self.temperature = getattr(config, "OPENAI_TEMPERATURE", 0.8)
        self.retry_count = getattr(config, "XHS_REQUEST_RETRY_COUNT", 2)
        self.retry_backoff = getattr(config, "XHS_REQUEST_RETRY_BACKOFF", 2)
        self._gemini_client = None
        self._openai_client = None

    def _get_gemini_client(self):   
        if not self.gemini_api_key:
            return None
        if self._gemini_client is not None:
            return self._gemini_client

        try:
            from google import genai
        except Exception as exc:  # noqa: BLE001 - SDK 可选依赖缺失时给出明确提示
            raise XHSGenerationError(
                "已配置 GEMINI_API_KEY，但未安装 google-genai 依赖，请先安装后再使用 Gemini 模型"
            ) from exc

        self._gemini_client = genai.Client(api_key=self.gemini_api_key)
        return self._gemini_client

    def _get_openai_client(self):
        if not self.openai_api_key:
            return None
        if self._openai_client is not None:
            return self._openai_client

        from openai import OpenAI

        self._openai_client = OpenAI(api_key=self.openai_api_key, timeout=self.timeout)
        return self._openai_client

    def _call_gemini(self, prompt: str) -> str:
        client = self._get_gemini_client()
        if client is None:
            raise XHSGenerationError("GEMINI_API_KEY 未配置")

        last_error: Exception | None = None
        attempts = max(1, int(self.retry_count) + 1)

        for attempt in range(1, attempts + 1):
            try:
                response = client.models.generate_content(
                    model=self.gemini_model,
                    contents=prompt,
                )
                copy = getattr(response, "text", None) or ""
                copy = copy.strip()
                if not copy:
                    raise XHSGenerationError("Gemini 未返回有效文案")
                return copy
            except Exception as exc:  # noqa: BLE001 - 对外部 API 统一兜底并重试
                last_error = exc
                if attempt < attempts:
                    time.sleep(self.retry_backoff * attempt)
                    continue
                break

        raise XHSGenerationError(f"Gemini 文案生成失败: {last_error}") from last_error

    def _call_openai(self, prompt: str) -> str:
        client = self._get_openai_client()
        if client is None:
            raise XHSGenerationError("OPENAI_API_KEY 未配置")

        last_error: Exception | None = None
        attempts = max(1, int(self.retry_count) + 1)

        for attempt in range(1, attempts + 1):
            try:
                response = client.chat.completions.create(
                    model=self.openai_model,
                    messages=[{"role": "user", "content": prompt}],
                    temperature=self.temperature,
                    max_tokens=self.max_tokens,
                )
                copy = response.choices[0].message.content if response.choices else None
                copy = (copy or "").strip()
                if not copy:
                    raise XHSGenerationError("OpenAI 未返回有效文案")
                return copy
            except Exception as exc:  # noqa: BLE001 - 对外部 API 统一兜底并重试
                last_error = exc
                if attempt < attempts:
                    time.sleep(self.retry_backoff * attempt)
                    continue
                break

        raise XHSGenerationError(f"OpenAI 文案生成失败: {last_error}") from last_error

    def _generate_copy(self, prompt: str) -> str:
        gemini_error: Exception | None = None

        if self.gemini_api_key:
            try:
                return self._call_gemini(prompt)
            except Exception as exc:  # noqa: BLE001 - Gemini 优先，失败后尝试 OpenAI
                gemini_error = exc

        if self.openai_api_key:
            try:
                return self._call_openai(prompt)
            except Exception as exc:
                if gemini_error is not None:
                    raise XHSGenerationError(
                        f"Gemini 与 OpenAI 均失败。Gemini 错误: {gemini_error}; OpenAI 错误: {exc}"
                    ) from exc
                raise

        if gemini_error is not None:
            raise gemini_error

        raise XHSGenerationError("未配置可用的文案模型，请至少配置 GEMINI_API_KEY 或 OPENAI_API_KEY")

    def _generate_image(self, image_prompt: str, image_path: Path, aspect_ratio: str) -> str:
        last_error: Exception | None = None
        attempts = max(1, int(self.retry_count) + 1)

        for attempt in range(1, attempts + 1):
            try:
                result = generate_image(image_prompt, aspect_ratio=aspect_ratio, output_path=str(image_path))
                return str(result)
            except Exception as exc:  # noqa: BLE001 - 对外部 API 统一兜底并重试
                last_error = exc
                if attempt < attempts:
                    time.sleep(self.retry_backoff * attempt)
                    continue
                break

        raise XHSGenerationError(f"图片生成失败: {last_error}") from last_error

    def generate_from_topic(
        self,
        topic: str,
        output_dir: str | None = None,
        style: str | None = None,
        auto_archive: bool = True,
    ) -> XHSGenerationResult:
        if not topic or not topic.strip():
            raise ValueError("topic 不能为空")

        default_output_root = getattr(config, "DEFAULT_OUTPUT_DIR", "./output")
        base_output_dir = output_dir or str(Path(default_output_root) / "xhs")
        out_dir = Path(base_output_dir)
        out_dir.mkdir(parents=True, exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        copy_path = out_dir / f"{timestamp}.md"
        image_path = out_dir / f"{timestamp}.jpg"

        min_words = getattr(config, "XHS_COPY_WORD_RANGE_MIN", 300)
        max_words = getattr(config, "XHS_COPY_WORD_RANGE_MAX", 500)
        prompt = build_topic_copy_prompt(topic=topic, min_words=min_words, max_words=max_words)

        copy = self._generate_copy(prompt)

        try:
            copy_path.write_text(copy, encoding="utf-8")
        except Exception as exc:
            raise XHSGenerationError(f"文案写入失败: {exc}") from exc

        image_style = style or getattr(config, "DEFAULT_IMAGE_STYLE", "cute")
        image_prompt = f"小红书风格封面图，主题：{topic}，明亮配色，清晰，适合年轻用户，1:1比例，无文字，风格：{image_style}"
        image_file = self._generate_image(
            image_prompt=image_prompt,
            image_path=image_path,
            aspect_ratio=getattr(config, "XHS_IMAGE_RATIO", "1:1"),
        )

        result = XHSGenerationResult(
            topic=topic,
            copy_path=str(copy_path),
            image_path=image_file,
            generated_at=datetime.now().isoformat(),
        )

        # 飞书归档（失败不中断主流程）
        if auto_archive:
            self._try_archive(result, copy)

        return result

    def _try_archive(self, result: XHSGenerationResult, copy_content: str) -> None:
        """尝试归档到飞书多维表格，失败时输出红色 Warning 但不抛出异常。"""
        import click

        # 检查飞书配置是否存在
        app_id = getattr(config, "FEISHU_APP_ID", "")
        app_secret = getattr(config, "FEISHU_APP_SECRET", "")
        if (
            not app_id
            or app_id == "your_feishu_app_id_here"
            or not app_secret
            or app_secret == "your_feishu_app_secret_here"
        ):
            return  # 未配置飞书，静默跳过

        try:
            from src.utils import archive_to_bitable

            archive_to_bitable(
                topic=result.topic,
                copy_content=copy_content,
                image_path=result.image_path,
                generated_at=result.generated_at,
            )
        except Exception as exc:  # noqa: BLE001 - 归档失败不应中断主流程
            click.echo(click.style(f"⚠️  飞书归档失败: {exc}", fg="red"))

