# Professional Sentiment Analysis Tool

A secure, offline sentiment analysis application designed for government agencies, legal firms, and organizations requiring confidential data processing without cloud dependencies.

## Purpose

In government agencies, law firms, and legal departments, there's a critical need to quickly categorize and prioritize large volumes of text data (complaints, feedback, legal documents) and route tasks to appropriate teams based on sentiment urgency. This tool provides **local, CPU-based sentiment analysis** that integrates with existing Excel/CSV workflows while maintaining complete data privacy.

## Key Features

- **100% Offline Processing** - No data leaves your machine
- **Multiple AI Models** - TextBlob, VADER, BERT, RoBERTa support
- **Excel/CSV Integration** - Direct import of existing spreadsheets
- **Professional GUI** - Intuitive interface with real-time progress
- **Batch Processing** - Handle thousands of records efficiently
- **Visual Results** - Charts and statistics with export capabilities

## Project Structure

```
├── sentiment_gui.py              # Main GUI application
├── multi_model_sentiment.py      # AI engine with multiple models
├── advanced_sentiment_analysis.py # Core analysis logic
├── LAUNCH_SENTIMENT_ANALYSIS.sh  # Setup and launch script
├── requirements.txt              # Python dependencies
├── Child_Support_Customer_Service_Survey.xlsx # Sample data
└── README.md                     # This file
```

## Quick Start

### Prerequisites
- Python 3.9+ (system Python recommended for macOS)
- No internet required after initial setup

### Installation & Launch

**Mac/Linux:**
```bash
chmod +x LAUNCH_SENTIMENT_ANALYSIS.sh
./LAUNCH_SENTIMENT_ANALYSIS.sh
```

**Windows:**
```bash
python -m venv sentiment_env
sentiment_env\Scripts\activate
pip install -r requirements.txt
python sentiment_gui.py
```

### Usage
1. Launch the application using the script above
2. Click "Browse File" and select your Excel/CSV file
3. Choose the text column for analysis
4. Select appropriate AI model for your use case
5. Click "Start Analysis" and monitor progress
6. Review results and export back to Excel/CSV

## AI Models

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| **TextBlob** | ⚡ Fast | Good | Quick processing |
| **VADER** | ⚡ Fast | Good | Social media/informal text |
| **DistilBERT** | 🔄 Medium | High | Professional documents |
| **RoBERTa** | 🐌 Slow | Highest | Critical analysis |

## Output Format

The tool adds sentiment analysis columns to your original data:

| Original Text | AI_Sentiment | AI_Sentiment_Score | AI_Sentiment_Confidence |
|---------------|--------------|-------------------|------------------------|
| "Service was terrible" | Negative | -0.8 | 0.95 |
| "Thank you for help" | Positive | 0.7 | 0.89 |
| "Need more information" | Neutral | 0.1 | 0.76 |

## Security & Privacy

- **Air-gapped Operation** - Works completely offline
- **Local Model Storage** - All AI models stored locally
- **No Data Transmission** - Zero external communication
- **GDPR Compliant** - Maintains complete data sovereignty

## Use Cases

**Government Agencies:** Citizen feedback analysis, complaint categorization
**Legal Firms:** Document sentiment analysis, case prioritization
**Attorney Offices:** Client communication analysis, urgency assessment
**Corporate Legal:** Contract review, compliance monitoring

## Troubleshooting

**GUI doesn't appear:** Use system Python instead of Homebrew Python on Mac
**Model loading fails:** Ensure internet connection for initial model download
**File loading errors:** Verify file format (.xlsx, .xls, .csv) and ensure file isn't password-protected

---

Built for professionals who need reliable, secure sentiment analysis without compromising data privacy.
