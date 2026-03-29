"""
抓取 Side Hustle Show 播客 RSS
"""
import feedparser
import requests
import io

class SideHustleRSS:
    def __init__(self):
        self.rss_url = "https://sidehustlenation.libsyn.com/rss"

    def scrape(self):
        items = []
        try:
            resp = requests.get(self.rss_url, timeout=15, headers={'User-Agent': 'Mozilla/5.0'})
            resp.raise_for_status()
            feed = feedparser.parse(io.BytesIO(resp.content))
            for entry in feed.entries[:10]:
                title = entry.get('title', '')
                summary = entry.get('summary', '')
                url = entry.get('link', self.rss_url)
                items.append({
                    "title": title,
                    "content": summary[:300] if summary else title,
                    "url": url,
                    "source": "Side Hustle Show",
                    "score_raw": 0,
                    "comments": 0
                })
            print(f"Side Hustle Show RSS: 抓取到 {len(items)} 条")
        except Exception as e:
            print(f"Side Hustle Show RSS 失败: {e}")
        return items
