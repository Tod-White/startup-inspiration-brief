# 🚀 Startup Inspiration Daily Brief

[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org)
[![Agentic Workflow](https://img.shields.io/badge/agentic-workflow-purple.svg)](https://github.com/Tod-White/startup-inspiration-brief)
[![Stars](https://img.shields.io/github/stars/Tod-White/startup-inspiration-brief?style=social)](https://github.com/Tod-White/startup-inspiration-brief/stargazers)

**English** | [中文](#中文说明)

⭐ **If this is useful, a star helps others find it** — and [follow @Tod-White](https://github.com/Tod-White) for more agentic workflows.

An agentic workflow that scrapes 13 startup communities daily, scores each item with Claude AI, and pushes a curated digest to Telegram — fully automated, ~$2/month to run.

**Core idea:** Skip the big news. Find non-consensus opportunities — real business stories that major platforms ignore but have solid commercial logic.

## ✨ Features

- **13 sources**: Hacker News, Product Hunt, IndieHackers, Reddit, V2EX, 36Kr, podcasts (How I Built This, My First Million, Side Hustle Show), Substack, Brave News/Community Search
- **AI scoring**: Claude evaluates each item on 5 dimensions — niche appeal, cross-industry potential, regulatory friendliness, executability, business imagination
- **Smart dedup**: Tracks history across all past reports, no repeats
- **Telegram push**: Formatted digest delivered daily
- **Archive**: Every report saved locally as Markdown

## 📋 Sample Output

**[🔗 Live Demo →](https://startup-brief-demo.vercel.app)** — bilingual, switch between English / 中文

> ⚠️ The demo shows a sample output — not a product or service. This tool runs on your own server for ~$2/month. Want a custom version for your niche? Fork this repo and go.


---

### 🇬🇧 English Sample

```
📡 Startup Inspiration Brief · 2026-03-28
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1 | Eggs priced like wine                           ★ 9.2
    Source: How I Built This
    Vital Farms turned commodity eggs into a public company.
    Not a food story — pure brand arbitrage.
    "You're not selling a better egg. You're selling an identity."
    ↑ Cross-industry  ↑ UK market fit  ↑ Narrative moat
    🟡 1-2yr window

#2 | Solo dev vs Bloomberg — 99% cheaper              ★ 7.4
    Source: Reddit r/SaaS
    Bloomberg metals data: $25,000/yr.
    He rebuilt the core, made the best part free.
    Free = moat. Acquisition cost: near zero.
    ↑ Price arbitrage  ↑ B2B  ↑ No sales team needed
    🟡 1-2yr window

#3 | Rewrote enterprise component in 1 day            ★ 9.0
    Source: Hacker News
    Reco.ai used AI to rewrite a legacy component.
    Result: saved $500,000/year.
    Real play: sell this as a fixed-price B2B service.
    NHS legacy stack density = world-class opportunity.
    ↑ AI execution  ↑ NHS fit  ↑ Underserved B2B
    🟡 1-2yr window

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Trends: Brand arbitrage · Legacy AI rewrite · Freemium B2B
Sources: HN(50) PH(20) Reddit(16) SideHustle(10) 36Kr(20) +7 more
```

---

### 🇨🇳 中文样本

```
📡 创业灵感日报 · 2026-03-28
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

#1 | 鸡蛋卖出了葡萄酒的价格                         ★ 9.2
    来源：How I Built This
    Vital Farms 把散养蛋做成了上市公司。
    不是食品故事——是品牌套利。
    「你卖的不是更好的蛋，你卖的是一种身份认同。」
    ↑ 跨界  ↑ 英国市场适配  ↑ 叙事护城河
    🟡 还有1-2年窗口

#2 | 一个人打Bloomberg，定价砍掉99%                  ★ 7.4
    来源：Reddit r/SaaS
    Bloomberg金属数据：$25,000/年。
    他重建了核心功能，把最好的部分免费开放。
    免费 = 护城河。获客成本：接近零。
    ↑ 价格套利  ↑ B2B  ↑ 无需销售团队
    🟡 还有1-2年窗口

#3 | 一天重写企业级组件，省了50万美元               ★ 9.0
    来源：Hacker News
    Reco.ai 用 AI 一天重写了遗留组件。
    结果：每年节省 $500,000。
    真正机会：把这件事包装成固定报价的B2B服务。
    NHS 遗留系统密度 = 世界级机会。
    ↑ AI执行力  ↑ NHS适配  ↑ 被低估的B2B赛道
    🟡 还有1-2年窗口

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
趋势关键词：品牌套利 · 遗留系统AI改造 · Freemium B2B
信息源：HN(50) PH(20) Reddit(16) SideHustle(10) 36Kr(20) 共13源
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

⭐ **如果对你有用，点个 Star 帮助更多人发现这个项目** — 并 [关注 @Tod-White](https://github.com/Tod-White) 获取更多 Agentic 工作流。

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
