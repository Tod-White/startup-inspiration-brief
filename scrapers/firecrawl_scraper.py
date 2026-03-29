"""
使用 Firecrawl 抓取多个数据源
"""
import requests
import json
from config import FIRECRAWL_API_KEY

class FirecrawlScraper:
    def __init__(self):
        self.api_url = "https://api.firecrawl.dev/v1/scrape"
        self.headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }

    def scrape_url(self, url, source_name):
        try:
            resp = requests.post(self.api_url, headers=self.headers, json={
                "url": url,
                "formats": ["markdown"],
                "onlyMainContent": True,
                "timeout": 20000
            }, timeout=30)
            data = resp.json()
            markdown = data.get("data", {}).get("markdown", "")
            return markdown
        except Exception as e:
            print(f"{source_name} Firecrawl 失败: {e}")
            return ""

    def parse_36kr_startup(self):
        """抓取 36kr 早期项目——只取帖子标题链接"""
        items = []
        print("正在抓取 36kr 早期项目...")
        md = self.scrape_url("https://36kr.com/early-projects", "36kr早期项目")
        if not md:
            print("36kr 早期项目: 抓取失败")
            return items
        import re
        for m in re.finditer(r'\[([^\]]{10,80})\]\((https://36kr\.com/p/\d+[^)]*)', md):
            title, url = m.group(1).strip(), m.group(2)
            if any(x in title for x in ['账号', '登录', '注册', '设置', '氪']):
                continue
            items.append({
                "title": title,
                "content": title,
                "url": url,
                "source": "36kr早期项目",
                "score_raw": 0,
                "comments": 0
            })
            if len(items) >= 15:
                break
        print(f"36kr 早期项目: 抓取到 {len(items)} 条")
        return items

    def parse_sspai(self):
        """抓取少数派"""
        items = []
        print("正在抓取少数派...")
        md = self.scrape_url("https://sspai.com/tag/独立开发", "少数派")
        if not md:
            print("少数派: 抓取失败")
            return items
        lines = md.split("\n")
        for line in lines:
            line = line.strip()
            if len(line) > 20 and not line.startswith("#") and not line.startswith("!"):
                items.append({
                    "title": line[:100],
                    "content": line[:200],
                    "url": "https://sspai.com/tag/独立开发",
                    "source": "少数派",
                    "score_raw": 0,
                    "comments": 0
                })
            if len(items) >= 15:
                break
        print(f"少数派: 抓取到 {len(items)} 条")
        return items

    def parse_v2ex_startup(self):
        """抓取 V2EX 创业节点——只取帖子标题行"""
        items = []
        print("正在抓取 V2EX 创业节点...")
        md = self.scrape_url("https://www.v2ex.com/go/startup", "V2EX创业")
        if not md:
            print("V2EX 创业: 抓取失败")
            return items
        import re
        # 只取 markdown 链接标题，过滤导航/UI 噪音
        for m in re.finditer(r'\[([^\]]{10,80})\]\((https://www\.v2ex\.com/t/\d+[^)]*)', md):
            title, url = m.group(1).strip(), m.group(2)
            items.append({
                "title": title,
                "content": title,
                "url": url,
                "source": "V2EX创业",
                "score_raw": 0,
                "comments": 0
            })
            if len(items) >= 15:
                break
        print(f"V2EX 创业: 抓取到 {len(items)} 条")
        return items

    def parse_yc(self):
        """抓取 YC Show HN via HN search"""
        items = []
        print("正在抓取 YC/HN Show HN...")
        md = self.scrape_url("https://news.ycombinator.com/show", "YC")
        if not md:
            print("YC: 抓取失败")
            return items
        import re
        for m in re.finditer(r'\[([^\]]{15,100})\]\((https://[^)]+)\)', md):
            title, url = m.group(1).strip(), m.group(2)
            if 'ycombinator' in url or 'hacker' in url.lower():
                continue
            if title.lower() in ['more', 'hide', 'past', 'comments', 'ask', 'show', 'jobs']:
                continue
            items.append({
                "title": title,
                "content": title,
                "url": url,
                "source": "YC Show HN",
                "score_raw": 0,
                "comments": 0
            })
            if len(items) >= 15:
                break
        print(f"YC Show HN: 抓取到 {len(items)} 条")
        return items

    def parse_indiehackers(self):
        """抓取 Indie Hackers 帖子"""
        items = []
        print("正在抓取 Indie Hackers...")
        md = self.scrape_url("https://www.indiehackers.com/posts?sort=top&period=day", "IndieHackers")
        if not md:
            print("Indie Hackers: 抓取失败")
            return items
        import re
        # 匹配标题文字行（IH页面结构：标题在链接外）
        for m in re.finditer(r'\[([^\]]{15,120})\]\((https://www\.indiehackers\.com/[^)]+)', md):
            title, url = m.group(1).strip(), m.group(2)
            if any(x in title.lower() for x in ['sign in', 'log in', 'sign up', 'home', 'forum']):
                continue
            items.append({
                "title": title,
                "content": title,
                "url": url,
                "source": "IndieHackers",
                "score_raw": 0,
                "comments": 0
            })
            if len(items) >= 15:
                break
        print(f"Indie Hackers: 抓取到 {len(items)} 条")
        return items

    def parse_sspai(self):
        """抓取少数派独立开发"""
        items = []
        print("正在抓取少数派...")
        md = self.scrape_url("https://sspai.com/tag/独立开发", "少数派")
        if not md:
            print("少数派: 抓取失败")
            return items
        import re
        for m in re.finditer(r'\[([^\]]{10,80})\]\((https://sspai\.com/post/[^)]+)', md):
            title, url = m.group(1).strip(), m.group(2)
            items.append({
                "title": title,
                "content": title,
                "url": url,
                "source": "少数派",
                "score_raw": 0,
                "comments": 0
            })
            if len(items) >= 15:
                break
        print(f"少数派: 抓取到 {len(items)} 条")
        return items
