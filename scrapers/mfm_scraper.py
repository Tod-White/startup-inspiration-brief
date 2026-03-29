"""
抓取 My First Million 播客最新集
"""
import subprocess
import json
import re

PLAYWRIGHT_SIMPLE = "/root/.openclaw/workspace/skills/playwright-scraper-skill/scripts/playwright-simple.js"

class MFMScraper:
    def scrape(self):
        items = []
        print("正在抓取 My First Million...")
        try:
            result = subprocess.run(
                ["node", PLAYWRIGHT_SIMPLE, "https://www.mfmpod.com"],
                capture_output=True, text=True, timeout=30
            )
            stdout = result.stdout
            json_start = stdout.find('{')
            json_end = stdout.rfind('}') + 1
            data = json.loads(stdout[json_start:json_end])
            content = data.get("content", "")

            # 解析集数：日期 + 标题 + 摘要模式
            # 格式：月 日, 年\n标题\n摘要...\nListen to the Episode
            pattern = re.finditer(
                r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d+,\s+\d+\n(.+?)\n(.{30,300}?)\nListen to the Episode',
                content, re.DOTALL
            )
            for m in pattern:
                date = m.group(1)
                title = m.group(2).strip()
                summary = m.group(3).strip()[:300]
                items.append({
                    "title": title,
                    "content": summary,
                    "url": "https://www.mfmpod.com",
                    "source": "My First Million",
                    "score_raw": 0,
                    "comments": 0
                })
            print(f"My First Million: 抓取到 {len(items)} 条")
        except Exception as e:
            print(f"My First Million 失败: {e}")
        return items
