#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Advanced Customer Service Sentiment Analysis with Modern ML
使用现代机器学习的高级客服情感分析
"""

import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# 现代ML包
try:
    from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
    TRANSFORMERS_AVAILABLE = True
    print("✓ Transformers (BERT/RoBERTa) available")
except ImportError:
    TRANSFORMERS_AVAILABLE = False
    print("⚠️ Transformers not available, falling back to traditional methods")

try:
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    from sklearn.pipeline import Pipeline
    from sklearn.model_selection import cross_val_score
    SKLEARN_AVAILABLE = True
    print("✓ Scikit-learn available")
except ImportError:
    SKLEARN_AVAILABLE = False

# 传统方法作为fallback
try:
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    print("✓ Traditional methods available")
except ImportError:
    print("⚠️ Installing traditional sentiment tools...")
    import subprocess
    import sys
    subprocess.check_call([sys.executable, "-m", "pip", "install", "textblob", "vaderSentiment"])
    from textblob import TextBlob
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

class AdvancedSentimentAnalyzer:
    def __init__(self, use_advanced=True):
        """
        初始化高级情感分析器
        use_advanced: 是否使用BERT/RoBERTa等现代模型
        """
        self.use_advanced = use_advanced and TRANSFORMERS_AVAILABLE
        
        if self.use_advanced:
            print("🚀 Loading BERT-based sentiment model...")
            try:
                # 使用专门的情感分析模型
                self.transformer_model = pipeline(
                    "sentiment-analysis",
                    model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                    tokenizer="cardiffnlp/twitter-roberta-base-sentiment-latest"
                )
                print("✅ Advanced BERT/RoBERTa model loaded")
            except Exception as e:
                print(f"⚠️ Failed to load advanced model: {e}")
                print("🔄 Falling back to traditional methods")
                self.use_advanced = False
        
        # 传统方法作为backup
        self.vader = SentimentIntensityAnalyzer()
        print("✅ Traditional sentiment analyzers initialized")
        
        # 客服专用词典 (比TextBlob更专业)
        self.customer_service_positive = {
            # 服务质量
            'professional', 'helpful', 'courteous', 'patient', 'knowledgeable',
            'efficient', 'quick', 'responsive', 'thorough', 'excellent',
            # 解决问题
            'resolved', 'solved', 'fixed', 'helped', 'assisted', 'guided',
            'explained', 'clarified', 'understood', 'satisfied',
            # 情感表达
            'thank', 'appreciate', 'grateful', 'pleased', 'happy',
            'recommend', 'impressed', 'outstanding', 'amazing', 'perfect'
        }
        
        self.customer_service_negative = {
            # 服务问题
            'unprofessional', 'rude', 'impatient', 'unhelpful', 'slow',
            'confusing', 'unclear', 'difficult', 'complicated', 'frustrated',
            # 问题未解决
            'unresolved', 'unsolved', 'failed', 'unable', 'refused',
            'ignored', 'dismissed', 'hung up', 'transferred', 'waiting',
            # 情感表达
            'disappointed', 'angry', 'upset', 'annoyed', 'complain',
            'terrible', 'awful', 'worst', 'horrible', 'disgusted'
        }

    def advanced_analysis(self, text):
        """使用BERT/RoBERTa进行高级分析"""
        if not self.use_advanced:
            return None
            
        try:
            # 使用transformer模型
            result = self.transformer_model(text)
            
            # 标准化输出
            label = result[0]['label'].upper()
            score = result[0]['score']
            
            # 转换标签格式
            if 'POS' in label:
                sentiment = 'Positive'
                confidence = score
            elif 'NEG' in label:
                sentiment = 'Negative'
                confidence = score
            else:
                sentiment = 'Neutral'
                confidence = score
                
            return sentiment, confidence, 'transformer'
            
        except Exception as e:
            print(f"Advanced analysis failed: {e}")
            return None

    def vader_analysis(self, text):
        """使用VADER进行分析 (比TextBlob更准确)"""
        try:
            scores = self.vader.polarity_scores(text)
            compound = scores['compound']
            
            # VADER的阈值经过优化
            if compound >= 0.05:
                return 'Positive', abs(compound), 'vader'
            elif compound <= -0.05:
                return 'Negative', abs(compound), 'vader'
            else:
                return 'Neutral', 1 - abs(compound), 'vader'
                
        except Exception:
            return None

    def textblob_analysis(self, text):
        """TextBlob分析 (最基础的方法)"""
        try:
            blob = TextBlob(text)
            polarity = blob.sentiment.polarity
            
            if polarity > 0.1:
                return 'Positive', polarity, 'textblob'
            elif polarity < -0.1:
                return 'Negative', abs(polarity), 'textblob'
            else:
                return 'Neutral', abs(polarity), 'textblob'
                
        except Exception:
            return 'Neutral', 0.5, 'textblob'

    def domain_specific_analysis(self, text):
        """客服领域专用分析"""
        words = text.lower().split()
        
        pos_count = sum(1 for word in words if word in self.customer_service_positive)
        neg_count = sum(1 for word in words if word in self.customer_service_negative)
        
        total_sentiment_words = pos_count + neg_count
        
        if total_sentiment_words == 0:
            return 'Neutral', 0.5, 'domain'
        
        if pos_count > neg_count:
            confidence = pos_count / total_sentiment_words
            return 'Positive', confidence, 'domain'
        elif neg_count > pos_count:
            confidence = neg_count / total_sentiment_words
            return 'Negative', confidence, 'domain'
        else:
            return 'Neutral', 0.5, 'domain'

    def ensemble_analysis(self, text):
        """集成多种方法的结果"""
        if not text or len(text.strip()) < 3:
            return 'Neutral', 0.5, 'empty'
        
        results = []
        methods_used = []
        
        # 1. 尝试高级模型
        if self.use_advanced:
            advanced_result = self.advanced_analysis(text)
            if advanced_result:
                results.append(advanced_result)
                methods_used.append('BERT/RoBERTa')
        
        # 2. VADER分析
        vader_result = self.vader_analysis(text)
        if vader_result:
            results.append(vader_result)
            methods_used.append('VADER')
        
        # 3. 领域专用分析
        domain_result = self.domain_specific_analysis(text)
        results.append(domain_result)
        methods_used.append('Domain-Specific')
        
        # 4. TextBlob作为fallback
        textblob_result = self.textblob_analysis(text)
        results.append(textblob_result)
        methods_used.append('TextBlob')
        
        # 集成决策
        if not results:
            return 'Neutral', 0.5, 'fallback'
        
        # 权重设置 (高级模型权重更高)
        weights = []
        if self.use_advanced and len(results) >= 1:
            weights.append(0.5)  # BERT/RoBERTa 50%权重
            weights.extend([0.25, 0.15, 0.1])  # 其他方法
        else:
            weights = [0.4, 0.3, 0.3]  # 没有高级模型时的权重
        
        # 确保权重数量匹配结果数量
        weights = weights[:len(results)]
        weights = [w / sum(weights) for w in weights]  # 归一化
        
        # 加权投票
        sentiment_scores = {'Positive': 0, 'Negative': 0, 'Neutral': 0}
        total_confidence = 0
        
        for i, (sentiment, confidence, method) in enumerate(results):
            weight = weights[i]
            sentiment_scores[sentiment] += weight * confidence
            total_confidence += weight * confidence
        
        # 最终决策
        final_sentiment = max(sentiment_scores.items(), key=lambda x: x[1])[0]
        final_confidence = min(sentiment_scores[final_sentiment], 1.0)
        
        method_info = f"Ensemble({'+'.join(methods_used)})"
        
        return final_sentiment, final_confidence, method_info

def main():
    """主函数"""
    print("="*80)
    print("🔬 Advanced Customer Service Sentiment Analysis")
    print("   使用现代机器学习技术的高级情感分析")
    print("="*80)
    
    # 询问是否使用高级模型
    use_advanced = True
    if TRANSFORMERS_AVAILABLE:
        choice = input("\n🚀 Use advanced BERT/RoBERTa models? (Y/n): ").strip().lower()
        use_advanced = choice != 'n'
    
    # 初始化分析器
    analyzer = AdvancedSentimentAnalyzer(use_advanced=use_advanced)
    
    # 测试样本
    test_texts = [
        "The customer service representative was extremely helpful and resolved my issue quickly. Excellent service!",
        "I had to wait 45 minutes and the agent was rude and unhelpful. Terrible experience.",
        "The issue was resolved. Standard service.",
        "Julie was amazing! She went above and beyond to help me understand my case. Very professional and patient.",
        "System kept giving errors and nobody could help me. Wasted 2 hours of my time."
    ]
    
    print(f"\n🧪 Testing with sample customer feedback:")
    print("-" * 80)
    
    for i, text in enumerate(test_texts, 1):
        sentiment, confidence, method = analyzer.ensemble_analysis(text)
        
        emoji = "😊" if sentiment == "Positive" else "😞" if sentiment == "Negative" else "😐"
        
        print(f"\n{i}. Text: {text[:60]}...")
        print(f"   {emoji} Result: {sentiment} (Confidence: {confidence:.3f})")
        print(f"   🔧 Method: {method}")
    
    print(f"\n" + "="*80)
    print("🎯 Method Comparison:")
    print("   🥇 BERT/RoBERTa: State-of-the-art transformer models")
    print("   🥈 VADER: Optimized for social media text")
    print("   🥉 Domain-Specific: Customer service vocabulary")
    print("   🔄 TextBlob: Basic pattern matching (fallback)")
    print("="*80)

if __name__ == "__main__":
    main()
