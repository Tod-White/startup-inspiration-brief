"""
Indie Hackers 爬虫
抓取热门帖子
"""

import requests
from bs4 import BeautifulSoup

class IndieHackersScraper:
    def __init__(self):
        self.base_url = "https://www.indiehackers.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self):
        """
        抓取 Indie Hackers 热门内容
        """
        items = []
        
        try:
            # 抓取首页热门
            response = requests.get(f"{self.base_url}/top", headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找帖子链接
            links = soup.find_all('a', href=lambda x: x and '/post/' in x, limit=20)
            
            seen_urls = set()
            
            for link in links:
                try:
                    url = link.get('href', '')
                    if not url or url in seen_urls:
                        continue
                    
                    if not url.startswith('http'):
                        url = f"{self.base_url}{url}"
                    
                    seen_urls.add(url)
                    
                    title = link.get_text(strip=True)
                    if not title or len(title) < 5:
                        continue
                    
                    items.append({
                        "title": title,
                        "content": "Indie Hackers 热门帖子",
                        "url": url,
                        "source": "Indie Hackers",
                        "score_raw": 0,
                        "comments": 0
                    })
                    
                except Exception as e:
                    continue
            
            print(f"Indie Hackers: 抓取到 {len(items)} 条")
            return items[:15]
            
        except Exception as e:
            print(f"Indie Hackers 抓取失败: {e}")
            return []

if __name__ == "__main__":
    scraper = IndieHackersScraper()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']}")
