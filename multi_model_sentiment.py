#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Multi-Model Customer Service Sentiment Analysis Tool
多模型客服情感分析工具 - 可选择不同复杂度的模型
"""

import pandas as pd
import numpy as np
import time
import os
import sys
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class ModelSelector:
    """模型选择和管理类"""
    
    def __init__(self):
        self.available_models = {}
        self.check_available_packages()
    
    def check_available_packages(self):
        """检查可用的包和模型"""
        print("🔍 Checking available AI packages...")
        
        # 检查基础包
        try:
            from textblob import TextBlob
            self.available_models['textblob'] = {
                'name': 'TextBlob',
                'level': 'Basic',
                'size': '~50MB',
                'speed': 'Very Fast',
                'accuracy': '65-70%',
                'description': 'Simple rule-based analysis',
                'available': True
            }
            print("✅ TextBlob - Basic model available")
        except ImportError:
            self.available_models['textblob'] = {'available': False}
        
        # 检查VADER
        try:
            from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
            self.available_models['vader'] = {
                'name': 'VADER',
                'level': 'Lightweight',
                'size': '~80MB',
                'speed': 'Very Fast',
                'accuracy': '75-80%',
                'description': 'Social media optimized lexicon',
                'available': True
            }
            print("✅ VADER - Lightweight model available")
        except ImportError:
            self.available_models['vader'] = {'available': False}
        
        # 检查transformers (轻量级模型)
        try:
            from transformers import pipeline
            
            # 轻量级BERT模型
            self.available_models['distilbert'] = {
                'name': 'DistilBERT',
                'level': 'Standard',
                'size': '~250MB',
                'speed': 'Fast',
                'accuracy': '82-85%',
                'description': 'Lightweight BERT (50% smaller)',
                'model_name': 'distilbert-base-uncased-finetuned-sst-2-english',
                'available': True
            }
            
            # RoBERTa Twitter模型
            self.available_models['roberta'] = {
                'name': 'RoBERTa-Twitter',
                'level': 'Professional',
                'size': '~500MB',
                'speed': 'Medium',
                'accuracy': '85-88%',
                'description': 'RoBERTa trained on Twitter data',
                'model_name': 'cardiffnlp/twitter-roberta-base-sentiment-latest',
                'available': True
            }
            
            # BERT Large (需要更多资源)
            self.available_models['bert_large'] = {
                'name': 'BERT-Large',
                'level': 'Enterprise',
                'size': '~1.3GB',
                'speed': 'Slow',
                'accuracy': '88-92%',
                'description': 'Full BERT model with maximum accuracy',
                'model_name': 'nlptown/bert-base-multilingual-uncased-sentiment',
                'available': True
            }
            
            print("✅ Transformers - Advanced models available")
        except ImportError:
            for model in ['distilbert', 'roberta', 'bert_large']:
                self.available_models[model] = {'available': False}
        
        # 检查OpenAI (如果有API key)
        try:
            import openai
            self.available_models['openai'] = {
                'name': 'OpenAI GPT',
                'level': 'Cloud',
                'size': 'API Call',
                'speed': 'Medium',
                'accuracy': '90-95%',
                'description': 'OpenAI GPT models (requires API key)',
                'available': True
            }
            print("✅ OpenAI - Cloud models available (requires API key)")
        except ImportError:
            self.available_models['openai'] = {'available': False}

class MultiModelSentimentAnalyzer:
    """多模型情感分析器"""
    
    def __init__(self, model_choice='auto'):
        self.model_choice = model_choice
        self.model_selector = ModelSelector()
        self.selected_model = None
        self.analyzer = None
        
        if model_choice == 'auto':
            self.auto_select_model()
        else:
            self.load_specific_model(model_choice)
    
    def auto_select_model(self):
        """自动选择最佳可用模型"""
        print("\n🤖 Auto-selecting best available model...")
        
        # 优先级顺序 (考虑性能和准确率平衡)
        priority_order = ['roberta', 'distilbert', 'vader', 'textblob']
        
        for model_key in priority_order:
            if (model_key in self.model_selector.available_models and 
                self.model_selector.available_models[model_key].get('available', False)):
                self.selected_model = model_key
                print(f"🎯 Auto-selected: {self.model_selector.available_models[model_key]['name']}")
                break
        
        if not self.selected_model:
            print("❌ No models available!")
            return False
        
        return self.load_model()
    
    def load_specific_model(self, model_key):
        """加载指定模型"""
        if (model_key in self.model_selector.available_models and 
            self.model_selector.available_models[model_key].get('available', False)):
            self.selected_model = model_key
            return self.load_model()
        else:
            print(f"❌ Model '{model_key}' not available!")
            return False
    
    def load_model(self):
        """加载选定的模型"""
        model_info = self.model_selector.available_models[self.selected_model]
        print(f"\n⏳ Loading {model_info['name']} model...")
        start_time = time.time()
        
        try:
            if self.selected_model == 'textblob':
                from textblob import TextBlob
                self.analyzer = lambda text: self._textblob_analyze(text)
                
            elif self.selected_model == 'vader':
                from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                self.vader_analyzer = SentimentIntensityAnalyzer()
                self.analyzer = lambda text: self._vader_analyze(text)
                
            elif self.selected_model in ['distilbert', 'roberta', 'bert_large']:
                from transformers import pipeline
                model_name = model_info['model_name']
                self.transformer_pipeline = pipeline(
                    "sentiment-analysis",
                    model=model_name,
                    tokenizer=model_name,
                    return_all_scores=False
                )
                self.analyzer = lambda text: self._transformer_analyze(text)
                
            elif self.selected_model == 'openai':
                import openai
                # 需要用户提供API key
                api_key = input("Please enter your OpenAI API key: ").strip()
                if not api_key:
                    print("❌ No API key provided")
                    return False
                openai.api_key = api_key
                self.analyzer = lambda text: self._openai_analyze(text)
            
            load_time = time.time() - start_time
            print(f"✅ Model loaded successfully in {load_time:.2f} seconds")
            print(f"📊 Model info: {model_info['description']}")
            print(f"🎯 Expected accuracy: {model_info['accuracy']}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to load model: {e}")
            return False
    
    def _textblob_analyze(self, text):
        """TextBlob分析"""
        from textblob import TextBlob
        blob = TextBlob(text)
        polarity = blob.sentiment.polarity
        
        if polarity > 0.1:
            return 'Positive', abs(polarity), 'textblob'
        elif polarity < -0.1:
            return 'Negative', abs(polarity), 'textblob'
        else:
            return 'Neutral', 1 - abs(polarity), 'textblob'
    
    def _vader_analyze(self, text):
        """VADER分析"""
        scores = self.vader_analyzer.polarity_scores(text)
        compound = scores['compound']
        
        if compound >= 0.05:
            return 'Positive', abs(compound), 'vader'
        elif compound <= -0.05:
            return 'Negative', abs(compound), 'vader'
        else:
            return 'Neutral', 1 - abs(compound), 'vader'
    
    def _transformer_analyze(self, text):
        """Transformer模型分析"""
        # 截断过长的文本 (BERT有512 token限制)
        if len(text) > 500:
            text = text[:500]
        
        result = self.transformer_pipeline(text)
        label = result[0]['label']
        score = result[0]['score']
        
        # 标准化标签
        if label.upper() in ['POSITIVE', 'POS']:
            sentiment = 'Positive'
        elif label.upper() in ['NEGATIVE', 'NEG']:
            sentiment = 'Negative'
        else:
            sentiment = 'Neutral'
        
        return sentiment, score, 'transformer'
    
    def _openai_analyze(self, text):
        """OpenAI分析"""
        import openai
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{
                    "role": "user",
                    "content": f"Analyze the sentiment of this customer service feedback and respond with only one word: Positive, Negative, or Neutral. Text: '{text}'"
                }],
                max_tokens=10,
                temperature=0
            )
            
            result = response.choices[0].message.content.strip().title()
            
            if result in ['Positive', 'Negative', 'Neutral']:
                return result, 0.9, 'openai'  # OpenAI通常很准确
            else:
                return 'Neutral', 0.5, 'openai'
                
        except Exception as e:
            print(f"OpenAI API error: {e}")
            return 'Neutral', 0.5, 'openai_error'
    
    def analyze_text(self, text):
        """分析单个文本"""
        if not self.analyzer:
            return 'Neutral', 0.5, 'no_model'
        
        if not text or len(text.strip()) < 3:
            return 'Neutral', 0.5, 'empty'
        
        return self.analyzer(text)
    
    def batch_analyze(self, texts, show_progress=True):
        """批量分析"""
        results = []
        total = len(texts)
        start_time = time.time()
        
        if show_progress:
            print(f"\n🚀 Analyzing {total} texts with {self.model_selector.available_models[self.selected_model]['name']}...")
        
        for i, text in enumerate(texts):
            if show_progress and i % 100 == 0 and i > 0:
                elapsed = time.time() - start_time
                speed = i / elapsed
                eta = (total - i) / speed if speed > 0 else 0
                print(f"⏳ Progress: {i}/{total} ({i/total*100:.1f}%) - Speed: {speed:.1f} texts/sec - ETA: {eta:.0f}s")
            
            sentiment, confidence, method = self.analyze_text(text)
            results.append({
                'sentiment': sentiment,
                'confidence': round(confidence, 3),
                'method': method
            })
        
        total_time = time.time() - start_time
        if show_progress:
            print(f"✅ Analysis completed in {total_time:.2f} seconds")
            print(f"📈 Average speed: {total/total_time:.1f} texts per second")
        
        return results

def display_available_models():
    """显示可用模型"""
    selector = ModelSelector()
    
    print("\n" + "="*80)
    print("🤖 AVAILABLE SENTIMENT ANALYSIS MODELS")
    print("="*80)
    
    for key, model in selector.available_models.items():
        if model.get('available', False):
            print(f"\n🎯 {model['name']} ({key})")
            print(f"   Level: {model['level']}")
            print(f"   Size: {model['size']}")
            print(f"   Speed: {model['speed']}")
            print(f"   Accuracy: {model['accuracy']}")
            print(f"   Description: {model['description']}")
        else:
            print(f"\n❌ {key} - Not available (package not installed)")
    
    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS:")
    print("🥇 For best accuracy: RoBERTa-Twitter or BERT-Large")
    print("🥈 For best speed: VADER or TextBlob")
    print("🥉 For balanced performance: DistilBERT")
    print("☁️ For highest accuracy: OpenAI GPT (requires API key)")
    print("="*80)

def interactive_model_selection():
    """交互式模型选择"""
    selector = ModelSelector()
    available_models = [k for k, v in selector.available_models.items() if v.get('available', False)]
    
    if not available_models:
        print("❌ No models available! Please install required packages.")
        return None
    
    print("\n🎯 SELECT ANALYSIS MODEL:")
    print("0. Auto-select best available model")
    
    for i, model_key in enumerate(available_models, 1):
        model = selector.available_models[model_key]
        print(f"{i}. {model['name']} - {model['level']} ({model['accuracy']} accuracy)")
    
    while True:
        try:
            choice = input(f"\nChoose model (0-{len(available_models)}): ").strip()
            choice_num = int(choice)
            
            if choice_num == 0:
                return 'auto'
            elif 1 <= choice_num <= len(available_models):
                return available_models[choice_num - 1]
            else:
                print("❌ Invalid choice! Please try again.")
                
        except ValueError:
            print("❌ Please enter a number!")

def main():
    """主函数"""
    print("="*80)
    print("🚀 MULTI-MODEL SENTIMENT ANALYSIS TOOL")
    print("   多模型客服情感分析工具")
    print("="*80)
    
    # 显示可用模型
    display_available_models()
    
    # 用户选择模型
    selected_model = interactive_model_selection()
    if not selected_model:
        return
    
    # 初始化分析器
    analyzer = MultiModelSentimentAnalyzer(selected_model)
    
    # 测试样例
    test_texts = [
        "The customer service representative was extremely helpful and resolved my issue quickly!",
        "I waited 2 hours and the agent was rude. Terrible experience.",
        "The issue was resolved. Standard service.",
        "Outstanding support! Julie went above and beyond to help me.",
        "System keeps crashing and nobody can fix it. Very frustrated.",
        "Quick response and professional handling of my request.",
        "Not satisfied with the resolution provided.",
        "Perfect service, highly recommend!"
    ]
    
    print(f"\n🧪 TESTING WITH SAMPLE TEXTS:")
    print("-" * 80)
    
    # 批量分析测试
    start_time = time.time()
    results = analyzer.batch_analyze(test_texts, show_progress=False)
    analysis_time = time.time() - start_time
    
    # 显示结果
    for i, (text, result) in enumerate(zip(test_texts, results)):
        sentiment = result['sentiment']
        confidence = result['confidence']
        
        emoji = "😊" if sentiment == "Positive" else "😞" if sentiment == "Negative" else "😐"
        
        print(f"\n{i+1}. {text[:50]}...")
        print(f"   {emoji} {sentiment} (Confidence: {confidence:.3f})")
    
    # 性能统计
    print(f"\n" + "="*80)
    print("📊 PERFORMANCE METRICS:")
    print(f"   Model: {analyzer.model_selector.available_models[analyzer.selected_model]['name']}")
    print(f"   Total texts: {len(test_texts)}")
    print(f"   Analysis time: {analysis_time:.3f} seconds")
    print(f"   Speed: {len(test_texts)/analysis_time:.1f} texts/second")
    
    # 统计结果
    sentiments = [r['sentiment'] for r in results]
    for sentiment in ['Positive', 'Negative', 'Neutral']:
        count = sentiments.count(sentiment)
        percentage = count / len(sentiments) * 100
        emoji = "😊" if sentiment == "Positive" else "😞" if sentiment == "Negative" else "😐"
        print(f"   {emoji} {sentiment}: {count} ({percentage:.1f}%)")
    
    print("="*80)

if __name__ == "__main__":
    main()
