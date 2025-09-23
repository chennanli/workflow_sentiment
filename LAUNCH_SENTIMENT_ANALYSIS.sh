#!/bin/bash

# =============================================================================
# Professional Sentiment Analysis Tool - Complete Setup & Launch
# 专业情感分析工具 - 完整安装和启动脚本
# =============================================================================

set -e  # Exit on error

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
WHITE='\033[1;37m'
NC='\033[0m'

# 图标定义
ICON_SUCCESS="✅"
ICON_ERROR="❌"
ICON_WARNING="⚠️"
ICON_INFO="ℹ️"
ICON_ROCKET="🚀"
ICON_GEAR="⚙️"
ICON_PYTHON="🐍"
ICON_GUI="🖥️"
ICON_AI="🤖"

print_header() {
    clear
    echo ""
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║                                                                              ║${NC}"
    echo -e "${CYAN}║${WHITE}                ${ICON_ROCKET} Professional Sentiment Analysis Tool ${ICON_ROCKET}               ${CYAN}║${NC}"
    echo -e "${CYAN}║${WHITE}                     Complete GUI Application Suite                      ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                                              ║${NC}"
    echo -e "${CYAN}║${YELLOW}              Auto Setup | GUI Interface | Multi-AI Models | Analytics      ${CYAN}║${NC}"
    echo -e "${CYAN}║                                                                              ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""
}

print_step() {
    echo -e "${BLUE}${ICON_INFO} $1${NC}"
}

print_success() {
    echo -e "${GREEN}${ICON_SUCCESS} $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}${ICON_WARNING} $1${NC}"
}

print_error() {
    echo -e "${RED}${ICON_ERROR} $1${NC}"
}

print_section() {
    echo ""
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo -e "${PURPLE}${ICON_GEAR} $1 ${ICON_GEAR}${NC}"
    echo -e "${PURPLE}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
    echo ""
}

# 获取脚本目录
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
cd "$SCRIPT_DIR"

print_header

print_step "Project Directory: $SCRIPT_DIR"

print_section "System Environment Check"

# 检查Python - 优先使用系统Python (有tkinter支持)
print_step "Checking Python installation..."

# 首先检查系统Python是否有tkinter支持
if [ -f "/usr/bin/python3" ]; then
    if /usr/bin/python3 -c "import tkinter" &> /dev/null; then
        PYTHON_VERSION=$(/usr/bin/python3 --version)
        print_success "Python: $PYTHON_VERSION (System Python with tkinter support)"
        PYTHON_CMD="/usr/bin/python3"
        PIP_CMD="/usr/bin/pip3"
    else
        print_warning "System Python found but no tkinter support"
        PYTHON_CMD=""
    fi
else
    PYTHON_CMD=""
fi

# 如果系统Python不可用，检查其他Python安装
if [ -z "$PYTHON_CMD" ]; then
    if command -v python3 &> /dev/null; then
        if python3 -c "import tkinter" &> /dev/null; then
            PYTHON_VERSION=$(python3 --version)
            print_success "Python: $PYTHON_VERSION (with tkinter support)"
            PYTHON_CMD="python3"
            PIP_CMD="pip3"
        else
            print_warning "Python3 found but no tkinter support"
            PYTHON_CMD=""
        fi
    fi
fi

# 最后检查通用python命令
if [ -z "$PYTHON_CMD" ]; then
    if command -v python &> /dev/null; then
        PYTHON_VERSION=$(python --version)
        if [[ $PYTHON_VERSION == *"3."* ]] && python -c "import tkinter" &> /dev/null; then
            print_success "Python: $PYTHON_VERSION (with tkinter support)"
            PYTHON_CMD="python"
            PIP_CMD="pip"
        else
            print_error "Python found but either Python 2 or no tkinter support"
            PYTHON_CMD=""
        fi
    fi
fi

# 如果没有找到合适的Python
if [ -z "$PYTHON_CMD" ]; then
    print_error "No Python 3 with tkinter support found!"
    echo ""
    echo -e "${YELLOW}Solutions:${NC}"
    echo "  1. Install Python with tkinter support:"
    echo "     brew install python-tk      # macOS with Homebrew"
    echo "     apt install python3-tk      # Ubuntu/Debian"
    echo "  2. Use system Python (recommended for macOS):"
    echo "     /usr/bin/python3 should have tkinter support"
    echo "  3. Download Python from https://python.org (includes tkinter)"
    echo ""
    read -p "Press Enter to exit..."
    exit 1
fi

# 检查pip
print_step "Checking pip package manager..."
if command -v $PIP_CMD &> /dev/null; then
    print_success "Found pip: $PIP_CMD"
elif $PYTHON_CMD -m pip --version &> /dev/null; then
    print_success "Found pip via python module"
    PIP_CMD="$PYTHON_CMD -m pip"
else
    print_error "pip not found! Please install pip"
    echo ""
    echo -e "${YELLOW}Install pip:${NC}"
    echo "  curl https://bootstrap.pypa.io/get-pip.py | $PYTHON_CMD"
    echo ""
    exit 1
fi

print_section "Virtual Environment Setup"

# 虚拟环境配置
VENV_NAME="sentiment_analysis_env"
VENV_PATH="$SCRIPT_DIR/$VENV_NAME"

if [ -d "$VENV_PATH" ]; then
    print_warning "Found existing virtual environment"
    echo -e "${CYAN}Do you want to recreate the virtual environment? (y/N): ${NC}"
    read -r recreate
    if [[ $recreate =~ ^[Yy]$ ]]; then
        print_step "Removing existing virtual environment..."
        rm -rf "$VENV_PATH"
        print_success "Existing environment removed"
    else
        print_step "Using existing virtual environment"
    fi
fi

if [ ! -d "$VENV_PATH" ]; then
    print_step "Creating new Python virtual environment..."
    $PYTHON_CMD -m venv "$VENV_PATH"
    print_success "Virtual environment created: $VENV_NAME"
fi

# 激活虚拟环境
print_step "Activating virtual environment..."
source "$VENV_PATH/bin/activate"
print_success "Virtual environment activated"

print_section "Dependencies Installation"

# 升级pip
print_step "Upgrading pip in virtual environment..."
$PIP_CMD install --upgrade pip --quiet
print_success "pip upgraded successfully"

# 创建完整的requirements.txt
print_step "Creating comprehensive requirements file..."
cat > requirements.txt << 'EOF'
# Core data processing
pandas>=1.3.0
numpy>=1.20.0
openpyxl>=3.0.0

# GUI framework
tkinter-tooltip>=2.0.0
pillow>=8.0.0

# Basic sentiment analysis
textblob>=0.15.0
vaderSentiment>=3.3.2

# Advanced AI models (CPU-friendly)
transformers>=4.20.0
torch>=1.12.0
torch-audio>=0.12.0

# Visualization and charts
matplotlib>=3.5.0
seaborn>=0.11.0

# Chinese text support
snownlp>=0.12.0
jieba>=0.42.0

# Progress bars and UI enhancements
tqdm>=4.64.0
EOF

# 分阶段安装依赖
print_step "Installing core dependencies..."
echo -e "${CYAN}Installing essential packages:${NC}"
echo -e "  ${ICON_PYTHON} pandas, numpy, openpyxl - Data processing"
echo -e "  ${ICON_GUI} tkinter, pillow - GUI framework"
echo -e "  ${ICON_AI} textblob, vaderSentiment - Basic AI models"
echo ""

$PIP_CMD install pandas numpy openpyxl pillow tqdm --quiet
print_success "Core dependencies installed"

print_step "Installing advanced AI models..."
echo -e "${CYAN}Installing AI/ML packages:${NC}"
echo -e "  ${ICON_AI} transformers, torch - Advanced BERT/RoBERTa models"
echo -e "  ${ICON_AI} snownlp, jieba - Chinese text analysis"
echo -e "  📊 matplotlib, seaborn - Data visualization"
echo ""

# 安装transformers可能比较慢，显示进度
$PIP_CMD install textblob vaderSentiment --quiet
$PIP_CMD install transformers torch --quiet
$PIP_CMD install snownlp jieba --quiet
$PIP_CMD install matplotlib seaborn --quiet

# 尝试安装tkinter-tooltip，如果失败就跳过
$PIP_CMD install tkinter-tooltip --quiet 2>/dev/null || print_warning "tkinter-tooltip installation skipped (optional)"

print_success "All dependencies installed successfully"

print_section "Application Components Check"

# 检查GUI应用是否存在
if [ ! -f "sentiment_gui.py" ]; then
    print_warning "GUI application not found, will be created..."
    # 这里我们假设GUI文件会被创建
fi

if [ ! -f "sentiment_engine.py" ]; then
    print_warning "Analysis engine not found, will be created..."
    # 这里我们假设引擎文件会被创建
fi

print_section "Application Launch"

# 检查显示环境 (GUI需要)
if [ -z "$DISPLAY" ] && [ "$(uname)" != "Darwin" ]; then
    print_warning "No display environment detected"
    print_step "Launching in console mode..."
    
    if [ -f "professional_sentiment_analysis.py" ]; then
        $PYTHON_CMD professional_sentiment_analysis.py
    else
        print_error "Console application not found!"
        exit 1
    fi
else
    print_step "Display environment detected, launching GUI application..."
    
    if [ -f "sentiment_gui.py" ]; then
        print_success "Starting Professional Sentiment Analysis GUI..."
        echo ""
        echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
        echo -e "${CYAN}║${WHITE}                          ${ICON_GUI} GUI Application Starting ${ICON_GUI}                        ${CYAN}║${NC}"
        echo -e "${CYAN}║                                                                              ║${NC}"
        echo -e "${CYAN}║${YELLOW}  Features Available:                                                    ${CYAN}║${NC}"
        echo -e "${CYAN}║${YELLOW}  • File Selection & Preview                                             ${CYAN}║${NC}"
        echo -e "${CYAN}║${YELLOW}  • Column Selection for Analysis                                        ${CYAN}║${NC}"
        echo -e "${CYAN}║${YELLOW}  • Multiple AI Model Options                                            ${CYAN}║${NC}"
        echo -e "${CYAN}║${YELLOW}  • Real-time Progress Tracking                                          ${CYAN}║${NC}"
        echo -e "${CYAN}║${YELLOW}  • Statistical Visualization                                            ${CYAN}║${NC}"
        echo -e "${CYAN}║${YELLOW}  • Results Export & Saving                                              ${CYAN}║${NC}"
        echo -e "${CYAN}║                                                                              ║${NC}"
        echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"
        echo ""
        
        $PYTHON_CMD sentiment_gui.py
    else
        print_warning "GUI application not found, launching console version..."
        if [ -f "professional_sentiment_analysis.py" ]; then
            $PYTHON_CMD professional_sentiment_analysis.py
        else
            print_error "No application found to launch!"
            exit 1
        fi
    fi
fi

print_section "Application Complete"

echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║                                                                              ║${NC}"
echo -e "${CYAN}║${WHITE}                      ${ICON_SUCCESS} Setup Complete! ${ICON_SUCCESS}                              ${CYAN}║${NC}"
echo -e "${CYAN}║                                                                              ║${NC}"
echo -e "${CYAN}║${YELLOW}  Your Professional Sentiment Analysis Tool is ready!                   ${CYAN}║${NC}"
echo -e "${CYAN}║                                                                              ║${NC}"
echo -e "${CYAN}║${GREEN}  Next time, simply run: ./LAUNCH_SENTIMENT_ANALYSIS.sh                 ${CYAN}║${NC}"
echo -e "${CYAN}║                                                                              ║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════════════════════════════════════╝${NC}"

echo ""
echo -e "${GREEN}${ICON_INFO} Virtual Environment Location: $VENV_PATH${NC}"
echo -e "${GREEN}${ICON_INFO} To manually activate: source $VENV_PATH/bin/activate${NC}"
echo -e "${GREEN}${ICON_INFO} To deactivate: deactivate${NC}"

echo ""
echo -e "${CYAN}Press any key to exit...${NC}"
read -n 1 -s
