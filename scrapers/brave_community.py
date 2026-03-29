"""
用 Brave Search API 搜索社区讨论内容
"""
import requests
import os

BRAVE_API_KEY = os.environ.get('BRAVE_API_KEY', '')
BRAVE_SEARCH_URL = "https://api.search.brave.com/res/v1/web/search"

QUERIES = [
    ("site:reddit.com/r/indiehackers OR site:indiehackers.com revenue milestone", "社区-IH"),
    ("site:reddit.com/r/startups bootstrapped profitable", "社区-Reddit创业"),
    ("site:reddit.com/r/SideProject launched users", "社区-SideProject"),
]

class BraveCommunityScraper:
    def __init__(self):
        self.headers = {
            "Accept": "application/json",
            "X-Subscription-Token": BRAVE_API_KEY,
        }

    def scrape(self):
        items = []
        seen = set()
        print("正在抓取 Brave 社区内容...")
        for query, source_name in QUERIES:
            try:
                resp = requests.get(
                    BRAVE_SEARCH_URL,
                    headers=self.headers,
                    params={"q": query, "count": 10, "freshness": "pd"},
                    timeout=15
                )
                data = resp.json()
                for r in data.get("web", {}).get("results", []):
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
                print(f"Brave 社区抓取失败 ({query}): {e}")
        print(f"Brave 社区共抓取 {len(items)} 条")
        return items
