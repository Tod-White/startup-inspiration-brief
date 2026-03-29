"""
使用 Playwright 抓取 Substack 榜单
"""
import subprocess
import json
import re

PLAYWRIGHT_SIMPLE = "/root/.openclaw/workspace/skills/playwright-scraper-skill/scripts/playwright-simple.js"

def scrape_substack(url, source_name, limit=15):
    items = []
    print(f"正在抓取 {source_name}...")
    try:
        result = subprocess.run(
            ["node", PLAYWRIGHT_SIMPLE, url],
            capture_output=True, text=True, timeout=30
        )
        # 找到输出中的 JSON 块
        stdout = result.stdout
        json_start = stdout.find('{')
        json_end = stdout.rfind('}') + 1
        data = json.loads(stdout[json_start:json_end])
        content = data.get("content", "")
        # 按行解析榜单条目（格式：序号 + 作者名 + 通讯名）
        lines = [l.strip() for l in content.split('\n') if l.strip()]
        i = 0
        while i < len(lines) and len(items) < limit:
            line = lines[i]
            # 跳过导航和UI元素
            if line in ['Home','Subscriptions','Chat','Activity','Explore','Profile','Create','Get app','Top Bestsellers','Rising','New Bestsellers']:
                i += 1
                continue
            # 跳过分类名
            if line in ['Culture','Technology','Business','Finance','Crypto','Science','Education']:
                i += 1
                continue
            # 数字序号行后面跟的是作者或通讯名
            if re.match(r'^\d+$', line):
                title_parts = []
                j = i + 1
                while j < len(lines) and j < i + 3:
                    if not re.match(r'^\d+$', lines[j]):
                        title_parts.append(lines[j])
                    else:
                        break
                    j += 1
                if title_parts:
                    title = ' - '.join(title_parts[:2])
                    items.append({
                        "title": title,
                        "content": f"Substack 热门通讯: {title}",
                        "url": url,
                        "source": source_name,
                        "score_raw": 0,
                        "comments": 0
                    })
                i = j
                continue
            i += 1
        print(f"{source_name}: 抓取到 {len(items)} 条")
    except Exception as e:
        print(f"{source_name} 失败: {e}")
    return items


class SubstackScraper:
    def scrape_business(self):
        return scrape_substack(
            "https://substack.com/discover/category/business",
            "Substack商业"
        )

    def scrape_tech(self):
        return scrape_substack(
            "https://substack.com/discover/category/technology",
            "Substack科技"
        )
