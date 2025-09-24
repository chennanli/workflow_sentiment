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

**Step 1: Launch Application**
```bash
./LAUNCH_SENTIMENT_ANALYSIS.sh
```

**Step 2: Load Your Data**
- Click "Select Excel/CSV File" in the File & Setup tab
- Choose your data file (try the included `Child_Support_Customer_Service_Survey.xlsx` sample)
- Preview your data in the "Data Preview" tab

**Step 3: Configure Analysis**
- Select the text column you want to analyze (e.g., "CustomerFeedback")
- The output column name will auto-generate (e.g., "CustomerFeedback_sentiment_results")
- Choose your AI model:
  - **TextBlob**: Fast, good for general text
  - **VADER**: Best for social media/informal text
  - **DistilBERT**: Balanced accuracy and speed
  - **RoBERTa**: Highest accuracy, slower

**Step 4: Run Analysis**
- Click "🚀 Start Analysis"
- Monitor real-time progress
- View results summary in the "Results" tab

**Step 5: Export Results**
- Save enhanced Excel file with sentiment columns added
- Copy analysis summary to clipboard
- Original data preserved with new sentiment columns added

## AI Models

| Model | Speed | Accuracy | Best For |
|-------|-------|----------|----------|
| **TextBlob** | ⚡ Fast | Good | Quick processing |
| **VADER** | ⚡ Fast | Good | Social media/informal text |
| **DistilBERT** | 🔄 Medium | High | Professional documents |
| **RoBERTa** | 🐌 Slow | Highest | Critical analysis |

## Output Format

The tool adds sentiment analysis columns to your original data:

| Original Text | CustomerFeedback_sentiment_results | CustomerFeedback_sentiment_results_score | CustomerFeedback_sentiment_results_confidence |
|---------------|-----------------------------------|----------------------------------------|---------------------------------------------|
| "Service was terrible" | Negative | 0.8 | 0.95 |
| "Thank you for help" | Positive | 0.7 | 0.89 |
| "Need more information" | Neutral | 0.1 | 0.76 |

## Sample Workflow

**Try with the included sample data:**

1. **Launch the application**: `./LAUNCH_SENTIMENT_ANALYSIS.sh`
2. **Load sample file**: Select `Child_Support_Customer_Service_Survey.xlsx`
3. **Choose column**: Select "CustomerFeedback" from dropdown
4. **Output naming**: Will auto-generate "CustomerFeedback_sentiment_results"
5. **Select model**: Choose "VADER" for customer feedback analysis
6. **Run analysis**: Click "🚀 Start Analysis" and watch progress
7. **Review results**: Check the Results tab for statistics
8. **Export**: Save the enhanced Excel file with sentiment columns

**Expected Results:**
- 40 customer feedback entries analyzed
- Sentiment distribution (Positive/Negative/Neutral percentages)
- Confidence scores for each prediction
- New Excel file with 3 additional columns:
  - `CustomerFeedback_sentiment_results` (Positive/Negative/Neutral)
  - `CustomerFeedback_sentiment_results_score` (numerical score)
  - `CustomerFeedback_sentiment_results_confidence` (confidence level)

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
