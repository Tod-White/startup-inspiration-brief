"""
用 Brave News API 抓创业相关新闻
"""
import requests
import os

BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', '')
BRAVE_NEWS_URL = "https://api.search.brave.com/res/v1/news/search"

QUERIES = [
    ("startup founder story revenue", "Brave新闻-创业"),
    ("side hustle income niche business", "Brave新闻-副业"),
    ("indie hacker bootstrapped product launch", "Brave新闻-独立开发"),
]

class BraveNewsScraper:
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY,
        }

    def scrape(self):
        items = []
        seen = set()
        print("正在抓取 Brave News...")
        for query, source_name in QUERIES:
            try:
                resp = requests.get(
                    BRAVE_NEWS_URL,
                    headers=self.headers,
                    params={"q": query, "count": 10, "freshness": "pd"},
                    timeout=15
                )
                data = resp.json()
                for r in data.get("results", []):
                    title = r.get("title", "").strip()
                    url = r.get("url", "")
                    desc = r.get("description", "").strip()
                    if not title or url in seen:
                        continue
                    seen.add(url)
                    items.append({
                        "title": title,
                        "url": url,
                        "summary": desc,
                        "source": source_name
                    })
            except Exception as e:
                print(f"Brave News 抓取失败 ({query}): {e}")
        print(f"Brave News 共抓取 {len(items)} 条")
        return items
