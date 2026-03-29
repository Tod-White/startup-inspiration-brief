"""
使用 Firecrawl 抓取 Indie Hackers 帖子
"""

import requests
import json
import os

FIRECRAWL_API_KEY = os.environ.get('FIRECRAWL_API_KEY', '')

class IndieHackersRSS:
    def __init__(self):
        self.api_url = "https://api.firecrawl.dev/v1/scrape"
        self.headers = {
            "Authorization": f"Bearer {FIRECRAWL_API_KEY}",
            "Content-Type": "application/json"
        }
    
    def scrape(self):
        """
        使用 Firecrawl 抓取 Indie Hackers 最新帖子
        """
        items = []
        
        urls = [
            "https://www.indiehackers.com/posts",
            "https://www.indiehackers.com/interviews"
        ]
        
        for url in urls:
            try:
                payload = {
                    "url": url,
                    "formats": ["markdown"],
                    "onlyMainContent": True
                }
                
                response = requests.post(
                    self.api_url,
                    headers=self.headers,
                    json=payload,
                    timeout=30
                )
                
                data = response.json()
                
                if not data.get('success'):
                    print(f"Indie Hackers Firecrawl 失败: {data}")
                    continue
                
                markdown = data.get('data', {}).get('markdown', '')
                
                # 解析 markdown 中的帖子
                lines = markdown.split('\n')
                current_title = ''
                current_content = []
                
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    
                    # 标题行（以 ## 开头）
                    if line.startswith('## ') or line.startswith('# '):
                        # 保存上一条
                        if current_title and len(current_content) > 0:
                            content_text = ' '.join(current_content[:5])
                            # 过滤掉太短或无意义的内容
                            if len(content_text) > 50:
                                items.append({
                                    "title": current_title,
                                    "content": content_text[:300],
                                    "url": url,
                                    "source": "Indie Hackers",
                                    "score_raw": 0,
                                    "comments": 0
                                })
                        current_title = line.lstrip('#').strip()
                        current_content = []
                    elif current_title and line and not line.startswith('!'):
                        current_content.append(line)
                
                # 保存最后一条
                if current_title and len(current_content) > 0:
                    content_text = ' '.join(current_content[:5])
                    if len(content_text) > 50:
                        items.append({
                            "title": current_title,
                            "content": content_text[:300],
                            "url": url,
                            "source": "Indie Hackers",
                            "score_raw": 0,
                            "comments": 0
                        })
                
            except Exception as e:
                print(f"Indie Hackers 抓取失败 ({url}): {e}")
                continue
        
        # 去重（按标题）
        seen = set()
        unique_items = []
        for item in items:
            if item['title'] not in seen and len(item['title']) > 5:
                seen.add(item['title'])
                unique_items.append(item)
        
        print(f"Indie Hackers: 抓取到 {len(unique_items)} 条")
        return unique_items[:20]  # 最多返回 20 条

if __name__ == "__main__":
    scraper = IndieHackersRSS()
    items = scraper.scrape()
    for item in items[:5]:
        print(f"- {item['title']}")
        print(f"  {item['content'][:100]}")
