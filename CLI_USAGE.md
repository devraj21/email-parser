# Email Parser CLI - Complete Usage Guide

The Email Parser CLI provides direct access to all MCP server tools through command-line flags, mirroring the exact functionality available through the MCP server.

## 🚀 Quick Start

```bash
# Activate the virtual environment
source .venv/bin/activate

# Make CLI executable (one time)
chmod +x email_cli.py

# Run help to see all commands
python email_cli.py --help
```

## 📋 Available Commands

### 1. **parse-file** - Parse Single .msg File

Parse individual email files and extract structured content.

```bash
# Basic usage
python email_cli.py parse-file /path/to/email.msg

# JSON output
python email_cli.py parse-file email.msg --format json

# Detailed format with output to file
python email_cli.py parse-file email.msg --format detailed --output email_analysis.json

# Quiet mode (suppress progress messages)
python email_cli.py parse-file email.msg --format summary --quiet
```

**Output includes:**
- Subject, sender, recipients, sent date
- Email body text and HTML
- Attachments information
- Extracted entities (emails, phones, dates, URLs, money)
- Categories and correlation score
- Standardized format with summary, key points, action items

### 2. **parse-folder** - Parse Multiple .msg Files

Batch process all .msg files in a directory.

```bash
# Parse folder with summary
python email_cli.py parse-folder ./emails --format summary

# Detailed analysis of each email
python email_cli.py parse-folder ./emails --output-format detailed --format json

# Save results to file
python email_cli.py parse-folder ./emails --format json --output batch_results.json

# Summary format for emails, JSON output format
python email_cli.py parse-folder ./emails --output-format summary --format json
```

**Options:**
- `--output-format`: How to format individual emails (`summary`, `detailed`, `json`)
- `--format`: How to format the overall output (`summary`, `detailed`, `json`)
- `--output`: Save results to file
- `--quiet`: Suppress progress messages

### 3. **analyze-patterns** - Email Pattern Analysis

Analyze communication patterns across multiple emails.

```bash
# Category analysis (default)
python email_cli.py analyze-patterns ./emails

# Sender analysis
python email_cli.py analyze-patterns ./emails --type senders --format detailed

# Entity analysis
python email_cli.py analyze-patterns ./emails --type entities --format json

# Complete analysis
python email_cli.py analyze-patterns ./emails --type all --output complete_analysis.json
```

**Analysis Types:**
- `categories`: Email categorization patterns
- `senders`: Sender behavior analysis
- `entities`: Entity extraction statistics
- `all`: Complete pattern analysis

**Output includes:**
- Category distribution and statistics
- Sender frequency and patterns
- Entity extraction summaries
- Correlation analysis

### 4. **extract-entities** - Text Entity Extraction

Extract structured data from arbitrary text using email parser patterns.

```bash
# Basic entity extraction
python email_cli.py extract-entities --text "Contact john@example.com or call 555-123-4567"

# Auto-save to organized output directory
python email_cli.py extract-entities --text "Meeting on 03/15/2024 budget \$10,000" --auto-save

# Show regex patterns used
python email_cli.py extract-entities --text "Visit https://company.com" --show-patterns --auto-save

# JSON output with custom file
python email_cli.py extract-entities --text "Complex content..." --output custom_entities.json

# Quiet mode with auto-save
python email_cli.py extract-entities --text "Quick extraction..." --auto-save --quiet
```

**Extracted Entities:**
- Email addresses
- Phone numbers (various formats)
- Dates (MM/DD/YYYY, YYYY/MM/DD)
- URLs (HTTP/HTTPS)
- Monetary amounts ($, €, £, USD, EUR, GBP)

### 5. **server** - Start Server Modes

Launch different server transports for integration.

```bash
# Start MCP server for Claude Desktop
python email_cli.py server --mcp

# Start HTTP REST API server
python email_cli.py server --http --port 8000

# Start WebSocket server
python email_cli.py server --websocket --port 8001 --host 0.0.0.0

# Custom host and port
python email_cli.py server --http --host localhost --port 9000
```

**Server Types:**
- `--mcp`: Model Context Protocol server (stdio transport)
- `--http`: HTTP REST API server 
- `--websocket`: WebSocket server for real-time communication

### 6. **demo** - Run Demonstrations

Test functionality without .msg files.

```bash
# Run all demos
python email_cli.py demo

# Basic functionality demo only
python email_cli.py demo --type basic

# Quiet mode
python email_cli.py demo --type basic --quiet
```

## 🎯 Real-World Usage Examples

### Email Compliance Audit
```bash
# Parse all emails in compliance folder with auto-save
python email_cli.py parse-folder /path/to/compliance_emails --auto-save --format json

# Analyze sender patterns for compliance with organized output
python email_cli.py analyze-patterns /path/to/compliance_emails --type all --auto-save

# Custom compliance report
python email_cli.py analyze-patterns /path/to/compliance_emails --type all --output "output/reports/compliance_$(date +%Y%m%d).json"
```

### Customer Support Analysis
```bash
# Parse support tickets
python email_cli.py parse-folder ./support_tickets --output-format detailed --format summary

# Analyze categories and priorities
python email_cli.py analyze-patterns ./support_tickets --type categories --format detailed
```

### Entity Extraction for Data Mining
```bash
# Extract contact information from email text
python email_cli.py extract-entities --text "$(cat email_content.txt)" --show-patterns --format json
```

### Batch Processing Workflow
```bash
#!/bin/bash
# Process emails and generate reports

# Parse all emails
python email_cli.py parse-folder ./monthly_emails --format json --output monthly_emails.json

# Generate pattern analysis
python email_cli.py analyze-patterns ./monthly_emails --type all --output monthly_patterns.json

# Extract entities from specific text
python email_cli.py extract-entities --text "$(grep -h 'Budget:' ./monthly_emails/*.txt)" --output monthly_budgets.json

echo "Monthly email analysis complete!"
```

## 📊 Output Formats

### Summary Format
Human-readable overview with key information:
```
📧 Email: Project Update Meeting
   From: manager@company.com
   Categories: meeting, report
   Correlation: 0.823
```

### Detailed Format
Complete structured data in readable JSON:
```json
{
  "subject": "Project Update Meeting",
  "sender": "manager@company.com",
  "categories": ["meeting", "report"],
  "correlation_score": 0.823,
  "extracted_entities": {
    "emails": ["john@company.com"],
    "dates": ["03/15/2024"]
  }
}
```

### JSON Format
Raw structured data for programmatic use:
```json
{
  "message_id": "...",
  "subject": "...",
  "standardized_format": {
    "summary": "...",
    "key_points": [...],
    "action_items": [...]
  }
}
```

## 🔧 Integration Examples

### Python Script Integration
```python
import subprocess
import json

# Parse emails and get JSON results
result = subprocess.run([
    'python', 'email_cli.py', 'parse-folder', 
    './emails', '--format', 'json'
], capture_output=True, text=True)

data = json.loads(result.stdout)
print(f"Processed {data['processed']} emails")
```

### Shell Script Automation
```bash
#!/bin/bash
for dir in /path/to/email/folders/*; do
    if [ -d "$dir" ]; then
        echo "Processing $dir..."
        python email_cli.py parse-folder "$dir" --format json --output "${dir##*/}_analysis.json"
    fi
done
```

### Cron Job for Automated Processing
```bash
# Add to crontab: process emails daily at 2 AM
0 2 * * * cd /path/to/email-parser && source .venv/bin/activate && python email_cli.py parse-folder /new/emails --output daily_$(date +\%Y\%m\%d).json
```

## 🚨 Common Issues & Solutions

### 1. "extract_msg not installed"
```bash
source .venv/bin/activate
uv pip install extract-msg
```

### 2. "No .msg files found"
- Ensure files have `.msg` extension
- Check folder path is correct
- Files must be Outlook .msg format

### 3. "Permission denied"
```bash
chmod +x email_cli.py
```

### 4. Virtual environment not activated
```bash
source .venv/bin/activate
# Then run your command
```

## 📚 Advanced Usage

### Custom Entity Patterns
The CLI uses the same regex patterns as the MCP server. View patterns:
```bash
python email_cli.py extract-entities --text "sample" --show-patterns --format json
```

### Performance Optimization
For large folders:
```bash
# Use quiet mode and JSON output for faster processing
python email_cli.py parse-folder ./large_folder --quiet --format json --output results.json
```

### Integration with Other Tools
```bash
# Pipe results to jq for JSON manipulation
python email_cli.py parse-folder ./emails --format json | jq '.emails[].subject'

# Filter by categories
python email_cli.py parse-folder ./emails --format json | jq '.emails[] | select(.categories[] == "urgent")'
```

This CLI provides the complete functionality of the MCP server in a convenient command-line interface, perfect for batch processing, automation, and integration with other tools!