"""
使用官方 API 抓取 V2EX
"""

import requests

class V2EXAPI:
    def __init__(self):
        self.api_url = "https://www.v2ex.com/api/topics/hot.json"
    
    def scrape(self):
        """
        使用官方 API 抓取 V2EX 热门话题
        """
        items = []
        
        try:
            response = requests.get(self.api_url, timeout=10)
            topics = response.json()
            
            for topic in topics[:20]:
                title = topic.get('title', '')
                url = topic.get('url', '')
                replies = topic.get('replies', 0)
                
                # 只保留有一定讨论度的
                if replies < 10:
                    continue
                
                items.append({
                    "title": title,
                    "content": f"V2EX 热门话题 ({replies} 回复)",
                    "url": url if url.startswith('http') else f"https://www.v2ex.com{url}",
                    "source": "V2EX",
                    "score_raw": replies,
                    "comments": replies
                })
            
            print(f"V2EX API: 抓取到 {len(items)} 条")
            return items
            
        except Exception as e:
            print(f"V2EX API 失败: {e}")
            return []

if __name__ == "__main__":
    scraper = V2EXAPI()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']} ({item['score_raw']} 回复)")
