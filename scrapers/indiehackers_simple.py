"""
使用 requests + BeautifulSoup 抓取 Indie Hackers
"""

import requests
from bs4 import BeautifulSoup
import re

class IndieHackersSimpleScraper:
    def __init__(self):
        self.url = "https://www.indiehackers.com/"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape(self):
        """
        抓取 Indie Hackers 首页
        """
        items = []
        
        try:
            response = requests.get(self.url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取所有文本
            text = soup.get_text()
            
            # 简单解析：查找包含 "upvotes" 的行
            lines = text.split('\n')
            
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 查找 upvotes 行
                if 'upvotes' in line.lower():
                    # 提取数字
                    match = re.search(r'(\d+)\s*upvotes', line, re.IGNORECASE)
                    if match:
                        upvotes = int(match.group(1))
                        
                        # 只保留 5+ upvotes
                        if upvotes < 5:
                            continue
                        
                        # 向上查找标题（前几行）
                        title = None
                        for j in range(max(0, i-5), i):
                            candidate = lines[j].strip()
                            if len(candidate) > 20 and ':' in candidate:
                                title = candidate
                                break
                        
                        if title:
                            items.append({
                                "title": title,
                                "content": f"Indie Hackers 热门 ({upvotes} upvotes)",
                                "url": self.url,
                                "source": "Indie Hackers",
                                "score_raw": upvotes,
                                "comments": 0
                            })
            
            # 去重
            seen = set()
            unique_items = []
            for item in items:
                if item['title'] not in seen:
                    seen.add(item['title'])
                    unique_items.append(item)
            
            print(f"Indie Hackers: 抓取到 {len(unique_items)} 条")
            return unique_items[:15]
            
        except Exception as e:
            print(f"Indie Hackers 抓取失败: {e}")
            return []

if __name__ == "__main__":
    scraper = IndieHackersSimpleScraper()
    items = scraper.scrape()
    for item in items[:5]:
        print(f"- {item['title']} ({item['score_raw']} upvotes)")
