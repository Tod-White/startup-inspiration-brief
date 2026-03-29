"""
五维评分系统
使用便宜的 Haiku 模型进行初筛和打分
"""

import anthropic
import time
from config import OPENCLAW_API_BASE, OPENCLAW_API_KEY, MODEL_CHEAP, SCORE_DIMENSIONS, SCORE_THRESHOLD

class ContentScorer:
    def __init__(self):
        self.client = anthropic.Anthropic(
            api_key=OPENCLAW_API_KEY,
            base_url=OPENCLAW_API_BASE
        )
    
    JUNK_PATTERNS = ["I am Claude", "I'm Claude", "I am an AI assistant", "As an AI language model"]

    def score_content(self, title, content, url):
        """
        对单条内容进行五维打分
        返回: {
            "scores": {"小众度": 8, "跨界度": 7, ...},
            "total": 7.6,
            "reason": "评分理由",
            "qualified": True/False
        }
        """
        # 过滤垃圾内容
        if any(p in content for p in self.JUNK_PATTERNS):
            return {"scores": {}, "total": 0, "reason": "内容含垃圾文本，自动过滤", "qualified": False}
        
        prompt = f"""请对以下内容进行创业价值评分（1-10分）：

标题：{title}
内容：{content[:500]}

**核心筛选标准（必须满足至少2项）：**
1. 有具体的人或团队？（名字、背景、团队规模）
2. 有具体做了什么？（过程、方法、时间线）
3. 有具体数据？（营收、用户数、成本、增长率、时间）

**优先内容：**
- 真实创业者的第一人称分享
- 有具体数字的案例（"4个月做到500万"）
- 小团队/个人的成功故事
- 有反直觉细节的案例

**排除内容：**
- 纯产品发布（"XX公司推出新工具"）
- 没有数据的泛泛介绍
- 大公司新闻
- 融资消息（除非有具体运营数据）

评分维度（每项1-10分）：
1. 小众度：赛道冷门程度
2. 跨界度：跨领域创新
3. 监管友好度：监管套利空间
4. 可执行性：小团队可复制性
5. 商业想象力：商业化潜力

**Metaman适配度加成（在总分基础上额外加分，不单独计入维度）：**
Metaman的背景：NHS内部工作者、建筑/医疗设施专业、AI动手能力强、南伦敦/英国市场、华人圈渠道（伴侣擅长小红书）。
- 强匹配（案例与以上背景高度契合，他有明显先发优势）：加2分
- 一般匹配（有一定关联）：加1分
- 无匹配：加0分

**时效性评估（单独给出，不计入总分）：**
- 🔴 窗口已关：竞争已饱和，进入太晚
- 🟡 还有1-2年：窗口期收窄，需尽快行动
- 🟢 早期：现在进入正好，竞争少

**重要：无论内容是否合适，都必须返回JSON格式的评分。**
如果不符合核心筛选标准，所有维度给1-3分。

返回格式（必须是纯JSON，不要其他文字）：
{{
    "小众度": 2,
    "跨界度": 1,
    "监管友好度": 1,
    "可执行性": 1,
    "商业想象力": 1,
    "metaman_bonus": 0,
    "时效性": "🔴 窗口已关",
    "reason": "不符合标准的原因"
}}"""

        import json
        max_retries = 3
        retry_delays = [10, 30, 60]  # 每次重试等待秒数
        
        for attempt in range(max_retries):
            try:
                response = self.client.messages.create(
                    model=MODEL_CHEAP,
                    max_tokens=500,
                    messages=[{"role": "user", "content": prompt}]
                )
                
                result_text = response.content[0].text.strip()
                
                # 提取JSON（可能包含markdown代码块或其他文本）
                if "```json" in result_text:
                    result_text = result_text.split("```json")[1].split("```")[0].strip()
                elif "```" in result_text:
                    result_text = result_text.split("```")[1].split("```")[0].strip()
                
                # 如果还有其他文本，尝试找到 JSON 对象
                if not result_text.startswith("{"):
                    start = result_text.find("{")
                    end = result_text.rfind("}") + 1
                    if start != -1 and end > start:
                        result_text = result_text[start:end]
                
                scores_data = json.loads(result_text)
                
                # 计算总分
                scores = {dim: scores_data.get(dim, 0) for dim in SCORE_DIMENSIONS}
                total = sum(scores.values()) / len(scores)
                metaman_bonus = scores_data.get("metaman_bonus", 0)
                total_with_bonus = round(total + metaman_bonus, 1)
                时效性 = scores_data.get("时效性", "")
                
                return {
                    "scores": scores,
                    "total": total_with_bonus,
                    "metaman_bonus": metaman_bonus,
                    "时效性": 时效性,
                    "reason": scores_data.get("reason", ""),
                    "qualified": total_with_bonus >= SCORE_THRESHOLD
                }
                
            except Exception as e:
                err_str = str(e)
                is_rate_limit = "cooldown" in err_str or "service_busy" in err_str or "529" in err_str or "rate" in err_str.lower()
                
                if is_rate_limit and attempt < max_retries - 1:
                    wait = retry_delays[attempt]
                    print(f"评分失败(API限流), {wait}秒后重试({attempt+1}/{max_retries})")
                    time.sleep(wait)
                    continue
                else:
                    print(f"评分失败: {e}")
                    return {
                        "scores": {dim: 0 for dim in SCORE_DIMENSIONS},
                        "total": 0,
                        "reason": f"评分失败: {err_str}",
                        "qualified": False
                    }
        
        # 所有重试都失败
        return {
            "scores": {dim: 0 for dim in SCORE_DIMENSIONS},
            "total": 0,
            "reason": "评分失败: 超过最大重试次数",
            "qualified": False
        }
    
    def batch_score(self, items):
        """
        批量评分
        items: [{"title": "", "content": "", "url": ""}, ...]
        返回: 按总分排序的合格项目列表
        """
        results = []
        total = len(items)
        
        for i, item in enumerate(items, 1):
            print(f"  评分进度: {i}/{total} - {item['title'][:50]}...")
            
            score_result = self.score_content(
                item["title"],
                item["content"],
                item["url"]
            )
            
            print(f"    得分: {score_result['total']} {'✅' if score_result['qualified'] else '❌'}")
            
            if score_result["qualified"]:
                results.append({
                    **item,
                    "score": score_result
                })
        
        # 按总分排序
        results.sort(key=lambda x: x["score"]["total"], reverse=True)
        
        return results

    def batch_score_all(self, items):
        """
        批量评分，返回所有内容（含不合格），保留来源信息
        """
        results = []
        total = len(items)
        
        for i, item in enumerate(items, 1):
            print(f"  评分进度: {i}/{total} - {item['title'][:50]}...")
            
            score_result = self.score_content(
                item["title"],
                item["content"],
                item["url"]
            )
            
            print(f"    得分: {score_result['total']} {'✅' if score_result['qualified'] else '❌'}")
            
            results.append({
                **item,
                "score": score_result
            })
        
        return results
