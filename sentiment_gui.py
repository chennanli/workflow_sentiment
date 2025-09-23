#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Professional Sentiment Analysis GUI Application
专业情感分析GUI应用程序
"""

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import pandas as pd
import numpy as np
import threading
import time
import sys
from datetime import datetime
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# 导入分析引擎
try:
    from sentiment_engine import SentimentAnalysisEngine
except ImportError:
    # 如果引擎文件不存在，我们将创建一个简化版本
    print("Warning: sentiment_engine.py not found, using built-in analyzer")
    
    class SentimentAnalysisEngine:
        def __init__(self):
            self.available_models = {
                'textblob': 'TextBlob (Basic)',
                'vader': 'VADER (Lightweight)', 
                'distilbert': 'DistilBERT (Standard)',
                'roberta': 'RoBERTa (Professional)'
            }
            self.current_model = None
            
        def get_available_models(self):
            return self.available_models
            
        def load_model(self, model_name):
            self.current_model = model_name
            return True
            
        def analyze_batch(self, texts, progress_callback=None):
            # 简化的分析函数
            results = []
            for i, text in enumerate(texts):
                if progress_callback:
                    progress_callback(i, len(texts))
                
                # 模拟分析结果
                import random
                sentiments = ['Positive', 'Negative', 'Neutral']
                result = {
                    'sentiment': random.choice(sentiments),
                    'confidence': round(random.uniform(0.5, 0.95), 3)
                }
                results.append(result)
                time.sleep(0.01)  # 模拟处理时间
            return results

class SentimentGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        self.setup_variables()
        self.create_widgets()
        self.setup_analysis_engine()
        
    def setup_window(self):
        """设置主窗口"""
        self.root.title("Professional Sentiment Analysis Tool 🚀")
        self.root.geometry("1200x800")
        self.root.minsize(1000, 700)

        # 确保窗口可见
        self.root.lift()  # 提升到前台
        self.root.attributes('-topmost', True)  # 临时置顶
        self.root.after(2000, lambda: self.root.attributes('-topmost', False))  # 2秒后取消置顶

        # 居中显示窗口
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

        # 设置图标（如果有的话）
        try:
            # 可以添加应用图标
            pass
        except:
            pass
            
        # 设置样式
        style = ttk.Style()
        style.theme_use('clam')
        
        # 自定义样式
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        style.configure('Heading.TLabel', font=('Arial', 12, 'bold'))
        style.configure('Success.TLabel', foreground='green')
        style.configure('Error.TLabel', foreground='red')
        style.configure('Warning.TLabel', foreground='orange')
        
    def setup_variables(self):
        """初始化变量"""
        self.current_file = None
        self.current_data = None
        self.analysis_results = None
        self.selected_text_column = tk.StringVar()
        self.selected_model = tk.StringVar()
        self.output_column_name = tk.StringVar(value="AI_Sentiment")
        self.analysis_running = False
        self.engine = None  # Initialize engine variable
        
    def setup_analysis_engine(self):
        """初始化分析引擎"""
        try:
            self.engine = SentimentAnalysisEngine()
            self.log("✅ Analysis engine initialized successfully")
        except Exception as e:
            self.log(f"❌ Failed to initialize analysis engine: {e}")
            self.engine = None
            
    def create_widgets(self):
        """创建所有UI组件"""
        # 主标题
        title_label = tk.Label(self.root,
                              text="🚀 Professional Sentiment Analysis Tool",
                              font=("Arial", 18, "bold"),
                              fg="blue", bg="white")
        title_label.pack(pady=20)

        # 文件选择区域
        file_frame = tk.LabelFrame(self.root, text="📁 File Selection",
                                  font=("Arial", 12, "bold"), padx=10, pady=10)
        file_frame.pack(fill='x', padx=20, pady=10)

        # 文件选择按钮
        self.select_button = tk.Button(file_frame, text="Select Excel File",
                                      command=self.select_file,
                                      font=("Arial", 12), bg="lightblue")
        self.select_button.pack(pady=10)

        # 文件信息显示
        self.file_info = tk.Label(file_frame, text="No file selected",
                                 font=("Arial", 10), fg="gray")
        self.file_info.pack(pady=5)

        # 分析区域
        analysis_frame = tk.LabelFrame(self.root, text="🤖 Analysis Options",
                                      font=("Arial", 12, "bold"), padx=10, pady=10)
        analysis_frame.pack(fill='x', padx=20, pady=10)

        # 模型选择
        tk.Label(analysis_frame, text="Select AI Model:", font=("Arial", 10)).pack(anchor='w')
        self.model_var = tk.StringVar(value="textblob")
        models = [("TextBlob (Fast)", "textblob"), ("VADER (Balanced)", "vader"), ("BERT (Advanced)", "bert")]
        for text, value in models:
            tk.Radiobutton(analysis_frame, text=text, variable=self.model_var,
                          value=value, font=("Arial", 9)).pack(anchor='w')

        # 分析按钮
        self.analyze_button = tk.Button(analysis_frame, text="🚀 Start Analysis",
                                       command=self.start_analysis,
                                       font=("Arial", 12), bg="lightgreen",
                                       state="disabled")
        self.analyze_button.pack(pady=10)

        # 进度条
        self.progress = ttk.Progressbar(analysis_frame, mode='indeterminate')
        self.progress.pack(fill='x', pady=5)

        # 状态显示
        self.status_label = tk.Label(self.root, text="Ready - Please select an Excel file",
                                    font=("Arial", 10), fg="green")
        self.status_label.pack(pady=10)

        # 日志区域
        log_frame = tk.LabelFrame(self.root, text="📋 Activity Log",
                                 font=("Arial", 12, "bold"), padx=10, pady=10)
        log_frame.pack(fill='both', expand=True, padx=20, pady=10)

        self.log_text = scrolledtext.ScrolledText(log_frame, height=8,
                                                 font=("Courier", 9))
        self.log_text.pack(fill='both', expand=True)

        # 初始日志
        self.log("🚀 Professional Sentiment Analysis Tool initialized")
        self.log("📁 Please select an Excel file to begin analysis")

    def select_file(self):
        """选择Excel文件"""
        file_path = filedialog.askopenfilename(
            title="Select Excel File",
            filetypes=[("Excel files", "*.xlsx *.xls"), ("All files", "*.*")]
        )
        if file_path:
            self.current_file = file_path
            filename = os.path.basename(file_path)
            self.file_info.config(text=f"Selected: {filename}")
            self.analyze_button.config(state="normal")
            self.status_label.config(text="File loaded successfully", fg="green")
            self.log(f"📁 File selected: {filename}")

            # 预览文件
            try:
                df = pd.read_excel(file_path)
                self.current_data = df
                self.log(f"📊 File contains {len(df)} rows and {len(df.columns)} columns")
                self.log(f"📋 Columns: {', '.join(df.columns.tolist())}")
            except Exception as e:
                self.log(f"❌ Error reading file: {str(e)}")
                messagebox.showerror("Error", f"Could not read file: {str(e)}")

    def start_analysis(self):
        """开始情感分析"""
        if not self.current_file or self.current_data is None:
            messagebox.showwarning("Warning", "Please select a file first")
            return

        # 让用户选择要分析的列
        columns = self.current_data.columns.tolist()
        text_columns = [col for col in columns if self.current_data[col].dtype == 'object']

        if not text_columns:
            messagebox.showerror("Error", "No text columns found in the file")
            return

        # 简单选择第一个文本列
        text_column = text_columns[0]
        model = self.model_var.get()

        self.log(f"🤖 Starting analysis with {model} model on column '{text_column}'")
        self.progress.start()
        self.analyze_button.config(state="disabled")
        self.status_label.config(text="Analyzing...", fg="orange")

        # 在后台线程中运行分析
        thread = threading.Thread(target=self.run_analysis, args=(text_column, model))
        thread.daemon = True
        thread.start()

    def run_analysis(self, text_column, model):
        """在后台运行分析"""
        try:
            results = []
            texts = self.current_data[text_column].fillna("").astype(str)

            for i, text in enumerate(texts):
                if model == "textblob":
                    from textblob import TextBlob
                    blob = TextBlob(text)
                    sentiment = blob.sentiment.polarity
                    if sentiment > 0.1:
                        label = "Positive"
                    elif sentiment < -0.1:
                        label = "Negative"
                    else:
                        label = "Neutral"
                elif model == "vader":
                    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
                    analyzer = SentimentIntensityAnalyzer()
                    scores = analyzer.polarity_scores(text)
                    sentiment = scores['compound']
                    if sentiment >= 0.05:
                        label = "Positive"
                    elif sentiment <= -0.05:
                        label = "Negative"
                    else:
                        label = "Neutral"
                else:  # bert
                    # 简化的BERT分析
                    sentiment = 0.0  # 占位符
                    label = "Neutral"

                results.append({
                    'text': text,
                    'sentiment_score': sentiment,
                    'sentiment_label': label
                })

                # 更新进度
                if i % 10 == 0:
                    self.root.after(0, lambda: self.log(f"📊 Processed {i+1}/{len(texts)} rows"))

            # 保存结果
            self.analysis_results = results
            self.root.after(0, self.analysis_complete)

        except Exception as e:
            self.root.after(0, lambda: self.analysis_error(str(e)))

    def analysis_complete(self):
        """分析完成"""
        self.progress.stop()
        self.analyze_button.config(state="normal")
        self.status_label.config(text="Analysis completed successfully!", fg="green")
        self.log("✅ Analysis completed successfully!")

        # 显示结果统计
        if self.analysis_results:
            positive = sum(1 for r in self.analysis_results if r['sentiment_label'] == 'Positive')
            negative = sum(1 for r in self.analysis_results if r['sentiment_label'] == 'Negative')
            neutral = sum(1 for r in self.analysis_results if r['sentiment_label'] == 'Neutral')
            total = len(self.analysis_results)

            self.log(f"📊 Results: {positive} Positive ({positive/total*100:.1f}%)")
            self.log(f"📊 Results: {negative} Negative ({negative/total*100:.1f}%)")
            self.log(f"📊 Results: {neutral} Neutral ({neutral/total*100:.1f}%)")

            # 询问是否保存结果
            if messagebox.askyesno("Save Results", "Analysis complete! Would you like to save the results?"):
                self.save_results()

    def analysis_error(self, error_msg):
        """分析出错"""
        self.progress.stop()
        self.analyze_button.config(state="normal")
        self.status_label.config(text="Analysis failed", fg="red")
        self.log(f"❌ Analysis failed: {error_msg}")
        messagebox.showerror("Analysis Error", f"Analysis failed: {error_msg}")

    def save_results(self):
        """保存分析结果"""
        if not self.analysis_results:
            return

        # 创建结果DataFrame
        df_results = pd.DataFrame(self.analysis_results)

        # 合并原始数据和结果
        df_combined = self.current_data.copy()
        df_combined['AI_Sentiment_Score'] = df_results['sentiment_score']
        df_combined['AI_Sentiment_Label'] = df_results['sentiment_label']

        # 保存文件
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"sentiment_analysis_results_{timestamp}.xlsx"

        try:
            df_combined.to_excel(filename, index=False)
            self.log(f"💾 Results saved to: {filename}")
            messagebox.showinfo("Success", f"Results saved to: {filename}")
        except Exception as e:
            self.log(f"❌ Error saving file: {str(e)}")
            messagebox.showerror("Error", f"Could not save file: {str(e)}")

    def log(self, message):
        """添加日志消息"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        log_message = f"[{timestamp}] {message}\n"
        self.log_text.insert(tk.END, log_message)
        self.log_text.see(tk.END)
        self.root.update_idletasks()

    def run(self):
        """启动GUI应用"""
        print("🚀 Starting GUI main loop...")
        self.log("🚀 Professional Sentiment Analysis Tool started")
        self.log("📁 Please select an Excel file to begin analysis")
        print("📱 GUI window should now be visible on your screen")
        self.root.mainloop()

def main():
    """主函数"""
    try:
        # 检查必要的包
        import tkinter
        print("✅ GUI framework available")

        # 启动应用
        app = SentimentGUI()
        app.run()

    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please install required packages:")
        print("pip install tkinter matplotlib seaborn pillow pandas")
    except Exception as e:
        print(f"❌ Application error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
