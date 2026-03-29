"""
使用 RSS 抓取 Product Hunt
"""

import feedparser

class ProductHuntRSS:
    def __init__(self):
        self.rss_url = "https://www.producthunt.com/feed"
    
    def scrape(self):
        """
        使用 RSS 抓取 Product Hunt
        """
        items = []
        
        try:
            feed = feedparser.parse(self.rss_url)
            
            for entry in feed.entries[:20]:
                title = entry.get('title', '')
                url = entry.get('link', '')
                summary = entry.get('summary', '')
                
                items.append({
                    "title": title,
                    "content": summary[:200] if summary else "Product Hunt 今日产品",
                    "url": url,
                    "source": "Product Hunt",
                    "score_raw": 0,
                    "comments": 0
                })
            
            print(f"Product Hunt RSS: 抓取到 {len(items)} 条")
            return items
            
        except Exception as e:
            print(f"Product Hunt RSS 失败: {e}")
            return []

if __name__ == "__main__":
    scraper = ProductHuntRSS()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']}")
