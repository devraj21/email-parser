# Email Parser - Output Organization Guide

The Email Parser CLI now includes automatic output organization with timestamped files for better workflow management.

## 📁 Output Directory Structure

```
output/
├── emails/          # Single email parsing results
├── analysis/        # Folder analysis and pattern reports  
├── entities/        # Entity extraction results
├── reports/         # Custom reports and summaries
└── README.md        # Documentation
```

## 🔄 Auto-Save Feature

Use the `--auto-save` flag to automatically save results with organized naming:

### **Entity Extraction**
```bash
# Automatically saves to output/entities/entities_YYYYMMDD_HHMMSS.json
python email_cli.py extract-entities --text "Contact john@company.com" --auto-save

# Example output file: output/entities/entities_20241230_143022.json
```

### **Single Email Parsing**
```bash
# Automatically saves to output/emails/EMAIL_NAME_YYYYMMDD_HHMMSS.json  
python email_cli.py parse-file email.msg --auto-save --format json

# Example output file: output/emails/important_email_20241230_143055.json
```

### **Folder Analysis**
```bash
# Automatically saves to output/analysis/folder_FOLDER_NAME_YYYYMMDD_HHMMSS.json
python email_cli.py parse-folder ./emails --auto-save --format json

# Example output file: output/analysis/folder_emails_20241230_143112.json
```

### **Pattern Analysis**
```bash
# Automatically saves to output/analysis/patterns_TYPE_YYYYMMDD_HHMMSS.json
python email_cli.py analyze-patterns ./emails --type all --auto-save

# Example output file: output/analysis/patterns_all_20241230_143155.json
```

## 🎯 Usage Examples

### **Quick Entity Extraction with Auto-Save**
```bash
source .venv/bin/activate

# Extract and save entities automatically
python email_cli.py extract-entities \
  --text "Meeting with sarah@company.com on 03/15/2024. Budget: $50,000" \
  --auto-save \
  --format json
  
# Output automatically saved to output/entities/entities_20241230_143022.json
```

### **Batch Processing with Organization**
```bash
# Process multiple email folders with auto-save
for folder in /path/to/email/folders/*; do
  echo "Processing $folder..."
  python email_cli.py parse-folder "$folder" --auto-save --format json --quiet
done

# Results organized in output/analysis/ with timestamps
```

### **Custom Path vs Auto-Save**
```bash
# Custom path (you specify location)
python email_cli.py parse-file email.msg --output /custom/path/result.json

# Auto-save (automatic organization)
python email_cli.py parse-file email.msg --auto-save

# Both (display + save)
python email_cli.py parse-file email.msg --auto-save --format summary
```

## 📊 File Naming Convention

### **Automatic Naming Patterns**
- **Entities**: `entities_YYYYMMDD_HHMMSS.json`
- **Single emails**: `EMAIL_NAME_YYYYMMDD_HHMMSS.json`
- **Folder analysis**: `folder_FOLDER_NAME_YYYYMMDD_HHMMSS.json`
- **Pattern analysis**: `patterns_TYPE_YYYYMMDD_HHMMSS.json`

### **Timestamp Format**
- Format: `YYYYMMDD_HHMMSS`
- Example: `20241230_143022` = December 30, 2024 at 14:30:22

### **Name Sanitization**
- Special characters replaced with underscores
- Spaces converted to underscores
- File extensions preserved

## 🔍 Finding Your Results

### **Latest Files**
```bash
# Find latest entity extraction
ls -t output/entities/*.json | head -1

# Find latest folder analysis  
ls -t output/analysis/folder_*.json | head -1

# Find latest pattern analysis
ls -t output/analysis/patterns_*.json | head -1
```

### **Search by Date**
```bash
# Find files from today
find output/ -name "*$(date +%Y%m%d)*" -type f

# Find files from specific date
find output/ -name "*20241230*" -type f

# Find files from last hour
find output/ -newermt "1 hour ago" -type f
```

### **Search by Type**
```bash
# All entity extractions
ls output/entities/

# All email parsing results
ls output/emails/

# All analysis reports
ls output/analysis/
```

## 🛠️ Integration Examples

### **Monitoring Script**
```bash
#!/bin/bash
# monitor_outputs.sh - Watch for new results

echo "📊 Latest Email Parser Results:"
echo "================================"

echo "🔍 Latest Entity Extraction:"
ls -t output/entities/*.json 2>/dev/null | head -1 || echo "  No results yet"

echo "📧 Latest Email Analysis:"
ls -t output/emails/*.json 2>/dev/null | head -1 || echo "  No results yet"  

echo "📊 Latest Pattern Analysis:"
ls -t output/analysis/*.json 2>/dev/null | head -1 || echo "  No results yet"

echo "📈 Total Results: $(find output/ -name "*.json" | wc -l)"
```

### **Automated Reporting**
```bash
#!/bin/bash
# daily_report.sh - Generate daily summary

DATE=$(date +%Y%m%d)
REPORT_FILE="output/reports/daily_summary_${DATE}.json"

echo "Generating daily report for $DATE..."

# Count results by type
ENTITIES=$(find output/entities/ -name "*${DATE}*" | wc -l)
EMAILS=$(find output/emails/ -name "*${DATE}*" | wc -l)  
ANALYSIS=$(find output/analysis/ -name "*${DATE}*" | wc -l)

# Create summary JSON
cat > "$REPORT_FILE" << EOF
{
  "date": "$DATE",
  "summary": {
    "entity_extractions": $ENTITIES,
    "email_analyses": $EMAILS,
    "pattern_analyses": $ANALYSIS,
    "total_results": $((ENTITIES + EMAILS + ANALYSIS))
  },
  "generated_at": "$(date -Iseconds)"
}
EOF

echo "Daily report saved to: $REPORT_FILE"
```

### **Cleanup Script**
```bash
#!/bin/bash
# cleanup_old_results.sh - Archive old results

# Archive files older than 30 days
find output/ -name "*.json" -mtime +30 -exec gzip {} \;

# Move archived files to archive directory
mkdir -p output/archive
find output/ -name "*.json.gz" -exec mv {} output/archive/ \;

echo "Cleanup complete. Archived $(ls output/archive/*.gz 2>/dev/null | wc -l) files."
```

## 🎨 Integration with Analysis Tools

### **jq Integration**
```bash
# Extract all email addresses from entity results
find output/entities/ -name "*.json" -exec jq -r '.entities.emails[]' {} \; | sort -u

# Get correlation scores from email analyses
find output/emails/ -name "*.json" -exec jq -r '.correlation_score' {} \; | sort -n

# Summary statistics from pattern analyses
find output/analysis/ -name "patterns_*.json" -exec jq -r '.processed_emails' {} \; | \
  awk '{sum+=$1} END {print "Total emails processed:", sum}'
```

### **Python Integration**
```python
#!/usr/bin/env python3
# analyze_results.py - Analyze saved results

import json
import glob
from pathlib import Path
from datetime import datetime

def analyze_daily_results():
    """Analyze all results from today"""
    today = datetime.now().strftime("%Y%m%d")
    
    # Find all JSON files from today
    pattern = f"output/**/*{today}*.json"
    files = glob.glob(pattern, recursive=True)
    
    print(f"📊 Analysis for {today}")
    print(f"Total files: {len(files)}")
    
    # Categorize results
    categories = {"entities": 0, "emails": 0, "analysis": 0, "reports": 0}
    
    for file_path in files:
        path = Path(file_path)
        category = path.parent.name
        if category in categories:
            categories[category] += 1
    
    for category, count in categories.items():
        print(f"{category.title()}: {count} files")

if __name__ == "__main__":
    analyze_daily_results()
```

## 🚀 Best Practices

### **1. Use Auto-Save for Automation**
```bash
# Good: Automatic organization
python email_cli.py parse-folder ./emails --auto-save --format json --quiet

# Less organized: Manual paths  
python email_cli.py parse-folder ./emails --output random_name.json
```

### **2. Combine with Custom Naming**
```bash
# For specific projects, use descriptive custom paths
python email_cli.py analyze-patterns ./customer_emails \
  --type all \
  --output "output/reports/customer_analysis_$(date +%Y%m%d).json"
```

### **3. Archive Regularly**
```bash
# Keep output directory manageable
find output/ -name "*.json" -mtime +7 -exec gzip {} \;
```

### **4. Monitor Disk Usage**
```bash
# Check output directory size
du -sh output/
```

This organized approach makes it easy to track results, integrate with other tools, and maintain clean workflows for email processing tasks!