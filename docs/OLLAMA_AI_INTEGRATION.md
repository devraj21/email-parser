# Ollama Phi3 AI Integration Guide

Your Email Parser now includes powerful AI integration with Ollama Phi3 for advanced email analysis, categorization, sentiment analysis, and summarization.

## 🧠 AI Features

### **Smart Email Analysis**
- **AI-powered summarization** using Phi3 language model
- **Intelligent categorization** beyond keyword matching
- **Sentiment analysis** (positive, negative, neutral, concerned)
- **Priority scoring** with AI-driven urgency detection
- **Action item extraction** with natural language understanding
- **Key insight identification** for business intelligence

### **Enhanced Capabilities**
- **Context-aware categorization**: Understanding email intent and purpose
- **Semantic analysis**: Beyond simple pattern matching
- **Business intelligence**: Extract actionable insights from email content
- **Sentiment tracking**: Monitor communication tone and mood
- **Priority detection**: AI-driven urgency assessment

## 🚀 Setup Instructions

### **1. Install Ollama**
```bash
# macOS (recommended)
curl -fsSL https://ollama.com/install.sh | sh

# Alternative: Download from https://ollama.com
```

### **2. Install Phi3 Model**
```bash
# Pull the Phi3 model (this may take a few minutes)
ollama pull phi3

# Verify installation
ollama list
```

### **3. Install AI Dependencies**
```bash
# Activate your virtual environment
source .venv/bin/activate

# Install AI dependencies
uv pip install ".[ai]"
```

### **4. Start Ollama Service**
```bash
# Start Ollama in the background
ollama serve

# Or check if it's already running
curl http://localhost:11434/api/tags
```

## 🤖 AI-Powered Commands

### **AI Analyze File**
Perform comprehensive AI analysis of a single email:

```bash
# Basic AI analysis
python email_cli.py ai-analyze file email.msg

# Detailed JSON output with auto-save
python email_cli.py ai-analyze file email.msg --format json --auto-save

# Compare traditional vs AI analysis
python email_cli.py ai-analyze file email.msg --format detailed
```

**AI Analysis Output:**
- **Summary**: AI-generated concise summary
- **Categories**: Intelligent categorization
- **Sentiment**: Emotional tone analysis
- **Priority Score**: 0.0-1.0 urgency rating
- **Key Insights**: Important points extracted
- **Action Items**: Tasks and requests identified
- **Traditional Analysis**: Comparison with regex-based parsing

### **AI Text Analysis**
Analyze arbitrary text with AI:

```bash
# Analyze email content without .msg file
python email_cli.py ai-analyze text --text "Urgent: Need budget approval for Q4 project by Friday. Contact CFO immediately."

# With auto-save
python email_cli.py ai-analyze text --text "Your sample text here" --auto-save --format json
```

### **AI Smart Categorization**
Intelligent batch processing with AI insights:

```bash
# Smart categorize entire folder
python email_cli.py ai-analyze categorize ./emails --format detailed

# Generate AI-powered reports
python email_cli.py ai-analyze categorize ./emails --auto-save --format json --quiet
```

**Smart Categorization Output:**
- **AI Categories**: Semantic categorization
- **Sentiment Distribution**: Mood analysis across emails
- **Priority Distribution**: Urgency breakdown (low/medium/high/critical)
- **Individual Summaries**: AI summary for each email
- **Batch Insights**: Patterns and trends identified

## 🎯 Usage Examples

### **Example 1: AI Email Analysis**
```bash
source .venv/bin/activate

# Ensure Ollama is running
ollama serve &

# Analyze a single email with AI
python email_cli.py ai-analyze file important_email.msg --format json

# Sample output:
{
  "file": "important_email.msg",
  "traditional_analysis": {
    "categories": ["meeting", "urgent"],
    "correlation_score": 0.75
  },
  "ai_analysis": {
    "summary": "Budget approval meeting scheduled for Friday with stakeholders to review Q4 project funding.",
    "categories": ["meeting", "urgent", "financial"],
    "sentiment": "concerned",
    "priority_score": 0.85,
    "key_insights": [
      "Time-sensitive budget decision required",
      "Multiple stakeholder involvement needed"
    ],
    "action_items": [
      "Prepare budget presentation materials",
      "Confirm attendee availability"
    ],
    "model_used": "phi3"
  }
}
```

### **Example 2: Batch AI Processing**
```bash
# Process customer support emails with AI
python email_cli.py ai-analyze categorize ./support_emails --auto-save

# Output saved to: output/analysis/ai_categorize_support_emails_20241230_143022.json
{
  "total_files": 25,
  "processed": 24,
  "ai_categories": {
    "support": 15,
    "urgent": 8,
    "complaint": 5,
    "positive": 3
  },
  "sentiment_distribution": {
    "neutral": 12,
    "concerned": 7,
    "negative": 4,
    "positive": 1
  },
  "priority_distribution": {
    "high": 8,
    "medium": 12,
    "low": 4,
    "critical": 0
  }
}
```

### **Example 3: Text Analysis Without .msg Files**
```bash
# Analyze email content directly
python email_cli.py ai-analyze text --text "
Subject: Quarterly Review Meeting

Hi team, we need to schedule our Q4 review meeting. Please send me your availability for next week. We'll be discussing:
- Budget performance
- Team achievements
- 2024 planning

This is high priority as we need to submit our report by month-end.
" --format detailed --auto-save
```

## 🔧 Integration Options

### **1. MCP Server with AI**
Start the MCP server to access AI tools through Claude Desktop:

```bash
# Start MCP server with AI capabilities
python email_cli.py server --mcp

# Available AI tools in Claude:
# - ai_analyze_email_file
# - ai_analyze_text  
# - ai_smart_categorize_folder
```

**Claude Desktop Configuration:**
```json
{
  "mcpServers": {
    "email-parser-ai": {
      "command": "python",
      "args": ["-m", "src.email_parser.main", "--mcp"],
      "cwd": "/path/to/email-parser"
    }
  }
}
```

### **2. HTTP API with AI**
```bash
# Start HTTP server
python email_cli.py server --http --port 8000

# AI endpoints available:
# POST /api/ai/analyze-file
# POST /api/ai/analyze-text
# POST /api/ai/categorize-folder
```

### **3. Python Integration**
```python
#!/usr/bin/env python3
import sys
from pathlib import Path
sys.path.insert(0, str(Path('.') / 'src'))

from email_parser.ai_integration import create_ai_analyzer

# Create AI analyzer
ai_analyzer = create_ai_analyzer("phi3")

if ai_analyzer and ai_analyzer.is_available():
    # Analyze text directly
    result = ai_analyzer.analyze_text("Your email content here")
    print(f"AI Summary: {result['summary']}")
    print(f"Sentiment: {result['sentiment']}")
    print(f"Priority: {result['priority_score']}")
```

## ⚡ Performance & Hardware Requirements

### **System Requirements**
- **RAM**: 8GB minimum, 16GB recommended for Phi3
- **Storage**: 2-4GB for Phi3 model
- **CPU**: Modern multi-core processor recommended
- **macOS**: M1/M2 Macs work excellently with Ollama

### **Performance Optimization**
```bash
# Check Ollama model info
ollama show phi3

# Monitor GPU usage (if available)
ollama run phi3 --verbose

# Use smaller model for faster processing
ollama pull phi3:mini
```

### **Batch Processing Tips**
```bash
# Process large folders efficiently
python email_cli.py ai-analyze categorize ./large_folder --quiet --auto-save

# Monitor progress
tail -f logs/email_parser.log
```

## 🛠️ Troubleshooting

### **Common Issues**

**1. "AI analysis not available"**
```bash
# Check if Ollama is running
curl http://localhost:11434/api/tags

# Start Ollama if not running
ollama serve

# Verify Phi3 model is installed
ollama list | grep phi3
```

**2. "Model not found"**
```bash
# Install Phi3 model
ollama pull phi3

# Or try the mini version for faster processing
ollama pull phi3:mini
```

**3. Slow processing**
```bash
# Use quiet mode for batch processing
python email_cli.py ai-analyze categorize ./emails --quiet

# Monitor system resources
htop

# Consider using phi3:mini for faster results
```

**4. Memory issues**
```bash
# Check available memory
free -h

# Restart Ollama to clear memory
pkill ollama && ollama serve
```

### **Configuration Options**

Create a config file for custom AI settings:
```yaml
# config/ai_settings.yaml
ai:
  model: "phi3"
  host: "http://localhost:11434"
  temperature: 0.3
  max_tokens: 500
  timeout: 30
```

## 🎨 Advanced Usage

### **Custom Prompts**
Modify prompts in `src/email_parser/ai_integration.py` for specialized analysis:

```python
# Example: Legal document analysis
def _analyze_legal_content(self, content: str) -> List[str]:
    prompt = f"""
    Analyze this legal email for:
    - Contract references
    - Compliance requirements  
    - Risk indicators
    - Action deadlines
    
    {content}
    """
```

### **Multiple Model Support**
```bash
# Install different models
ollama pull llama2
ollama pull mistral

# Use different model
python email_cli.py ai-analyze text --text "sample" --model llama2
```

### **Automation Workflows**
```bash
#!/bin/bash
# daily_ai_analysis.sh

DATE=$(date +%Y%m%d)
INBOX="/path/to/daily/emails"

echo "Running daily AI analysis for $DATE"

# AI categorization
python email_cli.py ai-analyze categorize "$INBOX" \
  --auto-save --quiet --format json

# Generate summary report
python generate_ai_summary.py "$DATE"

echo "AI analysis complete!"
```

This AI integration transforms your email parser from a simple extraction tool into an intelligent email analysis platform, providing deep insights and automation capabilities powered by local AI models!

## 🚀 Next Steps

1. **Install Ollama and Phi3**: Follow setup instructions above
2. **Test AI functionality**: Run sample commands to verify integration
3. **Explore AI analysis**: Try different email types and content
4. **Integrate with workflows**: Use AI tools in your email processing pipelines
5. **Customize prompts**: Adapt AI analysis for your specific use cases

The AI integration provides powerful local processing without cloud dependencies, perfect for sensitive email analysis and enterprise use cases!