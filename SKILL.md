# Startup Inspiration Daily Brief — OpenClaw Skill

## 触发条件

当用户说以下任意一种时激活：
- "跑一下今天的创业简报"
- "帮我抓今天的创业灵感"
- "run startup brief"
- "创业简报"

## 前置条件

首次使用前确认以下环境变量已配置（在 `.env` 文件或系统环境中）：
- `CLAUDE_API_KEY`
- `BRAVE_API_KEY`
- `TELEGRAM_CHAT_ID`

如未配置，告知用户参考 `.env.example` 填写。

## 执行步骤

### Step 1：检查配置

```bash
cd <skill_dir>
test -f .env && echo "ok" || echo "missing"
```

如果 .env 不存在，停止并提示用户配置。

### Step 2：运行简报

```bash
cd <skill_dir>
export $(grep -v '^#' .env | xargs) && python main.py
```

运行时间约 15-20 分钟，完成后会自动推送到 Telegram。

### Step 3：返回结果

运行完成后，告知用户：
- 本次抓取了多少条内容
- 最终推送了多少条
- 简报已发送到 Telegram
- 存档路径：`archive/YYYY-MM-DD.md`

**不要**把完整简报内容粘贴到对话里，Telegram 已经收到了。

## 定时运行

如需每天自动运行，在 OpenClaw cron 中添加：

```json
{
  "schedule": "0 8 * * *",
  "task": "run startup brief"
}
```

## 故障排查

- **Brave API 报错**：检查 `BRAVE_API_KEY` 是否正确，免费额度是否耗尽
- **Claude API 报错**：检查 `CLAUDE_API_KEY` 和 `CLAUDE_API_BASE`
- **Telegram 推送失败**：检查 `TELEGRAM_CHAT_ID`，确认 OpenClaw 已启动
- **抓取为空**：部分源（IndieHackers/MFM）偶尔失败，属正常现象，其他源会补齐
