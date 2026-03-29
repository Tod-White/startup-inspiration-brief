"""
使用 RSS 抓取 How I Built This (NPR 播客)
有人、有故事、有数字 - 真实创业案例
"""

import feedparser
import socket
import re

class HowIBuiltThisRSS:
    def __init__(self):
        self.rss_url = "https://feeds.npr.org/510313/podcast.xml"
    
    def scrape(self):
        items = []
        
        try:
            socket.setdefaulttimeout(8)
            feed = feedparser.parse(self.rss_url)
            
            for entry in feed.entries[:15]:
                title = entry.get('title', '')
                url = entry.get('link', '')
                summary = entry.get('summary', '')
                
                # 去掉 HTML 标签
                summary = re.sub(r'<[^>]+>', '', summary)
                
                # 过滤掉 Advice Line 类型（不是具体创业故事）
                if 'Advice Line' in title:
                    continue
                
                items.append({
                    "title": title,
                    "content": summary[:300] if summary else title,
                    "url": url,
                    "source": "How I Built This",
                    "score_raw": 0,
                    "comments": 0
                })
            
            print(f"How I Built This: 抓取到 {len(items)} 条")
            return items
            
        except Exception as e:
            print(f"How I Built This RSS 失败: {e}")
            return []

if __name__ == "__main__":
    scraper = HowIBuiltThisRSS()
    items = scraper.scrape()
    for item in items[:5]:
        print(f"- {item['title']}")
        print(f"  {item['content'][:100]}")
        print()
