# TensorsLab NewMedia Kit 配置文件示例
# 复制此文件为 config.py 并填写你的配置

# TensorsLab API 配置 (必填)
# 申请地址：https://tensorslab.ai
TENSORSLAB_API_KEY = "your_tensorslab_api_key_here"
TENSORSLAB_API_BASE = "https://api.tensorslab.ai/v1"

# Craw4AI 热点抓取配置 (可选，用于热点抓取功能)
# 申请地址：https://craw4ai.com
CRAW4AI_API_KEY = "your_craw4ai_api_key_here"
CRAW4AI_API_BASE = "https://api.craw4ai.com"

# OpenAI 配置 (小红书主题生成必填)
GEMINI_API_KEY = "your_gemini_api_key_here"
GEMINI_MODEL = "gemini-2.5-flash"
OPENAI_API_KEY = "your_openai_api_key_here"
OPENAI_MODEL = "gpt-4o"

# 飞书配置 (可选，用于自动归档到飞书多维表格)
# 申请地址：https://open.feishu.cn
# 注意：table_id 会自动从 API 获取多维表格中的第一个数据表
# 多维表格需包含以下字段：主题(文本)、文案(文本)、配图(附件)、生成时间(日期)
FEISHU_APP_ID = "your_feishu_app_id_here"
FEISHU_APP_SECRET = "your_feishu_app_secret_here"
FEISHU_BITABLE_XHS_TABLE = "" # 小红书素材库地址（多维表格 URL）
FEISHU_BITABLE_BLOG_TABLE = "" # 公众号文章库地址
FEISHU_BITABLE_VIDEO_TABLE = "" # 短视频素材库地址

# 全局默认配置
DEFAULT_IMAGE_STYLE = "cute" # 默认图片风格：cute/ins/business/realistic
DEFAULT_VIDEO_ASPECT_RATIO = "9:16" # 默认视频比例：9:16(竖屏)/16:9(横屏)/1:1(方形)
DEFAULT_OUTPUT_DIR = "./output" # 默认输出目录
