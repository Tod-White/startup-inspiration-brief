"""
Hacker News 爬虫
抓取过去24小时的热门内容
"""

import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta

class HackerNewsScraper:
    def __init__(self):
        self.base_url = "https://news.ycombinator.com"
    
    def scrape(self):
        """
        抓取 Hacker News Best 页面
        返回: [{"title": "", "content": "", "url": "", "source": "HN"}]
        """
        items = []
        
        try:
            # 抓取 best 页面
            response = requests.get(f"{self.base_url}/best", timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 解析条目
            rows = soup.find_all('tr', class_='athing')
            
            for row in rows[:50]:  # 增加到 50 条
                try:
                    title_elem = row.find('span', class_='titleline')
                    if not title_elem:
                        continue
                    
                    link = title_elem.find('a')
                    if not link:
                        continue
                    
                    title = link.text.strip()
                    url = link.get('href', '')
                    
                    # 处理相对链接
                    if url.startswith('item?id='):
                        url = f"{self.base_url}/{url}"
                    
                    # 获取评论数和分数
                    next_row = row.find_next_sibling('tr')
                    score = 0
                    comments = 0
                    
                    if next_row:
                        score_elem = next_row.find('span', class_='score')
                        if score_elem:
                            score = int(score_elem.text.split()[0])
                        
                        comment_elem = next_row.find_all('a')[-1]
                        if comment_elem and 'comment' in comment_elem.text:
                            comments_text = comment_elem.text.split()[0]
                            if comments_text.isdigit():
                                comments = int(comments_text)
                    
                    # 只保留有一定热度的内容
                    if score < 50:
                        continue
                    
                    items.append({
                        "title": title,
                        "content": f"Score: {score}, Comments: {comments}",
                        "url": url,
                        "source": "Hacker News",
                        "score_raw": score,
                        "comments": comments
                    })
                    
                except Exception as e:
                    print(f"解析HN条目失败: {e}")
                    continue
            
            print(f"HN: 抓取到 {len(items)} 条")
            return items
            
        except Exception as e:
            print(f"HN抓取失败: {e}")
            return []

if __name__ == "__main__":
    scraper = HackerNewsScraper()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']} ({item['score_raw']} points)")
