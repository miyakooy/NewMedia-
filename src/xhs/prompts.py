from __future__ import annotations


def build_topic_copy_prompt(topic: str, min_words: int = 300, max_words: int = 500) -> str:
    return f"""
请生成一篇小红书风格的主题内容，主题是：{topic}

要求：
1. 标题吸引人，带 emoji
2. 内容活泼自然，适合小红书年轻用户阅读
3. 结构清晰，有开头、内容展开和结尾互动引导
4. 文案总字数控制在 {min_words}-{max_words} 字左右
5. 结尾附带 5-8 个相关话题标签
6. 语气口语化，避免过于正式或像论文

输出要求：
- 直接输出完整文案
- 不要输出分析过程
- 不要输出 Markdown 代码块
""".strip()
