"""
使用 web_fetch 工具抓取 Indie Hackers
"""

import subprocess
import json
import re

class IndieHackersWebFetcher:
    def __init__(self):
        self.url = "https://www.indiehackers.com/"
    
    def scrape(self):
        """
        使用 OpenClaw web_fetch 抓取 Indie Hackers
        """
        items = []
        
        try:
            # 调用 openclaw web_fetch
            cmd = [
                "openclaw", "web", "fetch",
                self.url,
                "--extract-mode", "text",
                "--max-chars", "10000"
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode != 0:
                print(f"Indie Hackers 抓取失败: {result.stderr}")
                return []
            
            # 解析输出
            text = result.stdout
            
            # 提取标题和链接（简单正则）
            # 格式: "标题\n作者\n数字 upvotes\n数字 comments"
            lines = text.split('\n')
            
            current_title = None
            for i, line in enumerate(lines):
                line = line.strip()
                
                # 跳过空行和短行
                if len(line) < 10:
                    continue
                
                # 检测是否是标题（包含冒号或问号，且不是数字开头）
                if (':' in line or '?' in line) and not line[0].isdigit():
                    # 检查下一行是否有 upvotes
                    if i + 2 < len(lines) and 'upvotes' in lines[i + 2]:
                        current_title = line
                        
                        # 提取 upvotes 数量
                        upvotes_line = lines[i + 2]
                        upvotes_match = re.search(r'(\d+)\s*upvotes', upvotes_line)
                        upvotes = int(upvotes_match.group(1)) if upvotes_match else 0
                        
                        # 只保留有一定热度的
                        if upvotes >= 5:
                            items.append({
                                "title": current_title,
                                "content": f"Indie Hackers 热门帖子 ({upvotes} upvotes)",
                                "url": self.url,  # 暂时用首页链接
                                "source": "Indie Hackers",
                                "score_raw": upvotes,
                                "comments": 0
                            })
            
            print(f"Indie Hackers: 抓取到 {len(items)} 条")
            return items[:15]
            
        except Exception as e:
            print(f"Indie Hackers 抓取失败: {e}")
            return []

if __name__ == "__main__":
    scraper = IndieHackersWebFetcher()
    items = scraper.scrape()
    for item in items[:5]:
        print(f"- {item['title']} ({item['score_raw']} upvotes)")
