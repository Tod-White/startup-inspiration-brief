# 🚀 Startup Inspiration Daily Brief

每天自动抓取全球创业社区内容，用 Claude AI 打分筛选，推送到 Telegram。

**核心理念：** 不追大新闻，找非共识机会——那些大平台不报、但有真实商业逻辑的创业故事。

## 效果示例

```
📡 今日创业简报 · 2026-03-29

1｜ 一个人做的 PDF 工具，月收入 $8k
来源：IndieHackers · 评分：8.2/10
小众度↑ 可执行性↑ 商业想象力↑
https://...

2｜ 用 Notion 帮餐厅管库存，3个月100家客户
来源：Reddit/startups · 评分：7.8/10
...
```

## 信息源（13个）

| 来源 | 类型 |
|------|------|
| Hacker News | Show HN + Best |
| Product Hunt | 新产品发布 |
| IndieHackers | 独立开发者故事 |
| Reddit r/startups | 创业讨论 |
| Reddit r/SideProject | 副业项目 |
| V2EX 创业节点 | 中文创业社区 |
| 36Kr | 中文科技媒体 |
| How I Built This | 播客摘要 |
| My First Million | 播客摘要 |
| Side Hustle Show | 播客摘要 |
| Substack 商业/科技 | Newsletter |
| Brave News Search | 实时新闻 |
| Brave Community Search | 社区讨论 |

## 评分维度

Claude 从 5 个维度打分（各 1-10 分）：

- **小众度**：大平台有没有报道
- **跨界度**：是否跨行业组合
- **监管友好度**：合规风险低
- **可执行性**：普通人能不能做
- **商业想象力**：能不能做大

综合分 ≥ 6.5 才入选，每日推送 10 条。

## 快速开始

### 1. 克隆并安装依赖

```bash
git clone https://github.com/your-username/startup-inspiration-brief
cd startup-inspiration-brief
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入你的 API keys
```

必填：
- `CLAUDE_API_KEY`：[Anthropic Console](https://console.anthropic.com) 申请
- `BRAVE_API_KEY`：[Brave Search API](https://brave.com/search/api/) 申请（有免费额度）
- `TELEGRAM_CHAT_ID`：和 [@userinfobot](https://t.me/userinfobot) 对话获取

### 3. 运行

```bash
# 加载环境变量并运行
export $(cat .env | xargs) && python main.py
```

或者用 run.sh：

```bash
chmod +x run.sh
./run.sh
```

### 4. 定时运行（每天自动推送）

```bash
# 每天早上 8:00 运行
crontab -e
# 添加：
0 8 * * * cd /path/to/startup-inspiration-brief && export $(cat .env | xargs) && python main.py
```

## 作为 OpenClaw Skill 使用

如果你使用 [OpenClaw](https://github.com/openclaw/openclaw)，可以直接安装为 skill：

```bash
# 复制到 skills 目录
cp -r . ~/.openclaw/workspace/skills/startup-brief/
```

然后在对话中触发：
> "帮我跑一下今天的创业简报"

## 项目结构

```
├── main.py              # 主程序，协调所有模块
├── config.py            # 配置（全部读环境变量）
├── requirements.txt     # Python 依赖
├── .env.example         # 环境变量模板
├── scrapers/            # 各平台抓取器
│   ├── brave_news.py
│   ├── brave_community.py
│   ├── hackernews_api.py
│   ├── producthunt_rss.py
│   └── ...
├── filters/
│   └── scorer.py        # Claude AI 打分器
├── generators/
│   └── daily.py         # 简报生成器
└── archive/             # 历史简报存档（本地）
```

## API 费用估算

| API | 用量/天 | 费用/月 |
|-----|---------|--------|
| Claude Sonnet | ~50k tokens | ~$1.5 |
| Brave Search | ~30 次查询 | 免费额度内 |
| Firecrawl | ~10 次 | 免费额度内 |

**月总成本：约 $2-3**

## License

MIT — 自由使用，欢迎 PR。
