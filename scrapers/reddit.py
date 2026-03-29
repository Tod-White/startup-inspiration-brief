"""
Reddit 爬虫
抓取 r/singularity 和 r/startups 的热门内容
"""

import requests
from datetime import datetime

class RedditScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def scrape_subreddit(self, subreddit, limit=25):
        """
        抓取指定 subreddit 的今日热门
        subreddit: "singularity" 或 "startups"
        """
        items = []
        
        try:
            # 使用 old.reddit.com（更稳定）
            url = f"https://old.reddit.com/r/{subreddit}/top/?t=day"
            response = requests.get(url, headers=self.headers, timeout=10)
            
            # 简单解析（不用 JSON API）
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            
            posts = soup.find_all('div', class_='thing', limit=limit)
            
            for post in posts:
                try:
                    title_elem = post.find('a', class_='title')
                    if not title_elem:
                        continue
                    
                    title = title_elem.text.strip()
                    url = title_elem.get('href', '')
                    
                    # 处理相对链接
                    if url.startswith('/r/'):
                        url = f"https://www.reddit.com{url}"
                    
                    # 获取分数
                    score_elem = post.find('div', class_='score unvoted')
                    score = 0
                    if score_elem:
                        score_text = score_elem.get('title', '0')
                        try:
                            score = int(score_text)
                        except:
                            score = 0
                    
                    # 只保留有一定热度的内容
                    if score < 50:
                        continue
                    
                    items.append({
                        "title": title,
                        "content": f"Upvotes: {score}",
                        "url": url,
                        "source": f"Reddit r/{subreddit}",
                        "score_raw": score,
                        "comments": 0
                    })
                    
                except Exception as e:
                    continue
            
            print(f"Reddit r/{subreddit}: 抓取到 {len(items)} 条")
            return items
            
        except Exception as e:
            print(f"Reddit r/{subreddit} 抓取失败: {e}")
            return []
    
    def scrape(self):
        """
        抓取所有配置的 subreddit
        """
        all_items = []
        
        # r/singularity
        all_items.extend(self.scrape_subreddit("singularity"))
        
        # r/startups
        all_items.extend(self.scrape_subreddit("startups"))
        
        return all_items

if __name__ == "__main__":
    scraper = RedditScraper()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- [{item['source']}] {item['title']} ({item['score_raw']} upvotes)")
