# 🚀 创业灵感信息系统

每天自动抓取、筛选、推送创业灵感案例到 Telegram

## ✅ 已完成

- [x] Hacker News 爬虫
- [x] AI 五维评分系统（Haiku 初筛）
- [x] 简报生成（Opus 生成）
- [x] Telegram 推送
- [x] 定时任务（每天早上 7:00）

## 📅 运行时间

- **每日简报**：每天早上 7:00 自动运行
- **周报**：待实现

## 🎯 筛选标准

五维评分（1-10分），综合7分以上才推送：
1. **小众度**：赛道冷门程度
2. **跨界度**：跨领域创新
3. **监管友好度**：监管套利空间
4. **可执行性**：小团队可复制性
5. **商业想象力**：商业化潜力

## 📊 信息源

- ✅ Hacker News
- ⏳ Reddit (r/singularity, r/startups) - 待修复
- ⏳ Product Hunt - 待实现
- ⏳ Indie Hackers - 待实现
- ⏳ 36kr - 待实现
- ⏳ V2EX - 待实现

## 🛠 使用方法

### 手动运行
```bash
cd ~/.openclaw/workspace/explore/startup-inspiration
./run.sh
```

### 查看定时任务状态
```bash
systemctl --user status startup-inspiration.timer
```

### 查看运行日志
```bash
journalctl --user -u startup-inspiration.service -n 50
```

### 停止定时任务
```bash
systemctl --user stop startup-inspiration.timer
systemctl --user disable startup-inspiration.timer
```

### 重新启动定时任务
```bash
systemctl --user start startup-inspiration.timer
```

## 💰 成本优化

- 初筛：Haiku 4.5（便宜，~$0.001/条）
- 生成：Opus 4.6（质量，~$0.01/次）
- 每天预计成本：$0.05-0.10

## 📝 配置

编辑 `config.py` 可以修改：
- 评分阈值
- 每日推送数量
- 排除/优先关键词
- 信息源

## 🐛 已知问题

1. Reddit 爬虫需要修复（API 限制）
2. 其他信息源待实现
3. 周报功能待实现

## 📮 推送示例

每条案例包含：
- 一句话标题
- 所在赛道
- 团队规模
- 2-3句亮点说明
- 创业启发
- 五维评分
- 来源链接

最后附上今日趋势关键词。

## 🔧 维护

系统会自动运行，无需干预。如果想调整：
1. 修改 `config.py` 配置
2. 修改 `~/.config/systemd/user/startup-inspiration.timer` 改变运行时间
3. 运行 `systemctl --user daemon-reload` 重载配置

---

**下次运行时间**：每天早上 7:00
**推送目标**：Telegram (ID: 配置在 .env 的 TELEGRAM_CHAT_ID)
