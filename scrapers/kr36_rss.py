"""
使用 RSS 抓取 36kr
"""

import feedparser
import requests
import io
import time

class Kr36RSS:
    def __init__(self):
        self.rss_url = "https://36kr.com/feed"
    
    def scrape(self):
        """
        使用 requests 抓取 36kr RSS，失败自动重试3次
        """
        for attempt in range(3):
            try:
                resp = requests.get(
                    self.rss_url,
                    timeout=30,
                    headers={'User-Agent': 'Mozilla/5.0'}
                )
                resp.raise_for_status()
                feed = feedparser.parse(io.BytesIO(resp.content))
                
                items = []
                for entry in feed.entries[:20]:
                    title = entry.get('title', '')
                    url = entry.get('link', '')
                    summary = entry.get('summary', '')
                    items.append({
                        "title": title,
                        "content": summary[:200] if summary else "36kr 最新资讯",
                        "url": url,
                        "source": "36kr",
                        "score_raw": 0,
                        "comments": 0
                    })
                
                print(f"36kr RSS: 抓取到 {len(items)} 条")
                return items
                
            except Exception as e:
                print(f"36kr RSS 失败 (第{attempt+1}次): {e}")
                if attempt < 2:
                    time.sleep(5)
        
        print("36kr RSS: 3次重试均失败，跳过")
        return []

if __name__ == "__main__":
    scraper = Kr36RSS()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']}")
