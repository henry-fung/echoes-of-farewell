"""
渐进式衰减情感支持系统
基于悲伤的双过程模型和五阶段模型
"""
import re
import math
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from collections import deque
import json

# ============== 五阶段模型关键词库 ==============
STAGE_KEYWORDS = {
    "denial": {
        "zh": ["不可能", "怎么会", "不是真的", "骗我", "不可能发生", "我不相信", "一定是误会",
               "不可能", "怎麼會", "不是真的", "騙我", "我不相信", "一定是誤會"],
        "en": ["impossible", "can't be", "not real", "must be a mistake", "no way", "I don't believe"],
        "weight": 1.0
    },
    "anger": {
        "zh": ["为什么", "凭什么", "我恨", "不公平", "生气", "愤怒", "该死的", "滚", "恨你",
               "為什麼", "憑什麼", "我恨", "不公平", "生氣", "憤怒"],
        "en": ["why", "hate", "unfair", "angry", "damn", "furious", "mad at", "pissed"],
        "weight": 1.2
    },
    "bargaining": {
        "zh": ["如果能", "求求你", "我愿意", "只要", "请让", "要是", "宁愿", "求你",
               "如果能", "求求你", "我願意", "隻要", "請讓", "要是", "寧願"],
        "en": ["if only", "please", "I would", "as long as", "beg you", "wish", "I'm willing"],
        "weight": 0.9
    },
    "depression": {
        "zh": ["好想死", "活着没意思", "痛苦", "绝望", "不想活", "哭", "悲伤", "难过",
               "空虚", "孤独", "没意义", "抑郁",
               "好想死", "活著沒意思", "痛苦", "絕望", "不想活", "哭", "悲傷", "難過",
               "空虛", "孤獨", "沒意義", "抑郁"],
        "en": ["want to die", "no point", "suffering", "hopeless", "depressed", "sad", "crying",
               "empty", "lonely", "meaningless", "suicide"],
        "weight": 1.5  # 高风险阶段权重更高
    },
    "acceptance": {
        "zh": ["接受了", "会好的", "珍惜", "回忆", "谢谢", "感恩", "放下", "向前走",
               "會好的", "珍惜", "回憶", "謝謝", "感恩"],
        "en": ["accept", "will be ok", "cherish", "memory", "thank you", "grateful", "move on", "accepted"],
        "weight": 0.8
    }
}

# ============== 情感强度词典 ==============
EMOTION_INTENSITY = {
    "zh": {
        "high": ["非常", "极其", "太", "真的", "好", "特别", "无比", "极度", "崩溃", "撕心裂肺",
                 "非常", "極其", "太", "真的", "好", "特別", "無比", "極度", "崩潰"],
        "medium": ["有点", "比较", "还算", "挺", "蛮", "有些", "感覺", "比較"],
        "low": ["稍微", "略", "有点点", "一丢丢", "略微"]
    },
    "en": {
        "high": ["very", "extremely", "so", "really", "totally", "completely", "utterly", "devastated"],
        "medium": ["quite", "pretty", "fairly", "somewhat", "kind of"],
        "low": ["a bit", "slightly", "a little", "somewhat"]
    }
}

# ============== 悲伤关键词密度计算 ==============
GRIEF_KEYWORDS = {
    "zh": ["想念", "怀念", "如果", "为什么", "回不来了", "再也", "梦", "希望",
           "想念", "懷念", "如果", "為什麼", "回不來了", "再也", "夢", "希望"],
    "en": ["miss", "remember", "if only", "dream", "wish", "gone", "forever", "longing"]
}

RISK_KEYWORDS = {
    "zh": ["自杀", "想死", "结束生命", "不活了", "解脱", "跳楼", "割腕", "吃药",
           "自殺", "想死", "結束生命", "不活了", "解脫", "跳樓", "割腕"],
    "en": ["suicide", "kill myself", "end my life", "want to die", "overdose", "jump", "no reason to live"]
}

# ============== 效价 - 唤醒度关键词 (连续情绪维度) ==============
# 效价 (Valence): -1.0(极负面) 到 1.0(极正面)
# 唤醒度 (Arousal): 0.0(平静) 到 1.0(激动)
VALENCE_KEYWORDS = {
    "zh": {
        "positive": ["爱", "喜欢", "开心", "快乐", "幸福", "温暖", "感激", "希望", "美好", "珍惜",
                     "愛", "喜歡", "開心", "快樂", "幸福", "溫暖", "感激", "希望", "美好"],
        "negative": ["恨", "痛苦", "悲伤", "绝望", "孤独", "空虚", "后悔", "自责", "怨恨", "愤怒",
                     "恨", "痛苦", "悲傷", "絕望", "孤獨", "空虛", "後悔", "自責", "怨恨", "憤怒"]
    },
    "en": {
        "positive": ["love", "like", "happy", "joy", "grateful", "hope", "warm", "cherish"],
        "negative": ["hate", "pain", "suffering", "desperate", "lonely", "regret", "blame", "anger"]
    }
}

AROUSAL_KEYWORDS = {
    "zh": {
        "high": ["崩溃", "疯狂", "极度", "撕心裂肺", "大喊", "尖叫", "激动", "颤抖",
                 "崩潰", "瘋狂", "極度", "撕心裂肺", "大喊", "尖叫", "激動", "顫抖"],
        "low": ["平静", "安静", "沉默", "麻木", "无力", "疲惫", "淡然", "无所谓",
                "平靜", "安靜", "沉默", "麻木", "無力", "疲憊", "淡然", "無所謂"]
    },
    "en": {
        "high": ["collapse", "crazy", "extreme", "screaming", "shaking", "panic"],
        "low": ["calm", "quiet", "silent", "numb", "tired", "indifferent"]
    }
}

# ============== 用户行为分析关键词 ==============
BEHAVIOR_KEYWORDS = {
    # 依赖行为
    "dependency": {
        "zh": ["你在吗", "陪我", "不要离开", "只有你了", "别走", "一直都在吗",
               "你在嗎", "陪我", "不要離開", "只有你了", "別走", "一直都在嗎"],
        "en": ["are you there", "stay with me", "don't leave", "only you", "please stay"]
    },
    # 回忆行为
    "remembrance": {
        "zh": ["记得", "以前", "那时候", "曾经", "过去", "回忆", "想起", "梦到",
               "記得", "以前", "那時候", "曾經", "過去", "回憶", "想起", "夢到"],
        "en": ["remember", "used to", "back then", "once", "memory", "recall", "dreamed"]
    },
    # 未来导向
    "future_oriented": {
        "zh": ["以后", "将来", "明天", "接下来", "重新开始", "继续生活", "向前看",
               "以後", "將來", "明天", "接下來", "重新開始", "繼續生活", "向前看"],
        "en": ["future", "tomorrow", "next", "start over", "move on", "look forward"]
    },
    # 自我表露
    "self_disclosure": {
        "zh": ["我觉得", "我感到", "我认为", "我的", "自己", "内心", "心里",
               "我覺得", "我感到", "我認為", "我的", "自己", "內心", "心裡"],
        "en": ["I feel", "I think", "my", "myself", "inner", "heart", "inside"]
    }
}


@dataclass
class EmotionState:
    """用户情感状态 - 支持分阶段衰减曲线"""
    profile_id: int
    user_id: int
    
    # 心情指数 (0-100, 初始值)
    mood_index: float = 80.0
    
    # 基础衰减率 (根据阶段动态调整)
    base_decay_rate: float = 0.03
    
    # 当前实际衰减率 (动态计算)
    decay_rate: float = 0.03
    
    # 阶段起始时间 (用于计算当前处于哪个衰减阶段)
    phase_start_time: datetime = field(default_factory=datetime.utcnow)
    
    # 当前阶段 (acute/integrated/acceptance)
    recovery_phase: str = "acute"  # acute:急性期, integrated:整合期, acceptance:接受期
    
    # 五阶段概率分布
    stage_probabilities: Dict[str, float] = field(default_factory=lambda: {
        "denial": 0.2,
        "anger": 0.2,
        "bargaining": 0.2,
        "depression": 0.2,
        "acceptance": 0.2
    })
    
    # 主导阶段
    dominant_stage: str = "denial"
    
    # 上一个主导阶段 (用于检测阶段转移)
    previous_stage: str = "denial"
    
    # 阶段停留计数
    stage_dwell_count: int = 0
    
    # 交互历史 (用于计算熵和稳定度)
    interaction_history: deque = field(default_factory=lambda: deque(maxlen=50))
    
    # 最后交互时间
    last_interaction: datetime = field(default_factory=datetime.utcnow)
    
    # 情感稳定度 (基于方差计算)
    stability_score: float = 0.5
    
    # 风险等级 (0-1)
    risk_level: float = 0.0
    
    # 连续负面交互计数
    negative_streak: int = 0
    
    # 强烈负向事件计数 (用于临时降低衰减率)
    strong_negative_events: int = 0
    
    # 总交互次数
    total_interactions: int = 0
    
    # 记忆权重 (亲密记忆 vs 支持性内容)
    memory_intimacy_weight: float = 1.0  # 1.0=完全亲密, 0.0=完全支持性
    
    # 下次主动提醒时间
    next_proactive_time: Optional[datetime] = None
    
    # 是否允许主动发起
    allow_proactive: bool = True

    # ========== 新增：连续情绪维度 ==========
    # 效价 (Valence): -1.0(极负面) 到 1.0(极正面)
    valence: float = 0.0

    # 唤醒度 (Arousal): 0.0(平静) 到 1.0(激动)
    arousal: float = 0.5

    # ========== 新增：用户行为指标 ==========
    # 行为关键词计数
    behavior_counts: Dict[str, int] = field(default_factory=lambda: {
        "dependency": 0,
        "remembrance": 0,
        "future_oriented": 0,
        "self_disclosure": 0
    })

    # 提取的关键词列表
    extracted_keywords: List[str] = field(default_factory=list)


class EmotionEngine:
    """情感计算引擎"""
    
    # 阶段名称映射
    STAGE_NAMES = {
        "denial": {"zh": "否认", "en": "Denial"},
        "anger": {"zh": "愤怒", "en": "Anger"},
        "bargaining": {"zh": "讨价还价", "en": "Bargaining"},
        "depression": {"zh": "抑郁", "en": "Depression"},
        "acceptance": {"zh": "接受", "en": "Acceptance"}
    }
    
    def __init__(self):
        # 内存中存储用户状态 (生产环境应使用Redis)
        self.user_states: Dict[str, EmotionState] = {}
    
    def _get_state_key(self, user_id: int, profile_id: int) -> str:
        return f"{user_id}_{profile_id}"
    
    def get_or_create_state(self, user_id: int, profile_id: int) -> EmotionState:
        """获取或创建用户情感状态"""
        key = self._get_state_key(user_id, profile_id)
        if key not in self.user_states:
            self.user_states[key] = EmotionState(
                profile_id=profile_id,
                user_id=user_id,
                mood_index=80.0,  # 初始高亲密度
                decay_rate=0.03,  # 初始衰减率3%
            )
        return self.user_states[key]
    
    def analyze_text(self, text: str, language: str = "zh-CN") -> Dict:
        """分析用户文本的情感特征"""
        text_lower = text.lower()
        lang = "zh" if language.startswith("zh") else "en"
        
        # 1. 五阶段检测
        stage_scores = {}
        for stage, data in STAGE_KEYWORDS.items():
            keywords = data["zh"] if lang == "zh" else data["en"]
            score = sum(2 if kw in text_lower else 0 for kw in keywords)
            # 考虑情感强度词
            intensity = self._detect_intensity(text, lang)
            stage_scores[stage] = score * data["weight"] * intensity
        
        # 归一化阶段分数
        total = sum(stage_scores.values()) or 1
        stage_probs = {k: v/total for k, v in stage_scores.items()}
        dominant_stage = max(stage_probs, key=stage_probs.get)
        
        # 2. 悲伤关键词密度
        grief_words = GRIEF_KEYWORDS[lang]
        grief_count = sum(1 for w in grief_words if w in text_lower)
        grief_density = min(grief_count / (len(text) / 10 + 1), 1.0)  # 每10字密度
        
        # 3. 风险检测
        risk_words = RISK_KEYWORDS[lang]
        risk_count = sum(1 for w in risk_words if w in text_lower)
        risk_level = min(risk_count * 0.3, 1.0)  # 每个风险词+0.3
        
        # 4. 情感强度 (基于大写字母、感叹号、重复)
        intensity = self._calculate_emotional_intensity(text)
        
        # 5. 文本长度 (反映表达欲)
        text_length = len(text)

        # 6. 新增：连续情绪维度 (效价/唤醒度)
        valence, arousal = self._calculate_valence_arousal(text, lang)

        # 7. 新增：行为关键词分析
        behavior_counts = self._analyze_behavior_keywords(text, lang)

        # 8. 新增：关键词提取
        extracted_keywords = self._extract_keywords(text, lang)

        return {
            "stage_probabilities": stage_probs,
            "dominant_stage": dominant_stage,
            "grief_density": grief_density,
            "risk_level": risk_level,
            "intensity": intensity,
            "text_length": text_length,
            "is_negative": dominant_stage in ["denial", "anger", "depression"] or grief_density > 0.3,
            # 新增字段
            "valence": valence,
            "arousal": arousal,
            "behavior_counts": behavior_counts,
            "extracted_keywords": extracted_keywords
        }

    def _calculate_valence_arousal(self, text: str, lang: str) -> Tuple[float, float]:
        """
        计算连续情绪维度：效价 (Valence) 和唤醒度 (Arousal)
        效价：-1.0(极负面) 到 1.0(极正面)
        唤醒度：0.0(平静) 到 1.0(激动)
        """
        text_lower = text.lower()

        # 计算效价
        positive_count = sum(1 for kw in VALENCE_KEYWORDS[lang]["positive"] if kw in text_lower)
        negative_count = sum(1 for kw in VALENCE_KEYWORDS[lang]["negative"] if kw in text_lower)

        total_valence = positive_count + negative_count
        if total_valence == 0:
            valence = 0.0  # 中性
        else:
            # 归一化到 -1 到 1
            valence = (positive_count - negative_count) / total_valence

        # 计算唤醒度
        high_arousal = sum(1 for kw in AROUSAL_KEYWORDS[lang]["high"] if kw in text_lower)
        low_arousal = sum(1 for kw in AROUSAL_KEYWORDS[lang]["low"] if kw in text_lower)

        total_arousal = high_arousal + low_arousal
        if total_arousal == 0:
            arousal = 0.5  # 中等唤醒度
        else:
            # 归一化到 0 到 1
            arousal = high_arousal / total_arousal

        # 考虑标点符号对唤醒度的影响
        exclaim_count = text.count('!') + text.count('！')
        arousal = min(1.0, arousal + exclaim_count * 0.1)

        return valence, arousal

    def _analyze_behavior_keywords(self, text: str, lang: str) -> Dict[str, int]:
        """
        分析用户行为关键词
        返回：{dependency: count, remembrance: count, future_oriented: count, self_disclosure: count}
        """
        text_lower = text.lower()
        counts = {}

        for behavior_type, data in BEHAVIOR_KEYWORDS.items():
            keywords = data[lang]
            counts[behavior_type] = sum(1 for kw in keywords if kw in text_lower)

        return counts

    def _extract_keywords(self, text: str, lang: str, max_keywords: int = 20) -> List[str]:
        """
        提取文本中的关键词（五阶段、情绪、行为相关）
        返回提取到的关键词列表
        """
        text_lower = text.lower()
        keywords = []

        # 1. 提取五阶段关键词
        for stage, data in STAGE_KEYWORDS.items():
            for kw in data[lang]:
                if kw in text_lower and kw not in keywords:
                    keywords.append(kw)

        # 2. 提取悲伤关键词
        for kw in GRIEF_KEYWORDS[lang]:
            if kw in text_lower and kw not in keywords:
                keywords.append(kw)

        # 3. 提取风险关键词
        for kw in RISK_KEYWORDS[lang]:
            if kw in text_lower and kw not in keywords:
                keywords.append(kw)

        # 4. 提取情绪关键词
        for kw in VALENCE_KEYWORDS[lang]["positive"]:
            if kw in text_lower and kw not in keywords:
                keywords.append(f"[+]{kw}")
        for kw in VALENCE_KEYWORDS[lang]["negative"]:
            if kw in text_lower and kw not in keywords:
                keywords.append(f"[-]{kw}")

        # 5. 提取行为关键词
        for behavior_type, data in BEHAVIOR_KEYWORDS.items():
            for kw in data[lang]:
                if kw in text_lower and kw not in keywords:
                    keywords.append(f"[{behavior_type}]{kw}")

        return keywords[:max_keywords]
    
    def _detect_intensity(self, text: str, lang: str) -> float:
        """检测情感强度词"""
        text_lower = text.lower()
        intensity_words = EMOTION_INTENSITY[lang]
        
        for word in intensity_words["high"]:
            if word in text_lower:
                return 1.5
        for word in intensity_words["medium"]:
            if word in text_lower:
                return 1.2
        for word in intensity_words["low"]:
            if word in text_lower:
                return 0.8
        return 1.0
    
    def _calculate_emotional_intensity(self, text: str) -> float:
        """计算情感强度 (基于标点、重复等)"""
        intensity = 1.0
        
        # 感叹号数量
        exclaim_count = text.count('!') + text.count('！')
        intensity += exclaim_count * 0.1
        
        # 问号数量 (困惑/质疑)
        question_count = text.count('?') + text.count('？')
        intensity += question_count * 0.05
        
        # 重复字符 (如"啊啊啊")
        repeats = len(re.findall(r'(.)\1{2,}', text))
        intensity += repeats * 0.2
        
        # 大写字母比例 (英文)
        if any(c.isalpha() for c in text):
            upper_ratio = sum(1 for c in text if c.isupper()) / len(text)
            intensity += upper_ratio * 0.5
        
        return min(intensity, 3.0)
    
    def calculate_phase_decay_rate(self, state: EmotionState) -> float:
        """
        分阶段衰减曲线：30 天周期，根据时间自动切换阶段
        - 急性期 (1-10 天): 低衰减 0.02, 高支持度
        - 整合期 (11-20 天): 中线性衰减 0.04
        - 接受期 (21-30 天): 较高衰减 0.06, 逐步独立
        """
        now = datetime.utcnow()
        days_since_start = (now - state.phase_start_time).total_seconds() / 86400

        # 基于时间强制切换阶段 (严格 30 天周期)
        if days_since_start <= 10:
            # 急性期 (1-10 天)
            state.recovery_phase = "acute"
            base_rate = 0.02
        elif days_since_start <= 20:
            # 整合期 (11-20 天)
            state.recovery_phase = "integrated"
            base_rate = 0.04
        else:
            # 接受期 (21-30 天)
            state.recovery_phase = "acceptance"
            base_rate = 0.06

        # 强烈负向事件后临时降低衰减率 (更慢淡出)
        if state.strong_negative_events > 0:
            # 每次强烈负向事件降低衰减率 20%, 最多降低 60%
            reduction = min(state.strong_negative_events * 0.2, 0.6)
            base_rate *= (1 - reduction)
            state.strong_negative_events = max(0, state.strong_negative_events - 0.5)  # 逐渐恢复

        return max(base_rate, 0.01)  # 最低 1% 衰减

    def detect_phase_transition(self, state: EmotionState, analysis: Dict) -> Optional[str]:
        """
        检测阶段转移条件
        急性悲伤(acute) → 整合(integrated) → 接受(acceptance)
        """
        transitions = []
        
        # 检测主导阶段变化
        if state.dominant_stage != state.previous_stage:
            state.stage_dwell_count = 0
            state.previous_stage = state.dominant_stage
        else:
            state.stage_dwell_count += 1
        
        # 急性期 → 整合期条件
        if state.recovery_phase == "acute":
            conditions = []
            if state.stage_probabilities.get("acceptance", 0) > 0.25:
                conditions.append("接受概率>25%")
            if state.stability_score > 0.5:
                conditions.append("情感稳定")
            if state.negative_streak == 0 and state.stage_dwell_count > 5:
                conditions.append("连续稳定交互")
            
            if len(conditions) >= 2:
                transitions.append(f"可进入整合期: {', '.join(conditions)}")
        
        # 整合期 → 接受期条件
        elif state.recovery_phase == "integrated":
            conditions = []
            if state.stage_probabilities.get("acceptance", 0) > 0.45:
                conditions.append("接受概率>45%")
            if state.mood_index < 40:  # 心情指数较低, 说明衰减起作用
                conditions.append("心情指数适应")
            if state.total_interactions > 20:
                conditions.append("足够交互次数")
            
            if len(conditions) >= 2:
                transitions.append(f"可进入接受期: {', '.join(conditions)}")
        
        return transitions[0] if transitions else None
    
    def update_memory_weight(self, state: EmotionState) -> float:
        """
        动态调整记忆权重: 随心情指数降低, 逐步减少亲密记忆, 增加支持性内容
        M_t 高(80-100): weight=1.0 (大量亲密回忆)
        M_t 中(40-80): weight=0.5-1.0 (过渡)
        M_t 低(10-40): weight=0.0-0.5 (更多支持性、面向未来的内容)
        """
        M = state.mood_index / 100.0
        
        # 指数衰减曲线
        weight = math.exp(-1.5 * (1 - M))
        
        # 根据阶段微调
        if state.recovery_phase == "acceptance":
            weight *= 0.7  # 接受期进一步降低亲密记忆
        
        state.memory_intimacy_weight = max(0.1, min(1.0, weight))
        return state.memory_intimacy_weight
    
    def schedule_next_proactive(self, state: EmotionState) -> Optional[datetime]:
        """
        基于 F_t (频率因子) 计算下次主动发起时间
        F_t 高: 主动间隔短 (更频繁)
        F_t 低: 主动间隔长 (逐渐淡出)
        """
        M = state.mood_index / 100.0  # 频率因子
        
        # 基础间隔: 12-72小时
        base_interval_hours = 72 - (M * 60)  # M=1时12小时, M=0时72小时
        
        # 根据阶段调整
        if state.recovery_phase == "acute":
            base_interval_hours *= 0.6  # 急性期更频繁
        elif state.recovery_phase == "acceptance":
            base_interval_hours *= 1.5  # 接受期更稀疏
        
        # 风险情况优先
        if state.risk_level > 0.3:
            base_interval_hours = min(base_interval_hours, 6)  # 最多6小时
        
        next_time = datetime.utcnow() + timedelta(hours=base_interval_hours)
        state.next_proactive_time = next_time
        return next_time
    
    def should_proactive_initiate(self, state: EmotionState) -> Tuple[bool, str]:
        """
        判断是否应主动发起对话
        返回: (是否发起, 原因)
        """
        if not state.allow_proactive:
            return False, "主动发起已禁用"
        
        if state.next_proactive_time is None:
            self.schedule_next_proactive(state)
            return False, "首次调度"
        
        now = datetime.utcnow()
        if now < state.next_proactive_time:
            remaining = (state.next_proactive_time - now).total_seconds() / 3600
            return False, f"距离下次主动发起还有{remaining:.1f}小时"
        
        # 检查频率因子
        F = state.mood_index / 100.0
        if F < 0.2 and state.risk_level < 0.2:
            return False, "频率因子过低, 已进入淡出阶段"
        
        # 风险情况必须发起
        if state.risk_level > 0.4:
            return True, "高风险警报, 必须主动关心"
        
        # 连续负面需要关心
        if state.negative_streak >= 2:
            return True, "用户连续负面, 主动关心"
        
        return True, "正常主动发起"
    
    def update_mood_index(self, state: EmotionState, user_input: str, analysis: Dict) -> float:
        """
        更新心情指数: M_t = decay(M_{t-1}, b_t) + gain(u_t)
        包含分阶段衰减曲线和强烈事件处理
        """
        now = datetime.utcnow()
        time_diff = (now - state.last_interaction).total_seconds() / 3600  # 小时
        
        # 1. 动态计算衰减率 (分阶段曲线)
        state.decay_rate = self.calculate_phase_decay_rate(state)
        
        # 2. 时间衰减
        decay_factor = math.exp(-state.decay_rate * time_diff / 24)
        mood_after_decay = state.mood_index * decay_factor
        
        # 3. 计算用户输入带来的增益/减益
        gain = 0.0
        is_strong_negative = False
        
        # 负面情感增加 mood (需要更多支持)
        if analysis["is_negative"]:
            gain += analysis["intensity"] * 10
            state.negative_streak += 1
            
            # 检测强烈负向事件
            if analysis["intensity"] > 2.0 or analysis["grief_density"] > 0.5:
                state.strong_negative_events += 1
                is_strong_negative = True
        else:
            gain -= 5  # 正面情感逐渐减少mood
            state.negative_streak = max(0, state.negative_streak - 1)
        
        # 风险词汇大幅增加
        if analysis["risk_level"] > 0.3:
            gain += 30
            state.risk_level = analysis["risk_level"]
            state.strong_negative_events += 2  # 风险事件权重更高
        
        # 悲伤密度影响
        gain += analysis["grief_density"] * 15
        
        # 4. 应用安全阈值：强烈负向事件暂停衰减
        if state.negative_streak >= 3 or analysis["risk_level"] > 0.5 or is_strong_negative:
            new_mood = min(state.mood_index + gain, 100)
        else:
            new_mood = min(mood_after_decay + gain, 100)
        
        new_mood = max(new_mood, 10)
        state.mood_index = new_mood
        state.last_interaction = now
        state.total_interactions += 1

        # 5. 更新连续情绪维度（效价/唤醒度）
        state.valence = analysis.get("valence", 0.0)
        state.arousal = analysis.get("arousal", 0.5)

        # 6. 更新行为关键词计数
        for behavior_type, count in analysis.get("behavior_counts", {}).items():
            state.behavior_counts[behavior_type] = state.behavior_counts.get(behavior_type, 0) + count

        # 7. 更新提取的关键词
        keywords = analysis.get("extracted_keywords", [])
        state.extracted_keywords = keywords[:20]  # 限制存储数量

        # 8. 更新阶段概率和稳定度
        self._update_stage_probabilities(state, analysis)
        self._update_stability(state, analysis)

        # 9. 检测阶段转移
        transition = self.detect_phase_transition(state, analysis)

        # 10. 更新记忆权重
        self.update_memory_weight(state)

        # 11. 调度下次主动发起
        self.schedule_next_proactive(state)

        # 12. 记录交互（包含新的情绪维度）
        state.interaction_history.append({
            "timestamp": now.isoformat(),
            "mood": new_mood,
            "stage": analysis["dominant_stage"],
            "intensity": analysis["intensity"],
            "risk": analysis["risk_level"],
            "valence": analysis.get("valence", 0.0),
            "arousal": analysis.get("arousal", 0.5),
            "decay_rate": state.decay_rate,
            "phase": state.recovery_phase,
            "memory_weight": state.memory_intimacy_weight,
            "transition": transition,
            "keywords": keywords[:10]  # 存储前 10 个关键词
        })

        return new_mood
    
    def _update_stage_probabilities(self, state: EmotionState, analysis: Dict):
        """更新五阶段概率分布"""
        # 使用指数移动平均更新
        alpha = 0.3  # 平滑因子
        for stage, prob in analysis["stage_probabilities"].items():
            state.stage_probabilities[stage] = (
                (1 - alpha) * state.stage_probabilities[stage] + alpha * prob
            )
        
        # 更新主导阶段
        state.dominant_stage = max(
            state.stage_probabilities, 
            key=state.stage_probabilities.get
        )
    
    def _update_stability(self, state: EmotionState, analysis: Dict):
        """计算情感稳定度 (基于历史方差)"""
        if len(state.interaction_history) < 3:
            return

        # 计算最近几次交互的情绪强度方差
        recent_intensities = [
            h["intensity"] for h in list(state.interaction_history)[-5:]
        ]
        mean_intensity = sum(recent_intensities) / len(recent_intensities)
        variance = sum((x - mean_intensity) ** 2 for x in recent_intensities) / len(recent_intensities)

        # 计算效价方差
        recent_valences = [h.get("valence", 0.0) for h in list(state.interaction_history)[-5:]]
        mean_valence = sum(recent_valences) / len(recent_valences)
        valence_variance = sum((x - mean_valence) ** 2 for x in recent_valences) / len(recent_valences)

        # 计算唤醒度方差
        recent_arousals = [h.get("arousal", 0.5) for h in list(state.interaction_history)[-5:]]
        mean_arousal = sum(recent_arousals) / len(recent_arousals)
        arousal_variance = sum((x - mean_arousal) ** 2 for x in recent_arousals) / len(recent_arousals)

        # 综合稳定度：综合考虑强度、效价、唤醒度的方差
        # 总方差 = 加权和 (强度方差占 40%, 效价方差占 30%, 唤醒度方差占 30%)
        total_variance = 0.4 * variance + 0.3 * valence_variance + 0.3 * arousal_variance

        # 方差越大，稳定度越低
        state.stability_score = max(0, 1 - total_variance)
    
    def calculate_strategy_params(self, state: EmotionState) -> Dict:
        """
        策略映射: 将 M_t 转换为机器人行为参数 (增强版)
        包含记忆权重、阶段信息、主动发起时间等
        """
        M = state.mood_index / 100.0  # 归一化到0-1
        
        # 基础参数
        L_base = 150  # 基础字数
        I_base = 1.0  # 基础亲密度
        F_base = 1.0  # 基础频率
        
        # 单调递减函数 (指数衰减)
        f_L = math.exp(-2 * (1 - M))  # 回复长度衰减
        f_I = 0.3 + 0.7 * M  # 亲密度衰减 (最小保持0.3)
        f_F = M  # 频率衰减
        
        # 阶段调整 (五阶段模型)
        stage_multiplier = {
            "denial": 1.2,      # 否认期需要更多解释
            "anger": 1.0,       # 愤怒期正常回复
            "bargaining": 1.1,  # 讨价还价期需要引导
            "depression": 1.3,  # 抑郁期需要更多关怀
            "acceptance": 0.8   # 接受期逐渐减少
        }.get(state.dominant_stage, 1.0)
        
        # 恢复阶段调整 (双过程模型)
        phase_multiplier = {
            "acute": 1.2,       # 急性期更多支持
            "integrated": 1.0,  # 整合期正常
            "acceptance": 0.7   # 接受期减少
        }.get(state.recovery_phase, 1.0)
        
        # 风险干预：高风险时强制增加参数
        if state.risk_level > 0.3:
            L_base = 200
            f_L = 1.5
            f_I = 1.0
        
        # 计算下次主动发起时间
        next_proactive = state.next_proactive_time
        if next_proactive:
            hours_until = (next_proactive - datetime.utcnow()).total_seconds() / 3600
        else:
            hours_until = None
        
        params = {
            # 基础策略参数
            "max_length": int(L_base * f_L * stage_multiplier * phase_multiplier),
            "intimacy_level": min(I_base * f_I, 1.0),
            "frequency_factor": F_base * f_F,
            
            # 情感状态
            "mood_index": state.mood_index,
            "decay_rate": state.decay_rate,
            "dominant_stage": state.dominant_stage,
            "stage_name": self.STAGE_NAMES[state.dominant_stage],
            "recovery_phase": state.recovery_phase,
            "phase_name": self._get_phase_name(state.recovery_phase),
            "stability": state.stability_score,
            "risk_level": state.risk_level,
            
            # 记忆权重 (新增)
            "memory_intimacy_weight": state.memory_intimacy_weight,
            "memory_support_weight": 1.0 - state.memory_intimacy_weight,
            
            # 主动发起 (新增)
            "should_proactive": F_base * f_F > 0.6,
            "use_intimate_tone": I_base * f_I > 0.6,
            "next_proactive_hours": hours_until,
            "allow_proactive": state.allow_proactive,
            
            # 阶段统计
            "total_interactions": state.total_interactions,
            "stage_dwell_count": state.stage_dwell_count,
            "strong_negative_events": state.strong_negative_events,
        }
        
        return params
    
    def _get_phase_name(self, phase: str) -> Dict[str, str]:
        """获取恢复阶段名称"""
        names = {
            "acute": {"zh": "急性悲伤期", "en": "Acute Grief"},
            "integrated": {"zh": "整合调整期", "en": "Integrated Phase"},
            "acceptance": {"zh": "接受适应期", "en": "Acceptance Phase"}
        }
        return names.get(phase, {"zh": "未知", "en": "Unknown"})
    
    def generate_emotion_prompt(self, params: Dict, profile: Dict) -> str:
        """生成情感引导提示词 (增强版，包含记忆权重和恢复阶段)"""
        stage = params["dominant_stage"]
        phase = params["recovery_phase"]
        mood = params["mood_index"]
        intimacy = params["intimacy_level"]
        memory_weight = params.get("memory_intimacy_weight", 0.5)
        
        lang = "zh" if profile.get("language", "zh-CN").startswith("zh") else "en"
        
        # 五阶段引导
        stage_guidance = {
            "denial": {
                "zh": "用户处于否认阶段，TA可能难以接受现实。请温和地陪伴，不要强行打破否认，而是提供安全感。",
                "en": "User is in denial. Be gentle, provide safety without forcing reality."
            },
            "anger": {
                "zh": "用户处于愤怒阶段，TA可能感到不公和怨恨。请接纳TA的情绪，不要评判，让TA知道愤怒是正常的。",
                "en": "User is angry. Accept their emotions without judgment. Anger is normal."
            },
            "bargaining": {
                "zh": "用户处于讨价还价阶段，TA可能在反复思考'如果'。请温和地引导TA接受无法改变的事实，同时肯定TA的爱。",
                "en": "User is bargaining. Gently guide acceptance while affirming their love."
            },
            "depression": {
                "zh": "用户处于抑郁阶段，TA可能感到深深悲伤。请给予更多关怀和陪伴，如果检测到风险请建议专业帮助。",
                "en": "User is depressed. Provide extra care. Suggest professional help if needed."
            },
            "acceptance": {
                "zh": "用户正在走向接受，TA开始面对现实。请肯定TA的勇气，支持TA重建生活，同时珍惜回忆。",
                "en": "User is moving toward acceptance. Affirm their courage, support rebuilding."
            }
        }
        
        # 恢复阶段引导
        phase_guidance = {
            "acute": {
                "zh": "【急性悲伤期】用户处于早期悲伤阶段，需要高强度支持。请保持高亲密度，多分享回忆，提供情感依托。",
                "en": "[Acute Phase] Early grief stage. Maintain high intimacy, share memories, provide emotional support."
            },
            "integrated": {
                "zh": "【整合调整期】用户正在逐步调整，开始接受现实。请适度引导，帮助TA整合丧失经验，重建生活意义。",
                "en": "[Integrated Phase] User is adjusting. Guide moderately to integrate loss and rebuild meaning."
            },
            "acceptance": {
                "zh": "【接受适应期】用户已基本接受，正在适应新生活。请减少亲密回忆引用，更多支持面向未来的独立生活。",
                "en": "[Acceptance Phase] User has accepted. Reduce intimate memories, support future-oriented independence."
            }
        }
        
        # 记忆权重指导 (新增)
        if memory_weight > 0.7:
            memory_guide_zh = f"记忆权重高({memory_weight:.2f})：大量使用亲密回忆、共同经历，用'记得那时候...'的方式唤起温暖记忆。"
            memory_guide_en = f"High memory weight({memory_weight:.2f}): Use many intimate memories and shared experiences."
        elif memory_weight > 0.3:
            memory_guide_zh = f"记忆权重中({memory_weight:.2f})：适度提及回忆，同时加入支持性内容，平衡怀旧与向前看。"
            memory_guide_en = f"Medium memory weight({memory_weight:.2f}): Balance memories with supportive content."
        else:
            memory_guide_zh = f"记忆权重低({memory_weight:.2f})：减少回忆性内容，更多提供支持性、面向未来的建议，鼓励独立面对生活。"
            memory_guide_en = f"Low memory weight({memory_weight:.2f}): Reduce memories, provide supportive, future-oriented advice."
        
        memory_guide = memory_guide_zh if lang == "zh" else memory_guide_en
        
        # 亲密度指导
        intimacy_guidance = {
            "high": {
                "zh": "使用亲密的称呼（如孩子、宝贝），多用'我'和'你'，分享温暖回忆。",
                "en": "Use intimate terms, share warm memories, use 'I' and 'you' frequently."
            },
            "medium": {
                "zh": "保持温和的关心，适当分享，同时引导用户向前看。",
                "en": "Maintain gentle care, guide user to look forward."
            },
            "low": {
                "zh": "减少亲密称呼，更多提供支持性、面向未来的内容，鼓励独立。",
                "en": "Reduce intimacy, provide supportive, future-oriented content."
            }
        }
        
        # 确定亲密度等级
        if intimacy > 0.7:
            intim_level = "high"
        elif intimacy > 0.4:
            intim_level = "medium"
        else:
            intim_level = "low"
        
        stage_guide = stage_guidance.get(stage, stage_guidance["denial"])[lang]
        phase_guide = phase_guidance.get(phase, phase_guidance["acute"])[lang]
        intim_guide = intimacy_guidance[intim_level]["zh" if lang == "zh" else "en"]
        
        return f"""
【五阶段状态】{params['stage_name']['zh' if lang == 'zh' else 'en']}
{stage_guide}

{phase_guide}

【记忆权重指导】
{memory_guide}

【亲密度指导】({intimacy:.2f})
{intim_guide}

【回复要求】
- 最大字数：{params['max_length']}字
- 心情指数：{mood:.1f}/100 (衰减率: {params.get('decay_rate', 0.03):.3f})
- 风险等级：{'高风险，建议专业干预' if params['risk_level'] > 0.3 else '正常'}
- 情感稳定度：{params['stability']:.2f}
"""
    
    def check_safety_alert(self, state: EmotionState) -> Optional[str]:
        """安全检查，返回警告信息"""
        alerts = []
        
        # 高风险连续出现
        if state.risk_level > 0.5:
            alerts.append("高风险：检测到自杀倾向词汇")
        
        # 抑郁阶段持续
        if (state.dominant_stage == "depression" and 
            state.stage_probabilities["depression"] > 0.6 and
            state.total_interactions > 10):
            alerts.append("持续抑郁：建议专业心理支持")
        
        # 情绪剧烈波动 (稳定度低)
        if state.stability_score < 0.3 and state.total_interactions > 5:
            alerts.append("情绪不稳定：需要更多关注")
        
        # 负面连续过长
        if state.negative_streak >= 5:
            alerts.append("连续负面情绪：建议调整策略")
        
        if alerts:
            return " | ".join(alerts)
        return None
    
    def get_interaction_entropy(self, state: EmotionState) -> float:
        """计算交互熵 (衡量用户依赖度/情绪多样性)"""
        if len(state.interaction_history) < 5:
            return 0.5

        # 计算阶段分布的熵
        stage_counts = {"denial": 0, "anger": 0, "bargaining": 0, "depression": 0, "acceptance": 0}
        for h in state.interaction_history:
            stage = h.get("stage", "denial")
            stage_counts[stage] = stage_counts.get(stage, 0) + 1

        total = sum(stage_counts.values())
        entropy = 0
        for count in stage_counts.values():
            if count > 0:
                p = count / total
                entropy -= p * math.log2(p)

        # 最大熵是 log2(5) ≈ 2.32
        normalized_entropy = entropy / 2.32

        # 返回依赖度 (1 - 熵，熵越低依赖越集中)
        return 1 - normalized_entropy

    def analyze_user_trend(self, state: EmotionState) -> Dict:
        """
        用户行为趋势分析
        返回：{
            - 情绪变化趋势 (效价/唤醒度/心情的时间序列趋势)
            - 行为模式 (依赖/回忆/未来导向的比例)
            - 五阶段进展趋势
            - 交互熵变化
            - 风险趋势
        }
        """
        if len(state.interaction_history) < 5:
            return {
                "trend": "insufficient_data",
                "message": "需要至少 5 次交互才能进行趋势分析"
            }

        history = list(state.interaction_history)

        # 1. 计算情绪变化趋势 (线性回归斜率)
        recent_moods = [h["mood"] for h in history[-10:]]
        mood_trend = self._calculate_trend_slope(recent_moods)

        recent_valences = [h.get("valence", 0.0) for h in history[-10:]]
        valence_trend = self._calculate_trend_slope(recent_valences)

        recent_arousals = [h.get("arousal", 0.5) for h in history[-10:]]
        arousal_trend = self._calculate_trend_slope(recent_arousals)

        # 2. 行为模式分析
        total_dependency = sum(h.get("behavior_counts", {}).get("dependency", 0) for h in history)
        total_remembrance = sum(h.get("behavior_counts", {}).get("remembrance", 0) for h in history)
        total_future = sum(h.get("behavior_counts", {}).get("future_oriented", 0) for h in history)
        total_disclosure = sum(h.get("behavior_counts", {}).get("self_disclosure", 0) for h in history)

        total_behavior = total_dependency + total_remembrance + total_future + total_disclosure
        if total_behavior > 0:
            behavior_pattern = {
                "dependency_ratio": total_dependency / total_behavior,
                "remembrance_ratio": total_remembrance / total_behavior,
                "future_oriented_ratio": total_future / total_behavior,
                "self_disclosure_ratio": total_disclosure / total_behavior
            }
        else:
            behavior_pattern = {
                "dependency_ratio": 0,
                "remembrance_ratio": 0,
                "future_oriented_ratio": 0,
                "self_disclosure_ratio": 0
            }

        # 3. 五阶段进展趋势
        stage_progression = {
            "denial": sum(1 for h in history if h.get("stage") == "denial"),
            "anger": sum(1 for h in history if h.get("stage") == "anger"),
            "bargaining": sum(1 for h in history if h.get("stage") == "bargaining"),
            "depression": sum(1 for h in history if h.get("stage") == "depression"),
            "acceptance": sum(1 for h in history if h.get("stage") == "acceptance")
        }

        # 计算主导趋势
        if len(history) >= 2:
            first_half = history[:len(history)//2]
            second_half = history[len(history)//2:]

            first_acceptance = sum(1 for h in first_half if h.get("stage") == "acceptance") / len(first_half)
            second_acceptance = sum(1 for h in second_half if h.get("stage") == "acceptance") / len(second_half)

            first_depression = sum(1 for h in first_half if h.get("stage") == "depression") / len(first_half)
            second_depression = sum(1 for h in second_half if h.get("stage") == "depression") / len(second_half)

            stage_trend = "improving" if second_acceptance > first_acceptance and second_depression < first_depression else \
                         "declining" if second_depression > first_depression else "stable"
        else:
            stage_trend = "insufficient_data"

        # 4. 风险趋势
        recent_risks = [h.get("risk", 0.0) for h in history[-5:]]
        risk_trend = "increasing" if len(recent_risks) >= 2 and recent_risks[-1] > recent_risks[0] * 1.5 else \
                    "decreasing" if len(recent_risks) >= 2 and recent_risks[-1] < recent_risks[0] * 0.5 else "stable"

        # 5. 综合评估
        overall_assessment = "stable"
        if mood_trend > 2 and valence_trend > 0.1:
            overall_assessment = "improving"
        elif mood_trend < -2 and valence_trend < -0.1:
            overall_assessment = "declining"
        elif abs(mood_trend) > 5:
            overall_assessment = "fluctuating"

        return {
            "trend": overall_assessment,
            "mood_trend": round(mood_trend, 4),
            "valence_trend": round(valence_trend, 4),
            "arousal_trend": round(arousal_trend, 4),
            "behavior_pattern": behavior_pattern,
            "stage_progression": stage_progression,
            "stage_trend": stage_trend,
            "risk_trend": risk_trend,
            "total_interactions_analyzed": len(history)
        }

    def _calculate_trend_slope(self, values: List[float]) -> float:
        """
        计算时间序列的趋势斜率 (简单线性回归)
        正值表示上升趋势，负值表示下降趋势
        """
        n = len(values)
        if n < 2:
            return 0.0

        # 简单线性回归斜率计算
        x_mean = (n - 1) / 2
        y_mean = sum(values) / n

        numerator = sum((i - x_mean) * (values[i] - y_mean) for i in range(n))
        denominator = sum((i - x_mean) ** 2 for i in range(n))

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def analyze_monthly_trend(self, state: EmotionState, monthly_stats: List[Dict]) -> Dict:
        """
        按月情绪趋势分析
        Args:
            state: 用户情感状态
            monthly_stats: 月度统计数据（来自 get_monthly_emotion_stats）
        Returns:
            月度趋势分析结果
        """
        if len(monthly_stats) < 2:
            return {
                "trend": "insufficient_data",
                "message": "需要至少 2 个月的数据才能进行趋势分析"
            }

        # 按时间正序排列（数据库返回的是倒序）
        stats = sorted(monthly_stats, key=lambda x: x['month'])

        # 1. 计算 mood 指数趋势
        mood_values = [s['avg_mood_index'] or 50 for s in stats]
        mood_trend = self._calculate_trend_slope(mood_values)

        # 2. 计算效价趋势
        valence_values = [s['avg_valence'] or 0 for s in stats]
        valence_trend = self._calculate_trend_slope(valence_values)

        # 3. 计算唤醒度趋势
        arousal_values = [s['avg_arousal'] or 0.5 for s in stats]
        arousal_trend = self._calculate_trend_slope(arousal_values)

        # 4. 计算风险趋势
        risk_values = [s['avg_risk_level'] or 0 for s in stats]
        risk_trend = self._calculate_trend_slope(risk_values)

        # 5. 五阶段变化趋势
        acceptance_values = [s.get('acceptance_ratio', 0) or 0 for s in stats]
        depression_values = [s.get('depression_ratio', 0) or 0 for s in stats]

        acceptance_trend = self._calculate_trend_slope(acceptance_values)
        depression_trend = self._calculate_trend_slope(depression_values)

        # 6. 综合评估
        overall_assessment = "stable"
        if mood_trend > 2 and valence_trend > 0.1:
            overall_assessment = "improving"
        elif mood_trend < -2 and valence_trend < -0.1:
            overall_assessment = "declining"
        elif abs(mood_trend) > 5:
            overall_assessment = "fluctuating"

        # 7. 阶段进展判断
        stage_progress = "stable"
        if acceptance_trend > 1 and depression_trend < -1:
            stage_progress = "improving"
        elif depression_trend > 2:
            stage_progress = "declining"

        return {
            "trend": overall_assessment,
            "mood_trend": round(mood_trend, 4),
            "valence_trend": round(valence_trend, 4),
            "arousal_trend": round(arousal_trend, 4),
            "risk_trend": round(risk_trend, 4),
            "acceptance_trend": round(acceptance_trend, 4),
            "depression_trend": round(depression_trend, 4),
            "stage_progress": stage_progress,
            "months_analyzed": len(stats),
            "monthly_data": [
                {
                    "month": str(s['month'])[:7] if hasattr(s['month'], '__str__') else s['month'],
                    "avg_mood_index": round(s['avg_mood_index'], 2) if s['avg_mood_index'] else 0,
                    "avg_valence": round(s['avg_valence'], 2) if s['avg_valence'] else 0,
                    "avg_arousal": round(s['avg_arousal'], 2) if s['avg_arousal'] else 0,
                    "avg_risk_level": round(s['avg_risk_level'], 2) if s['avg_risk_level'] else 0,
                    "dominant_stage": s['dominant_stage'],
                    "interaction_count": s['interaction_count']
                }
                for s in stats
            ]
        }


    def analyze_period_trend(self, state: EmotionState, period_stats: Dict) -> Dict:
        """
        按 10 天周期情绪趋势分析（30 天项目周期）
        Args:
            state: 用户情感状态
            period_stats: 周期统计数据（来自 get_period_emotion_stats）
        Returns:
            周期趋势分析结果
        """
        periods = period_stats.get('periods', [])
        
        if len(periods) < 2:
            return {
                "trend": "insufficient_data",
                "message": "需要至少 2 个周期的数据才能进行趋势分析"
            }
        
        # 定义周期名称
        period_names = {
            1: "急性期 (1-10 天)",
            2: "整合期 (11-20 天)",
            3: "接受期 (21-30 天)"
        }
        
        # 1. 计算 mood 指数趋势
        mood_values = [p.get('avg_mood_index') or 50 for p in periods]
        mood_trend = self._calculate_trend_slope(mood_values)
        
        # 2. 计算效价趋势
        valence_values = [p.get('avg_valence') or 0 for p in periods]
        valence_trend = self._calculate_trend_slope(valence_values)
        
        # 3. 计算唤醒度趋势
        arousal_values = [p.get('avg_arousal') or 0.5 for p in periods]
        arousal_trend = self._calculate_trend_slope(arousal_values)
        
        # 4. 计算风险趋势
        risk_values = [p.get('avg_risk_level') or 0 for p in periods]
        risk_trend = self._calculate_trend_slope(risk_values)
        
        # 5. 五阶段变化趋势
        acceptance_values = [p.get('acceptance_ratio', 0) or 0 for p in periods]
        depression_values = [p.get('depression_ratio', 0) or 0 for p in periods]
        
        acceptance_trend = self._calculate_trend_slope(acceptance_values)
        depression_trend = self._calculate_trend_slope(depression_values)
        
        # 6. 综合评估
        overall_assessment = "stable"
        if mood_trend > 2 and valence_trend > 0.1:
            overall_assessment = "improving"
        elif mood_trend < -2 and valence_trend < -0.1:
            overall_assessment = "declining"
        elif abs(mood_trend) > 5:
            overall_assessment = "fluctuating"
        
        # 7. 阶段进展判断
        stage_progress = "stable"
        if acceptance_trend > 1 and depression_trend < -1:
            stage_progress = "improving"
        elif depression_trend > 2:
            stage_progress = "declining"
        
        # 8. 周期详细数据
        period_data = []
        for p in periods:
            period_num = int(p['period_num']) if not isinstance(p['period_num'], int) else p['period_num']
            period_data.append({
                "period": period_names.get(period_num, f"第{period_num}周期"),
                "period_num": period_num,
                "avg_mood_index": round(p['avg_mood_index'], 2) if p['avg_mood_index'] else 0,
                "avg_valence": round(p['avg_valence'], 2) if p['avg_valence'] else 0,
                "avg_arousal": round(p['avg_arousal'], 2) if p['avg_arousal'] else 0,
                "avg_risk_level": round(p['avg_risk_level'], 2) if p['avg_risk_level'] else 0,
                "avg_grief_density": round(p['avg_grief_density'], 2) if p['avg_grief_density'] else 0,
                "dominant_stage": p['dominant_stage'],
                "interaction_count": p['interaction_count'],
                "denial_ratio": round(p['denial_ratio'], 2) if p['denial_ratio'] else 0,
                "anger_ratio": round(p['anger_ratio'], 2) if p['anger_ratio'] else 0,
                "bargaining_ratio": round(p['bargaining_ratio'], 2) if p['bargaining_ratio'] else 0,
                "depression_ratio": round(p['depression_ratio'], 2) if p['depression_ratio'] else 0,
                "acceptance_ratio": round(p['acceptance_ratio'], 2) if p['acceptance_ratio'] else 0
            })
        
        return {
            "trend": overall_assessment,
            "mood_trend": round(mood_trend, 4),
            "valence_trend": round(valence_trend, 4),
            "arousal_trend": round(arousal_trend, 4),
            "risk_trend": round(risk_trend, 4),
            "acceptance_trend": round(acceptance_trend, 4),
            "depression_trend": round(depression_trend, 4),
            "stage_progress": stage_progress,
            "periods_analyzed": len(periods),
            "period_data": period_data
        }

    def analyze_monthly_trend(self, state: EmotionState, monthly_stats: List[Dict]) -> Dict:
        """
        按月情绪趋势分析（已废弃，请使用 analyze_period_trend）
        Args:
            state: 用户情感状态
            monthly_stats: 月度统计数据
        Returns:
            月度趋势分析结果
        """
        # 重定向到周期分析
        return self.analyze_period_trend(state, {"periods": monthly_stats})


# 全局引擎实例
emotion_engine = EmotionEngine()
