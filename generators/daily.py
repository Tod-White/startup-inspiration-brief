"""
每日简报生成器
使用 Sonnet 4.6 生成最终简报（性价比更高）
"""

import anthropic
from datetime import datetime
from config import OPENCLAW_API_BASE, OPENCLAW_API_KEY, MODEL_GOOD

class DailyReportGenerator:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=OPENCLAW_API_KEY,
            base_url=OPENCLAW_API_BASE
        )
    
    def generate(self, scored_items, success_sources=None, failed_sources=None, tech_items=None):
        """
        生成每日简报
        scored_items: 已评分并筛选后的案例列表
        success_sources: 成功的信息源列表
        failed_sources: 失败的信息源列表
        """
        
        if not scored_items:
            return "今日无符合标准的创业灵感案例。"
        
        # 构建案例列表
        JUNK_PATTERNS = ["I am Claude", "I'm Claude", "As an AI", "as an AI assistant", "OpenAI", "ChatGPT"]
        cases_text = ""
        for i, item in enumerate(scored_items, 1):
            content = item['content'][:300]
            # 过滤垃圾内容
            if any(p in content for p in JUNK_PATTERNS):
                content = "（内容抓取异常，见标题）"
            metaman_bonus = item['score'].get('metaman_bonus', 0)
            时效性 = item['score'].get('时效性', '')
            cases_text += f"""
案例 {i}:
标题: {item['title']}
来源: {item['source']}
链接: {item['url']}
评分: {item['score']['total']}分（Metaman加成: +{metaman_bonus}）
时效性: {时效性}
维度: {item['score']['scores']}
理由: {item['score']['reason']}
内容摘要: {content}

---
"""
        
        prompt = f"""你是一个创业灵感分析专家。请基于以下筛选后的案例，生成一份每日创业灵感简报。

今日案例（共{len(scored_items)}条）：
{cases_text}

**重要要求：**

1. **只选真实故事，不要产品发布**
   - 必须有具体的人/团队
   - 必须有具体的过程或数据
   - 不要"XX公司推出新工具"这种内容

2. **创业启发要有洞察力**
   - 不要写"选择垂直领域，用AI解决问题"这种万能句式
   - 要写出这个案例背后的反直觉模式
   - 要告诉我一个我没想到的东西
   - 例如："跨境电商的壁垒不是货，是语言+文化+运营。AI把这三道墙全推平了。而且他卖的是毛毯——越普通的品类，对手越想不到一个人能做到这种效率。"

3. **格式要灵活，不要千篇一律**
   - 不要每条都是"亮点+启发"的工整格式
   - 有的案例核心是数字，就放大数字
   - 有的案例核心是反直觉细节，就围绕细节展开
   - 有的案例之间有关联，就放在一起讲

4. **每条案例包含：**
   - 一句话标题（吸引人，突出核心）
   - 人物/团队（谁做的）
   - 具体做了什么（过程）
   - 关键数据（如果有）
   - 创业启发（有洞察力的分析，不是套话）
   - 五维评分 + Metaman加成（如果有加成，说明为什么跟他背景匹配）
   - 时效性评估（直接显示🔴/🟡/🟢及原因）
   - 来源链接

5. **最后附上3-5个今日趋势关键词**

6. **语气要简洁、有洞察力，不要废话**

开始生成简报："""

        try:
            response = self.client.messages.create(
                model=MODEL_GOOD,
                max_tokens=4000,
                messages=[{"role": "user", "content": prompt}]
            )
            
            report = response.content[0].text.strip()
            
            # 添加日期和统计
            today = datetime.now().strftime("%Y年%m月%d日")
            header = f"""# 🚀 创业灵感日报 - {today}

今日精选 {len(scored_items)} 条案例

"""
            
            # 添加信息源统计
            footer = "\n\n---\n\n## 📊 信息源统计\n\n"
            if success_sources:
                footer += f"✅ **成功**: {', '.join(success_sources)}\n\n"
            if failed_sources:
                footer += f"❌ **失败**: {', '.join(failed_sources)}\n\n"
            
            # 科技板块
            tech_section = ""
            if tech_items:
                tech_items_text = ""
                for item in tech_items:
                    tech_items_text += f"- 标题: {item['title']}\n  来源: {item['source']}\n  链接: {item['url']}\n  评分: {item['score']['total']}\n\n"
                tech_prompt = f"""以下是科技前沿内容，请将标题翻译为中文，并用一句话说明这是什么，格式如下：
• **中文标题**（评分分 | 来源）
  一句话说明
  🔗 链接

内容：
{tech_items_text}
只输出格式化结果，不要其他内容。"""
                tech_response = self.client.messages.create(
                    model=MODEL_GOOD,
                    max_tokens=800,
                    messages=[{"role": "user", "content": tech_prompt}]
                )
                tech_section = "\n\n---\n\n## 🔬 科技前沿（未入选主榜，供参考）\n\n" + tech_response.content[0].text.strip()

            return header + report + tech_section + footer
            
        except Exception as e:
            print(f"生成简报失败: {e}")
            return f"生成简报失败: {str(e)}"

if __name__ == "__main__":
    # 测试
    test_items = [
        {
            "title": "澳洲人用ChatGPT给流浪狗设计mRNA疫苗",
            "content": "一个没有生物学背景的人，用ChatGPT和AlphaFold给领养的癌症晚期流浪狗设计了定制mRNA疫苗，肿瘤缩小了。",
            "url": "https://example.com",
            "source": "Hacker News",
            "score": {
                "total": 8.4,
                "scores": {"小众度": 9, "跨界度": 9, "监管友好度": 8, "可执行性": 7, "商业想象力": 9},
                "reason": "宠物医疗是小众赛道，兽药审批宽松，个人用AI完成专业团队的工作"
            }
        }
    ]
    
    generator = DailyReportGenerator()
    report = generator.generate(test_items)
    print(report)
