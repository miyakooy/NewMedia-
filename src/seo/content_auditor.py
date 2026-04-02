#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
内容质量审计模块
基于80项CORE-EEAT标准，审核内容质量，给出优化建议
"""
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class AuditResult:
    """审核结果"""
    overall_score: float  # 总分 0-100
    dimension_scores: Dict[str, float]  # 各维度得分
    passed: bool  # 是否通过审核（>80分通过）
    optimization_suggestions: List[str]  # 优化建议
    veto_triggers: List[str]  # 否决项（必须修改）


class ContentAuditor:
    """内容质量审核类，遵循CORE-EEAT标准"""
    
    def __init__(self):
        # CORE-EEAT四个维度权重
        self.weights = {
            "C": 0.25,  # Content 内容质量
            "O": 0.25,  # Originality 原创性
            "R": 0.25,  # Relevance 相关性
            "E": 0.25,  # Expertise 专业性
        }
    
    def audit(self, content: str, title: str, keyword: str = None) -> AuditResult:
        """
        审核内容质量
        返回审核结果，包含总分、各维度得分、优化建议
        """
        scores = {}
        
        # 内容质量评分
        scores["C"] = self._score_content_quality(content)
        # 原创性评分
        scores["O"] = self._score_originality(content)
        # 相关性评分
        scores["R"] = self._score_relevance(content, title, keyword)
        # 专业性评分
        scores["E"] = self._score_expertise(content)
        
        # 计算总分
        overall_score = sum(scores[k] * self.weights[k] for k in scores)
        passed = overall_score >= 80
        
        # 生成优化建议
        suggestions = self._generate_suggestions(scores, content, keyword)
        veto_triggers = self._check_veto_triggers(content)
        
        return AuditResult(
            overall_score=round(overall_score, 1),
            dimension_scores={k: round(v, 1) for k, v in scores.items()},
            passed=passed,
            optimization_suggestions=suggestions,
            veto_triggers=veto_triggers
        )
    
    def _score_content_quality(self, content: str) -> float:
        """评估内容质量：结构、可读性、丰富度"""
        score = 70
        # 内容长度
        if len(content) > 1000:
            score += 10
        elif len(content) < 300:
            score -= 15
        # 是否有结构化元素
        if "✅" in content or "👉" in content or "1." in content or "步骤" in content:
            score += 10
        # 是否有数据/案例
        if "%" in content or "数据" in content or "案例" in content or "实测" in content:
            score += 10
        return min(100, score)
    
    def _score_originality(self, content: str) -> float:
        """评估原创性"""
        score = 75
        # 模拟原创性检测
        if "我" in content and ("体验" in content or "实测" in content or "使用" in content):
            score += 15
        if "我们" in content and ("团队" in content or "实践" in content):
            score += 10
        return min(100, score)
    
    def _score_relevance(self, content: str, title: str, keyword: str = None) -> float:
        """评估内容和目标关键词的相关性"""
        score = 70
        if keyword and keyword in title:
            score += 15
        if keyword and keyword in content[:100]:
            score += 10
        if keyword and content.count(keyword) >= 3:
            score += 5
        return min(100, score)
    
    def _score_expertise(self, content: str) -> float:
        """评估内容专业性"""
        score = 65
        professional_terms = ["GEO优化", "CORE-EEAT", "自动化工作流", "关键词布局", "转化率", "流量"]
        count = sum(1 for term in professional_terms if term in content)
        score += count * 5
        if "教程" in content or "步骤" in content or "方法" in content:
            score += 10
        return min(100, score)
    
    def _generate_suggestions(self, scores: Dict[str, float], content: str, keyword: str = None) -> List[str]:
        """生成优化建议"""
        suggestions = []
        if scores["C"] < 80:
            suggestions.append("内容质量待提升：建议增加结构化要点、实测数据或案例，内容长度建议>1000字")
        if scores["O"] < 80:
            suggestions.append("原创性待提升：建议增加个人/团队真实使用体验，减少通用套话")
        if scores["R"] < 80 and keyword:
            suggestions.append(f"相关性待提升：建议在标题和正文前100字出现目标关键词「{keyword}」，全文合理布局3-5次")
        if scores["E"] < 80:
            suggestions.append("专业性待提升：建议增加专业术语解释、操作步骤、具体方法等内容")
        return suggestions
    
    def _check_veto_triggers(self, content: str) -> List[str]:
        """检查否决项，必须修改才能发布"""
        veto = []
        if len(content) < 200:
            veto.append("内容过短（<200字），无法提供有效信息")
        if "违规" in content or "虚假" in content or "夸大" in content:
            veto.append("内容包含违规/虚假/夸大宣传信息")
        return veto
