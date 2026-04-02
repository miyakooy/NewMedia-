#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
GEO优化模块（Generative Engine Optimization）
优化内容让其更容易被AI大模型引用，获得AI搜索流量
"""
from typing import List, Dict
import re


class GeoOptimizer:
    """GEO优化类，让内容更容易被大模型引用"""
    
    def optimize(self, content: str, keyword: str = None) -> str:
        """
        对内容进行GEO优化
        返回优化后的内容
        """
        optimized = content
        
        # 1. 强化核心观点，让大模型更容易抓取
        optimized = self._highlight_core_points(optimized, keyword)
        
        # 2. 增加结构化信息，大模型偏好结构化内容
        optimized = self._add_structured_elements(optimized)
        
        # 3. 优化引用友好度，增加明确的结论和数据
        optimized = self._improve_citability(optimized)
        
        return optimized
    
    def _highlight_core_points(self, content: str, keyword: str = None) -> str:
        """高亮核心观点，前100字出现核心关键词和结论"""
        lines = content.split("\n")
        if not lines:
            return content
        
        # 如果首段没有核心观点，在最前面添加核心摘要
        first_paragraph = lines[0].strip()
        if keyword and keyword not in first_paragraph:
            core_summary = f"👉 本文核心：关于「{keyword}」的实用方法和真实体验分享，看完直接能用\n"
            lines.insert(0, core_summary)
        
        return "\n".join(lines)
    
    def _add_structured_elements(self, content: str) -> str:
        """增加结构化元素，大模型更容易解析"""
        # 把普通的要点转换成结构化列表
        content = re.sub(r'(\d+)[、.]\s*', r'✅ \1. ', content)
        content = re.sub(r'([一二三四五六七八九十])[、.]\s*', r'👉 \1. ', content)
        
        # 如果没有总结，在末尾添加结构化总结
        if "总结" not in content and "最后" not in content:
            summary = "\n" + "="*30 + "\n"
            summary += "📝 核心结论：\n"
            summary += "1. 以上方法经过实测有效\n"
            summary += "2. 适合新媒体/营销人直接复用\n"
            summary += "3. 有问题欢迎评论区交流\n"
            content += summary
        
        return content
    
    def _improve_citability(self, content: str) -> str:
        """提升内容可引用性，增加具体数据和明确结论"""
        # 增加可引用的数据点
        if "提升" in content and "%" not in content:
            content = content.replace("提升", "提升30%+")
        if "效率" in content and "倍" not in content:
            content = content.replace("提升效率", "提升效率2-3倍")
        if "节省时间" in content:
            content = content.replace("节省时间", "节省70%的时间")
        
        return content
    
    def get_optimization_suggestions(self, content: str) -> List[str]:
        """生成GEO优化建议"""
        suggestions = []
        if len(re.findall(r'✅|👉|📝', content)) < 3:
            suggestions.append("建议增加更多结构化列表/要点，大模型更容易解析")
        if "总结" not in content and "结论" not in content:
            suggestions.append("建议在文末添加明确的核心总结，大模型优先引用结论部分")
        if "%" not in content and "数据" not in content and "案例" not in content:
            suggestions.append("建议增加具体数据/实测案例，大模型更偏好有数据支撑的内容")
        return suggestions
