"""
使用官方 API 抓取 Hacker News
"""

import requests

class HackerNewsAPI:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"
    
    def scrape(self):
        """
        使用官方 API 抓取 HN 最佳帖子
        """
        items = []
        
        try:
            # 获取最佳帖子 ID 列表
            response = requests.get(f"{self.base_url}/beststories.json", timeout=10)
            story_ids = response.json()[:50]  # 取前 50 个
            
            # 获取每个帖子的详情
            for story_id in story_ids:
                try:
                    story_response = requests.get(
                        f"{self.base_url}/item/{story_id}.json",
                        timeout=5
                    )
                    story = story_response.json()
                    
                    if not story:
                        continue
                    
                    title = story.get('title', '')
                    url = story.get('url', f"https://news.ycombinator.com/item?id={story_id}")
                    score = story.get('score', 0)
                    comments = story.get('descendants', 0)
                    
                    # 只保留有一定热度的
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
                    continue
            
            print(f"HN API: 抓取到 {len(items)} 条")
            return items
            
        except Exception as e:
            print(f"HN API 抓取失败: {e}")
            return []

if __name__ == "__main__":
    scraper = HackerNewsAPI()
    items = scraper.scrape()
    for item in items[:3]:
        print(f"- {item['title']} ({item['score_raw']} points)")
