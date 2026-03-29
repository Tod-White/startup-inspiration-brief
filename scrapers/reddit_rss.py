"""
使用 RSS 抓取 Reddit 替代源
"""

import feedparser
import re

class RedditRSS:
    def __init__(self):
        self.sources = [
            ("Lobsters", "https://lobste.rs/rss"),
            ("TLDR AI", "https://tldr.tech/api/rss/ai")
        ]
    
    def scrape(self):
        """
        使用替代 RSS 源
        """
        all_items = []
        
        for source_name, rss_url in self.sources:
            try:
                feed = feedparser.parse(rss_url)
                
                for entry in feed.entries[:15]:  # 每个源取 15 条
                    title = entry.get('title', '')
                    url = entry.get('link', '')
                    summary = entry.get('summary', '')
                    
                    all_items.append({
                        "title": title,
                        "content": summary[:200] if summary else f"{source_name} 热门内容",
                        "url": url,
                        "source": source_name,
                        "score_raw": 0,
                        "comments": 0
                    })
                
                print(f"{source_name} RSS: 抓取到 {len([e for e in feed.entries[:15]])} 条")
                
            except Exception as e:
                print(f"{source_name} RSS 失败: {e}")
                continue
        
        print(f"Reddit 替代源: 总共抓取到 {len(all_items)} 条")
        return all_items

if __name__ == "__main__":
    scraper = RedditRSS()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- [{item['source']}] {item['title']}")
