# Professional Sentiment Analysis Tool 🚀

A secure, offline sentiment analysis application designed for government agencies, legal firms, and organizations requiring confidential data processing without cloud dependencies.

## 🎯 Purpose & Use Case

In government agencies, law firms, and legal departments, there's a critical need to:
- **Quickly categorize and prioritize** large volumes of text data (complaints, feedback, legal documents)
- **Route tasks to appropriate teams** based on sentiment urgency and content tone
- **Process sensitive information locally** without cloud services due to confidentiality requirements
- **Work with existing Excel/CSV workflows** that are standard in these organizations

This tool addresses these needs by providing **local, CPU-based sentiment analysis** that integrates seamlessly with existing data formats while maintaining complete data privacy.

## ✨ Key Features

### 🔒 **Security & Privacy First**
- **100% Offline Processing** - No data leaves your machine
- **Local AI Models** - All analysis runs on CPU/local resources
- **No Cloud Dependencies** - Perfect for classified or sensitive data
- **GDPR/Compliance Ready** - Maintains data sovereignty

### 📊 **Professional Data Handling**
- **Excel/CSV Integration** - Direct import of existing spreadsheets
- **Batch Processing** - Handle thousands of records efficiently
- **Multiple AI Models** - TextBlob, VADER, BERT, RoBERTa support
- **Real-time Progress** - Live updates during analysis

### 🎨 **User-Friendly Interface**
- **Intuitive GUI** - No technical expertise required
- **Drag & Drop** - Easy file loading
- **Visual Results** - Charts and statistics
- **Export Ready** - Save results back to Excel/CSV

## 🏛️ Target Organizations

- **Government Agencies** - Citizen feedback analysis, complaint categorization
- **Legal Firms** - Document sentiment analysis, case prioritization
- **Attorney Offices** - Client communication analysis, urgency assessment
- **Corporate Legal** - Contract review, compliance monitoring
- **Public Sector** - Survey analysis, public opinion assessment

## 🚀 Quick Start

### Prerequisites
- macOS, Windows, or Linux
- Python 3.9+ (system Python recommended)
- No internet required after installation

### Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd CA_Gov
   ```

2. **Run the setup script**
   ```bash
   chmod +x LAUNCH_SENTIMENT_ANALYSIS.sh
   ./LAUNCH_SENTIMENT_ANALYSIS.sh
   ```

3. **Launch the application**
   - The GUI will automatically open
   - Select your Excel/CSV file
   - Choose text column for analysis
   - Select AI model and start processing

## 📋 Workflow Example

### Government Agency Use Case
1. **Import** citizen feedback Excel file
2. **Select** "Comments" column for analysis
3. **Choose** VADER model (optimized for social media/informal text)
4. **Analyze** 10,000+ records in minutes
5. **Export** results with sentiment labels:
   - 🔴 **Negative** → Priority/Urgent team
   - 🟡 **Neutral** → Standard processing team
   - 🟢 **Positive** → Acknowledgment team

### Legal Firm Use Case
1. **Import** client communication spreadsheet
2. **Select** "Message Content" column
3. **Choose** BERT model (high accuracy for formal text)
4. **Analyze** and categorize by urgency
5. **Route** cases based on sentiment scores

## 🤖 AI Models Available

| Model | Best For | Speed | Accuracy | Use Case |
|-------|----------|-------|----------|----------|
| **TextBlob** | General text | ⚡ Fast | Good | Quick processing |
| **VADER** | Social media, informal | ⚡ Fast | Good | Citizen feedback |
| **DistilBERT** | Balanced performance | 🔄 Medium | High | Professional docs |
| **RoBERTa** | Maximum accuracy | 🐌 Slow | Highest | Critical analysis |

## 📊 Output Format

The tool adds sentiment analysis columns to your original data:

| Original Column | AI_Sentiment | AI_Sentiment_Score | AI_Sentiment_Confidence |
|----------------|--------------|-------------------|------------------------|
| "Service was terrible" | Negative | -0.8 | 0.95 |
| "Thank you for help" | Positive | 0.7 | 0.89 |
| "Need more information" | Neutral | 0.1 | 0.76 |

## 🛡️ Security Features

- **Air-gapped Operation** - Works completely offline
- **Local Model Storage** - All AI models stored locally
- **No Telemetry** - Zero data collection or transmission
- **Audit Trail** - Complete processing logs
- **Data Integrity** - Original files remain unchanged

## 📁 File Support

- **Excel Files** (.xlsx, .xls)
- **CSV Files** (.csv)
- **Large Datasets** (tested up to 100K+ records)
- **Unicode Support** (multilingual text)

## 🔧 Technical Architecture

```
┌─────────────────────────────────────────┐
│           GUI Layer (tkinter)           │
├─────────────────────────────────────────┤
│        Business Logic Layer            │
│  - File Processing                      │
│  - Analysis Engine                      │
│  - Results Management                   │
├─────────────────────────────────────────┤
│         AI Models Layer                 │
│  - TextBlob (Rule-based)               │
│  - VADER (Lexicon-based)               │
│  - Transformers (Neural Networks)      │
├─────────────────────────────────────────┤
│         Data Layer                      │
│  - pandas (Excel/CSV)                  │
│  - numpy (calculations)                │
│  - matplotlib (visualization)          │
└─────────────────────────────────────────┘
```

## 🚀 Performance

- **Processing Speed**: 1,000-10,000 records per minute (depending on model)
- **Memory Usage**: Optimized for standard office computers
- **CPU Requirements**: Works on any modern processor
- **Storage**: ~500MB for all models

## 📈 Use Cases by Industry

### Government & Public Sector
- Citizen complaint prioritization
- Public feedback analysis
- Survey response categorization
- Social media monitoring (offline)

### Legal & Attorney Services
- Client communication analysis
- Document sentiment assessment
- Case priority determination
- Contract review assistance

### Corporate Compliance
- Employee feedback analysis
- Regulatory document review
- Risk assessment support
- Internal audit assistance

## 📋 Installation & Setup

### For Mac/Linux Users:
```bash
# Navigate to project directory
cd ~/Desktop/LLM_Project/CA_Gov

# Make launch script executable
chmod +x LAUNCH_SENTIMENT_ANALYSIS.sh

# Run the application
./LAUNCH_SENTIMENT_ANALYSIS.sh
```

### For Windows Users:
1. Ensure Python 3.9+ is installed from https://python.org
2. Open Command Prompt in the project directory
3. Run: `LAUNCH_SENTIMENT_ANALYSIS.bat`

## 🎯 Usage Instructions

1. **Launch Application**: Run the launch script
2. **Load Data**: Click "Browse File" and select your Excel/CSV file
3. **Preview Data**: Review your data in the preview tab
4. **Select Column**: Choose the text column for analysis
5. **Choose Model**: Select appropriate AI model for your use case
6. **Start Analysis**: Click "Start Analysis" and monitor progress
7. **Review Results**: View statistics and charts in the Results tab
8. **Export Data**: Save results back to Excel/CSV format

## 📊 Sample Output

After analysis, you'll get comprehensive results:

```
📊 SENTIMENT ANALYSIS RESULTS
==================================================

📈 Distribution:
   😊 Positive: 1,247 (62.4%)
   😞 Negative: 423 (21.2%)
   😐 Neutral:  330 (16.5%)

🎯 Confidence Metrics:
   Average Confidence: 0.847
   High Confidence (>0.7): 1,654 (82.7%)

📋 Summary:
   Total Records: 2,000
   Model Used: VADER
   Text Column: CustomerFeedback
   Analysis Date: 2024-12-23 14:30:52
```

## 🛠️ Troubleshooting

### Common Issues:

**GUI doesn't appear:**
- Check if tkinter is installed: `python -c "import tkinter"`
- Use system Python instead of Homebrew Python on Mac

**Model loading fails:**
- Ensure internet connection for initial model download
- Check available disk space (500MB+ required)

**File loading errors:**
- Verify file format (.xlsx, .xls, .csv)
- Check for password-protected files
- Ensure file isn't open in another application

**Performance issues:**
- Use TextBlob or VADER for faster processing
- Process files in smaller batches if memory limited

## 🤝 Contributing

This project prioritizes data privacy and security. When contributing:
- Maintain offline-first architecture
- Ensure no data transmission to external services
- Follow security best practices
- Test with sensitive data scenarios

## 📄 License

[Add your preferred license here]

## 🆘 Support

For technical support:
- Check the built-in application logs
- Verify system requirements are met
- Ensure all dependencies are properly installed
- Review troubleshooting section above

---

**Built for professionals who need reliable, secure, and efficient sentiment analysis without compromising data privacy.**
