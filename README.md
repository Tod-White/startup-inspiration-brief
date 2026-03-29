# 🚀 Startup Inspiration Daily Brief

**English** | [中文](#中文说明)

An agentic workflow that scrapes 13 startup communities daily, scores each item with Claude AI, and pushes a curated digest to Telegram — fully automated, ~$2/month to run.

**Core idea:** Skip the big news. Find non-consensus opportunities — real business stories that major platforms ignore but have solid commercial logic.

## ✨ Features

- **13 sources**: Hacker News, Product Hunt, IndieHackers, Reddit, V2EX, 36Kr, podcasts (How I Built This, My First Million, Side Hustle Show), Substack, Brave News/Community Search
- **AI scoring**: Claude evaluates each item on 5 dimensions — niche appeal, cross-industry potential, regulatory friendliness, executability, business imagination
- **Smart dedup**: Tracks history across all past reports, no repeats
- **Telegram push**: Formatted digest delivered daily
- **Archive**: Every report saved locally as Markdown

## 📋 Sample Output

```
📡 Startup Brief · 2026-03-29

1｜ Solo dev PDF tool — $8k/month, one person
Source: IndieHackers · Score: 8.2/10
↑ Niche  ↑ Executable  ↑ Business potential
https://...

2｜ Notion-based inventory for restaurants — 100 clients in 3 months
Source: Reddit/startups · Score: 7.8/10
...
```

## 🚀 Quick Start

### 1. Clone & install

```bash
git clone https://github.com/Tod-White/startup-inspiration-brief
cd startup-inspiration-brief
pip install -r requirements.txt
```

### 2. Configure

```bash
cp .env.example .env
# Edit .env with your API keys
```

Required:
- `CLAUDE_API_KEY` — [Anthropic Console](https://console.anthropic.com)
- `BRAVE_API_KEY` — [Brave Search API](https://brave.com/search/api/) (free tier available)
- `TELEGRAM_CHAT_ID` — Chat with [@userinfobot](https://t.me/userinfobot) to get yours

Optional:
- `FIRECRAWL_API_KEY` — for IndieHackers scraping (free tier)

### 3. Run

```bash
./run.sh
```

Takes ~15-20 minutes. Report will be pushed to Telegram automatically.

### 4. Schedule daily (cron)

```bash
crontab -e
# Add:
0 8 * * * cd /path/to/startup-inspiration-brief && ./run.sh
```

## 💰 Cost Estimate

| API | Daily usage | Monthly cost |
|-----|-------------|-------------|
| Claude Sonnet | ~50k tokens | ~$1.5 |
| Brave Search | ~30 queries | Free tier |
| Firecrawl | ~10 crawls | Free tier |

**Total: ~$2/month**

## 📁 Project Structure

```
├── main.py              # Orchestrator
├── config.py            # Config (all from env vars)
├── run.sh               # Entry point
├── .env.example         # Config template
├── requirements.txt
├── scrapers/            # Source scrapers
│   ├── brave_news.py
│   ├── brave_community.py
│   ├── hackernews_api.py
│   ├── producthunt_rss.py
│   └── ...
├── filters/
│   └── scorer.py        # Claude AI scorer
├── generators/
│   └── daily.py         # Report generator
└── archive/             # Local report archive
```

## 🔧 OpenClaw Skill

If you use [OpenClaw](https://github.com/openclaw/openclaw), install as a skill:

```bash
cp -r . ~/.openclaw/workspace/skills/startup-brief/
```

Then trigger with: *"run startup brief"*

---

## 中文说明

一个 Agentic 工作流：每天自动抓取 13 个创业社区，用 Claude AI 打分筛选，推送精选简报到 Telegram。全自动运行，月成本约 $2。

**核心理念：** 不追大新闻，找非共识机会——那些大平台不报、但有真实商业逻辑的创业故事。

### ✨ 功能

- **13个信息源**：Hacker News、Product Hunt、IndieHackers、Reddit、V2EX、36Kr、播客（How I Built This、My First Million、Side Hustle Show）、Substack、Brave 新闻/社区搜索
- **AI 打分**：Claude 从 5 个维度评估——小众度、跨界度、监管友好度、可执行性、商业想象力
- **智能去重**：追踪历史简报，不重复推送
- **Telegram 推送**：每日自动发送格式化简报
- **本地存档**：每份简报保存为 Markdown 文件

### 🚀 快速开始

```bash
git clone https://github.com/Tod-White/startup-inspiration-brief
cd startup-inspiration-brief
pip install -r requirements.txt
cp .env.example .env
# 编辑 .env，填入你的 API keys
./run.sh
```

必填配置：
- `CLAUDE_API_KEY`：[Anthropic Console](https://console.anthropic.com) 申请
- `BRAVE_API_KEY`：[Brave Search API](https://brave.com/search/api/) 申请（有免费额度）
- `TELEGRAM_CHAT_ID`：和 [@userinfobot](https://t.me/userinfobot) 对话获取

### 💰 费用估算

月总成本约 **$2**（Claude Sonnet ~$1.5，其余 API 免费额度内）

### License

MIT — 自由使用，欢迎 PR 和 Star ⭐
