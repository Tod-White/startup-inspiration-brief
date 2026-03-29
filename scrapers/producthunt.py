"""
Product Hunt 爬虫
抓取今日热门产品
"""

import requests
from bs4 import BeautifulSoup

class ProductHuntScraper:
    def __init__(self):
        self.base_url = "https://www.producthunt.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self):
        """
        抓取 Product Hunt 今日热门
        """
        items = []
        
        try:
            response = requests.get(self.base_url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Product Hunt 的结构可能需要调整
            # 这里使用简单的标题和链接抓取
            posts = soup.find_all('a', href=lambda x: x and '/posts/' in x, limit=20)
            
            seen_urls = set()
            
            for post in posts:
                try:
                    url = post.get('href', '')
                    if not url or url in seen_urls:
                        continue
                    
                    if not url.startswith('http'):
                        url = f"{self.base_url}{url}"
                    
                    seen_urls.add(url)
                    
                    # 获取标题
                    title = post.get_text(strip=True)
                    if not title or len(title) < 5:
                        continue
                    
                    items.append({
                        "title": title,
                        "content": "Product Hunt 今日热门产品",
                        "url": url,
                        "source": "Product Hunt",
                        "score_raw": 0,
                        "comments": 0
                    })
                    
                except Exception as e:
                    continue
            
            print(f"Product Hunt: 抓取到 {len(items)} 条")
            return items[:15]  # 限制数量
            
        except Exception as e:
            print(f"Product Hunt 抓取失败: {e}")
            return []

if __name__ == "__main__":
    scraper = ProductHuntScraper()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']}")
