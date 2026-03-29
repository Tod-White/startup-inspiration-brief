"""
配置文件 - 所有敏感信息通过环境变量读取
复制 .env.example 为 .env 并填入你的 API keys
"""
import os

# Telegram 配置
TELEGRAM_CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID', '')  # 你的 Telegram Chat ID

# Claude API 配置（支持任何 OpenAI 兼容接口）
OPENCLAW_API_BASE = os.environ.get('CLAUDE_API_BASE', 'https://api.anthropic.com')
OPENCLAW_API_KEY = os.environ.get('CLAUDE_API_KEY', '')

# Brave Search API
BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', '')

# Firecrawl API（可选，用于抓取 IndieHackers）
FIRECRAWL_API_KEY = os.environ.get('FIRECRAWL_API_KEY', '')

# 模型配置
MODEL_CHEAP = os.environ.get('MODEL_SCORING', 'claude-sonnet-4-5')   # 打分用
MODEL_GOOD = os.environ.get('MODEL_REPORT', 'claude-sonnet-4-5')    # 生成简报用

# 信息源配置
SOURCES = {
    "hackernews": "https://news.ycombinator.com/best",
    "reddit_singularity": "https://www.reddit.com/r/singularity/top/?t=day",
    "reddit_startups": "https://www.reddit.com/r/startups/top/?t=day",
    "producthunt": "https://www.producthunt.com",
    "indiehackers": "https://www.indiehackers.com/top",
    "36kr": "https://36kr.com",
    "v2ex": "https://www.v2ex.com",
    "ycombinator": "https://news.ycombinator.com/show"
}

# 筛选配置
SCORE_THRESHOLD = 6.5  # 综合分数阈值
MIN_ITEMS = 10         # 每天最少推送数
MAX_ITEMS = 10         # 每天最多推送数
FORCE_MIN = True       # 不足 MIN_ITEMS 时降低阈值强制补齐

# 评分维度
SCORE_DIMENSIONS = [
    "小众度",      # 1-10
    "跨界度",      # 1-10
    "监管友好度",  # 1-10
    "可执行性",    # 1-10
    "商业想象力"   # 1-10
]

# 排除关键词
EXCLUDE_KEYWORDS = [
    "融资", "A轮", "B轮", "C轮", "获投",
    "Google发布", "Apple发布", "Microsoft发布",
    "趋势分析", "行业报告"
]

# 优先关键词
PRIORITY_KEYWORDS = [
    "营收", "用户数", "成本", "利润",
    "个人开发", "solo", "indie",
    "AI", "ChatGPT", "自动化"
]
