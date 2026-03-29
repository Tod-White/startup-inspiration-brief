"""
主程序
协调爬虫、筛选、生成、推送
"""

import sys
import os
import glob
import re
from pathlib import Path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from datetime import datetime, timezone
from scrapers.hackernews_api import HackerNewsAPI
from scrapers.reddit_rss import RedditRSS
from scrapers.producthunt_rss import ProductHuntRSS
from scrapers.indiehackers_rss import IndieHackersRSS
from scrapers.v2ex_api import V2EXAPI
from scrapers.kr36_rss import Kr36RSS
from scrapers.howitbuilt_rss import HowIBuiltThisRSS
from scrapers.sidehustle_rss import SideHustleRSS
from scrapers.mfm_scraper import MFMScraper
from scrapers.brave_news import BraveNewsScraper
from scrapers.brave_community import BraveCommunityScraper
from scrapers.firecrawl_scraper import FirecrawlScraper
from scrapers.substack_scraper import SubstackScraper
from filters.scorer import ContentScorer
from generators.daily import DailyReportGenerator
from config import MIN_ITEMS, MAX_ITEMS, TELEGRAM_CHAT_ID
import subprocess

def send_telegram(message):
    """
    通过 OpenClaw 发送 Telegram 消息
    """
    try:
        # 使用完整路径的 openclaw CLI
        cmd = [
            "/root/.nvm/versions/node/v22.22.1/bin/openclaw", 
            "message", "send",
            "--target", TELEGRAM_CHAT_ID,
            "--message", message
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Telegram 推送成功")
            return True
        else:
            print(f"❌ Telegram 推送失败: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Telegram 推送异常: {e}")
        return False

def main():
    print("=" * 50)
    print("🚀 创业灵感信息系统 - 开始运行")
    print("=" * 50)
    print(f"时间: {datetime.now()}")
    
    # 启动时通知用户
    send_telegram("📡 创业简报已启动，正在抓取数据，约20分钟后推送今日内容...")
    
    # 0. 加载历史已推送的 URL 和标题，用于去重
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    seen_urls = set()
    seen_titles = set()
    archives = sorted(glob.glob(os.path.join(archive_dir, "*.md")))  # 取所有历史文件去重
    for f in archives:
        content = Path(f).read_text(encoding='utf-8')
        seen_urls.update(re.findall(r'https?://[^\s)\]]+', content))
        for title_match in re.findall(r'(?:##\s*\d+[｜|]\s*|^\d+\.\s+)(.+)', content, re.MULTILINE):
            seen_titles.add(title_match.strip().lower()[:40])
    print(f"📋 已加载历史去重 URL {len(seen_urls)} 条，标题 {len(seen_titles)} 条")

    # 1. 数据抓取
    print("\n📡 步骤1: 抓取数据...")
    all_items = []
    success_sources = []
    failed_sources = []
    
    # Hacker News API
    print("正在抓取 Hacker News API...")
    try:
        hn_scraper = HackerNewsAPI()
        hn_items = hn_scraper.scrape()
        all_items.extend(hn_items)
        if hn_items:
            success_sources.append(f"Hacker News ({len(hn_items)}条)")
        else:
            failed_sources.append("Hacker News")
    except Exception as e:
        print(f"HN 失败: {e}")
        failed_sources.append("Hacker News")
    
    # Reddit RSS（暂时禁用 - 网络超时）
    # print("正在抓取 Reddit RSS...")
    # try:
    #     reddit_scraper = RedditRSS()
    #     reddit_items = reddit_scraper.scrape()
    #     all_items.extend(reddit_items)
    #     if reddit_items:
    #         success_sources.append(f"Reddit ({len(reddit_items)}条)")
    #     else:
    #         failed_sources.append("Reddit")
    # except Exception as e:
    #     print(f"Reddit 失败: {e}")
    #     failed_sources.append("Reddit")
    # Product Hunt RSS
    print("正在抓取 Product Hunt RSS...")
    try:
        ph_scraper = ProductHuntRSS()
        ph_items = ph_scraper.scrape()
        all_items.extend(ph_items)
        if ph_items:
            success_sources.append(f"Product Hunt ({len(ph_items)}条)")
        else:
            failed_sources.append("Product Hunt")
    except Exception as e:
        print(f"Product Hunt 失败: {e}")
        failed_sources.append("Product Hunt")
    
    # Indie Hackers RSS（暂时禁用 - RSS 源失效）
    # print("正在抓取 Indie Hackers RSS...")
    # try:
    #     ih_scraper = IndieHackersRSS()
    #     ih_items = ih_scraper.scrape()
    #     all_items.extend(ih_items)
    #     if ih_items:
    #         success_sources.append(f"Indie Hackers ({len(ih_items)}条)")
    #     else:
    #         failed_sources.append("Indie Hackers")
    # except Exception as e:
    #     print(f"Indie Hackers 失败: {e}")
    #     failed_sources.append("Indie Hackers")
    # V2EX API
    print("正在抓取 V2EX API...")
    try:
        v2ex_scraper = V2EXAPI()
        v2ex_items = v2ex_scraper.scrape()
        all_items.extend(v2ex_items)
        if v2ex_items:
            success_sources.append(f"V2EX ({len(v2ex_items)}条)")
        else:
            failed_sources.append("V2EX")
    except Exception as e:
        print(f"V2EX 失败: {e}")
        failed_sources.append("V2EX")
    
    # 36kr RSS
    print("正在抓取 36kr RSS...")
    try:
        kr36_scraper = Kr36RSS()
        kr36_items = kr36_scraper.scrape()
        all_items.extend(kr36_items)
        if kr36_items:
            success_sources.append(f"36kr ({len(kr36_items)}条)")
        else:
            failed_sources.append("36kr")
    except Exception as e:
        print(f"36kr 失败: {e}")
        failed_sources.append("36kr")
    
    # How I Built This RSS
    print("正在抓取 How I Built This...")
    try:
        hibt_scraper = HowIBuiltThisRSS()
        hibt_items = hibt_scraper.scrape()
        all_items.extend(hibt_items)
        if hibt_items:
            success_sources.append(f"How I Built This ({len(hibt_items)}条)")
        else:
            failed_sources.append("How I Built This")
    except Exception as e:
        print(f"How I Built This 失败: {e}")
        failed_sources.append("How I Built This")
    
    # Brave Community (Reddit + IndieHackers)
    print("正在抓取 Reddit/IndieHackers (via Brave)...")
    try:
        brave_community = BraveCommunityScraper()
        community_items = brave_community.scrape()
        all_items.extend(community_items)
        if community_items:
            success_sources.append(f"Reddit/IndieHackers ({len(community_items)}条)")
        else:
            failed_sources.append("Reddit/IndieHackers")
    except Exception as e:
        print(f"Brave Community 失败: {e}")
        failed_sources.append("Reddit/IndieHackers")

    # Brave News
    print("正在抓取 Brave News...")
    try:
        brave_scraper = BraveNewsScraper()
        brave_items = brave_scraper.scrape()
        all_items.extend(brave_items)
        if brave_items:
            success_sources.append(f"Brave新闻 ({len(brave_items)}条)")
        else:
            failed_sources.append("Brave新闻")
    except Exception as e:
        print(f"Brave News 失败: {e}")
        failed_sources.append("Brave新闻")

    # My First Million
    print("正在抓取 My First Million...")
    try:
        mfm_scraper = MFMScraper()
        mfm_items = mfm_scraper.scrape()
        all_items.extend(mfm_items)
        if mfm_items:
            success_sources.append(f"My First Million ({len(mfm_items)}条)")
        else:
            failed_sources.append("My First Million")
    except Exception as e:
        print(f"My First Million 失败: {e}")
        failed_sources.append("My First Million")

    # Side Hustle Show RSS
    print("正在抓取 Side Hustle Show...")
    try:
        shs_scraper = SideHustleRSS()
        shs_items = shs_scraper.scrape()
        all_items.extend(shs_items)
        if shs_items:
            success_sources.append(f"Side Hustle Show ({len(shs_items)}条)")
        else:
            failed_sources.append("Side Hustle Show")
    except Exception as e:
        print(f"Side Hustle Show 失败: {e}")
        failed_sources.append("Side Hustle Show")

    # Firecrawl 数据源
    firecrawl = FirecrawlScraper()
    # Substack
    substack = SubstackScraper()
    for method, name in [(substack.scrape_business, 'Substack商业'), (substack.scrape_tech, 'Substack科技')]:
        try:
            items = method()
            all_items.extend(items)
            if items:
                success_sources.append(f"{name} ({len(items)}条)")
            else:
                failed_sources.append(name)
        except Exception as e:
            print(f"{name} 失败: {e}")
            failed_sources.append(name)

    for method, name in [(firecrawl.parse_v2ex_startup, 'V2EX创业'), (firecrawl.parse_yc, 'YC Show HN')]:
        try:
            items = method()
            all_items.extend(items)
            if items:
                success_sources.append(f"{name} ({len(items)}条)")
            else:
                failed_sources.append(name)
        except Exception as e:
            print(f"{name} 失败: {e}")
            failed_sources.append(name)

    print(f"✅ 共抓取 {len(all_items)} 条原始内容")
    print(f"✅ 成功信息源: {', '.join(success_sources) if success_sources else '无'}")
    if failed_sources:
        print(f"❌ 失败信息源: {', '.join(failed_sources)}")
    
    if not all_items:
        print("❌ 没有抓取到任何内容，退出")
        return
    
    # 2. AI 筛选和打分
    print("\n🤖 步骤2: AI筛选和打分（使用Sonnet）...")
    print(f"开始评分 {len(all_items)} 条内容...")
    scorer = ContentScorer()
    
    # 评分所有内容（不限制数量）
    print(f"实际评分: {len(all_items)} 条")
    
    # batch_score 返回所有已评分内容（含不合格的）
    all_scored = scorer.batch_score_all(all_items)
    
    # 按分数排序
    all_scored.sort(key=lambda x: x['score']['total'], reverse=True)
    
    qualified_items = [x for x in all_scored if x['score']['qualified']]
    print(f"✅ 筛选出 {len(qualified_items)} 条合格内容")
    
    # 强制补齐到 MIN_ITEMS，从已评分内容里按分数补
    if len(qualified_items) < MIN_ITEMS:
        extras = [x for x in all_scored if not x['score']['qualified']]
        needed = MIN_ITEMS - len(qualified_items)
        qualified_items.extend(extras[:needed])
        print(f"⚠️  补齐至 {len(qualified_items)} 条（含低分内容）")
    
    if not qualified_items:
        print("❌ 没有任何内容，退出")
        return
    
    # 3. 科技板块：从所有评分内容里单独挑科技相关
    TECH_KEYWORDS = ['AI', 'LLM', 'GPT', '模型', '算法', 'open source', 'GitHub', 'Show HN',
                     'machine learning', 'neural', 'robot', 'quantum', '芯片', '大模型', '推理']
    tech_items = [
        x for x in all_scored
        if any(kw.lower() in x['title'].lower() or kw.lower() in x['content'].lower() for kw in TECH_KEYWORDS)
        and x not in qualified_items
    ]
    tech_items.sort(key=lambda x: x['score']['total'], reverse=True)
    tech_items = tech_items[:5]

    # 4. 去重：过滤掉历史已出现的URL和标题
    if seen_urls or seen_titles:
        before = len(qualified_items)
        def is_seen(item):
            if item.get('url', '') in seen_urls:
                return True
            title_key = item.get('title', '').strip().lower()[:40]
            if title_key and title_key in seen_titles:
                return True
            return False
        qualified_items = [x for x in qualified_items if not is_seen(x)]
        print(f"🔄 去重后：{before} → {len(qualified_items)} 条")
    
    # 限制数量
    final_items = qualified_items[:MAX_ITEMS]
    
    print(f"📊 最终推送 {len(final_items)} 条")
    
    # 4. 生成简报
    print("\n✍️  步骤3: 生成简报（使用Sonnet）...")
    generator = DailyReportGenerator()
    report = generator.generate(final_items, success_sources, failed_sources, tech_items=tech_items)
    
    print("✅ 简报生成完成")
    print("\n" + "=" * 50)
    print(report[:500] + "...")
    print("=" * 50)
    
    # 5. 存档简报
    archive_dir = os.path.join(os.path.dirname(__file__), "archive")
    os.makedirs(archive_dir, exist_ok=True)
    archive_file = os.path.join(archive_dir, f"{datetime.now(timezone.utc).strftime('%Y-%m-%d')}.md")
    with open(archive_file, "w", encoding="utf-8") as f:
        f.write(report)
    print(f"📁 简报已存档: archive/{datetime.now().strftime('%Y-%m-%d')}.md")

    # 6. 推送到 Telegram
    print("\n📤 步骤5: 推送到Telegram...")
    success = send_telegram(report)
    
    if success:
        print("\n🎉 任务完成！")
    else:
        print("\n❌ 推送失败，但简报已生成")
        print("简报内容：")
        print(report)

if __name__ == "__main__":
    main()
