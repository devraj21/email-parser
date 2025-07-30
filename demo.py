#!/usr/bin/env python3
"""
Complete Email Parser Demo
Shows all capabilities of the email parsing system
"""

import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from email_parser.parser import EmailParser, EmailContent
import json
from datetime import datetime

def print_header(title):
    """Print a formatted header"""
    print(f"\n{'='*60}")
    print(f"🚀 {title}")
    print(f"{'='*60}")

def print_section(title):
    """Print a formatted section"""
    print(f"\n📋 {title}")
    print("-" * 40)

def demo_entity_extraction():
    """Demo entity extraction capabilities"""
    print_header("Entity Extraction Demo")
    
    parser = EmailParser()
    
    sample_texts = {
        "Business Email": """
        Dear Team,
        
        Please contact sarah.johnson@company.com or call +1-555-987-6543 for urgent matters.
        The project deadline is 03/15/2024 and the budget is $75,000.
        
        Additional resources: https://project.company.com/docs
        Alternative contact: (555) 123-4567
        Secondary budget: €25,000
        
        Best regards,
        John
        """,
        
        "Meeting Invitation": """
        Subject: Weekly Team Meeting - March 15th
        
        Hi everyone,
        
        Our weekly meeting is scheduled for 03/15/2024 at 2:00 PM.
        Please review the agenda at https://meetings.company.com/agenda/123
        
        Conference line: 1-800-555-0199
        Meeting room budget: $500 for refreshments
        
        Contact admin@company.com for any issues.
        """,
        
        "Invoice Email": """
        Invoice #INV-2024-001
        
        Amount due: $12,500.00
        Due date: 12/31/2024
        
        Questions? Call our billing department at (555) 987-1234
        Or email billing@vendor.com
        
        Payment portal: https://pay.vendor.com/invoice/001
        Late fee: $150.00 after due date
        """
    }
    
    for email_type, text in sample_texts.items():
        print_section(f"{email_type} Analysis")
        
        entities = parser._extract_entities(text)
        
        print(f"📧 Sample: {text[:100]}...")
        print()
        
        for entity_type, items in entities.items():
            if items:
                print(f"  🔍 {entity_type.title()}: {', '.join(items)}")
        
        # Show correlation and categorization
        lines = text.strip().split('\n')
        subject = lines[0] if lines else ""
        body = '\n'.join(lines[1:]) if len(lines) > 1 else text
        
        correlation = parser._calculate_correlation(subject, body, [])
        categories = parser._categorize_email(subject, body, [])
        
        print(f"  📊 Correlation Score: {correlation:.3f}")
        print(f"  🏷️  Categories: {', '.join(categories)}")

def demo_email_standardization():
    """Demo email content standardization"""
    print_header("Email Content Standardization Demo")
    
    parser = EmailParser()
    
    sample_emails = [
        {
            "subject": "URGENT: Server maintenance window tonight",
            "body": """
            Team,
            
            We have an urgent server maintenance scheduled for tonight from 11 PM to 3 AM.
            
            Key points:
            • All services will be unavailable
            • Database backup completed
            • Rollback plan is ready
            
            Action items:
            1. Please inform your clients about the downtime
            2. Monitor the #ops channel for updates
            3. Be available for emergency calls
            
            The maintenance is critical for security updates.
            
            Questions? Call the ops team at 555-0123 or email ops@company.com
            
            Thanks,
            IT Team
            """,
            "attachments": [
                {"filename": "maintenance_plan.pdf", "size": 2048000}
            ]
        },
        {
            "subject": "Q4 Sales Report - Action Required",
            "body": """
            Hi Sales Team,
            
            Please find the Q4 sales report attached. We exceeded our target by 15%!
            
            Important notes:
            - Revenue: $2.5M (target was $2.2M)
            - New clients: 47
            - Renewal rate: 94%
            
            Next steps:
            Please review your individual performance metrics and schedule 1:1s with your manager by Friday.
            
            The board presentation is scheduled for January 15th, 2024.
            
            Great work everyone!
            
            Best,
            Sarah (sarah@company.com)
            """,
            "attachments": [
                {"filename": "Q4_sales_report.xlsx", "size": 512000},
                {"filename": "individual_metrics.pdf", "size": 256000}
            ]
        }
    ]
    
    for i, email_data in enumerate(sample_emails, 1):
        print_section(f"Email {i}: {email_data['subject']}")
        
        subject = email_data["subject"]
        body = email_data["body"]
        attachments = email_data.get("attachments", [])
        
        # Extract entities
        combined_text = f"{subject} {body}"
        entities = parser._extract_entities(combined_text)
        
        # Calculate correlation
        correlation = parser._calculate_correlation(subject, body, attachments)
        
        # Categorize
        categories = parser._categorize_email(subject, body, attachments)
        
        # Create standardized format
        standardized = parser._create_standardized_format(subject, body, attachments, entities)
        
        print(f"📧 Original Subject: {subject}")
        print(f"📝 Summary: {standardized['summary']}")
        print(f"📊 Correlation Score: {correlation:.3f}")
        print(f"🏷️  Categories: {', '.join(categories)}")
        
        if standardized['key_points']:
            print(f"🔑 Key Points:")
            for point in standardized['key_points']:
                print(f"    • {point}")
        
        if standardized['action_items']:
            print(f"✅ Action Items:")
            for action in standardized['action_items']:
                print(f"    → {action}")
        
        if standardized['priority_indicators']:
            print(f"⚠️  Priority Indicators: {', '.join(standardized['priority_indicators'])}")
        
        print(f"📎 Attachments: {standardized['attachment_summary']}")
        
        if any(entities.values()):
            print(f"🔍 Extracted Entities:")
            for entity_type, items in entities.items():
                if items:
                    print(f"    {entity_type}: {', '.join(items)}")

def demo_pattern_analysis():
    """Demo pattern analysis across multiple emails"""
    print_header("Pattern Analysis Demo")
    
    parser = EmailParser()
    
    # Simulate multiple emails
    emails_data = [
        ("Meeting Request", "john@company.com", ["meeting", "has_attachments"], 0.8),
        ("Invoice Payment", "billing@vendor.com", ["invoice", "urgent"], 0.6),
        ("Project Update", "sarah@company.com", ["report", "has_attachments"], 0.9),
        ("Meeting Reminder", "calendar@company.com", ["meeting", "follow_up"], 0.7),
        ("Support Ticket", "support@helpdesk.com", ["support", "urgent"], 0.5),
        ("Contract Review", "legal@company.com", ["contract", "has_attachments"], 0.8),
        ("Weekly Report", "manager@company.com", ["report"], 0.9),
    ]
    
    print_section("Sender Analysis")
    sender_stats = {}
    for subject, sender, categories, correlation in emails_data:
        if sender not in sender_stats:
            sender_stats[sender] = {"count": 0, "avg_correlation": 0, "categories": set()}
        
        sender_stats[sender]["count"] += 1
        sender_stats[sender]["avg_correlation"] += correlation
        sender_stats[sender]["categories"].update(categories)
    
    for sender, stats in sender_stats.items():
        stats["avg_correlation"] = stats["avg_correlation"] / stats["count"]
        print(f"  📧 {sender}")
        print(f"     Emails: {stats['count']}")
        print(f"     Avg Correlation: {stats['avg_correlation']:.3f}")
        print(f"     Categories: {', '.join(list(stats['categories']))}")
        print()
    
    print_section("Category Distribution")
    category_stats = {}
    for subject, sender, categories, correlation in emails_data:
        for category in categories:
            if category not in category_stats:
                category_stats[category] = {"count": 0, "avg_correlation": 0}
            category_stats[category]["count"] += 1
            category_stats[category]["avg_correlation"] += correlation
    
    for category, stats in category_stats.items():
        stats["avg_correlation"] = stats["avg_correlation"] / stats["count"]
        print(f"  🏷️  {category}: {stats['count']} emails (avg correlation: {stats['avg_correlation']:.3f})")

def demo_mcp_capabilities():
    """Demo MCP server capabilities (simulated)"""
    print_header("MCP Server Capabilities Demo")
    
    print("""
🔧 MCP Server Tools Available:

1. 📁 parse_email_folder
   - Batch process all .msg files in a directory
   - Output formats: JSON, summary, detailed
   - Example: Process 100+ emails in seconds

2. 📧 parse_single_email  
   - Detailed analysis of individual emails
   - Includes raw content option
   - Perfect for debugging specific emails

3. 📊 analyze_email_patterns
   - Sender behavior analysis
   - Category distribution
   - Entity extraction statistics
   - Correlation analysis across email sets

🚀 Automation Scenarios:

• Daily email processing pipeline
• Customer communication analysis
• Compliance and audit trail creation
• Email classification for CRM systems
• Automatic priority detection
• Content standardization for reporting
    """)

def demo_integration_examples():
    """Show integration examples"""
    print_header("Integration Examples")
    
    parser = EmailParser()
    
    # Example: Create a structured output for API integration
    sample_email = {
        "subject": "Contract Amendment - ABC Corp",
        "body": """
        Hi Legal Team,
        
        Please review the attached contract amendment for ABC Corp.
        Deadline: March 20th, 2024
        Contract value: $150,000
        
        Key changes:
        • Extended term by 6 months
        • Updated payment schedule
        • Added new deliverables
        
        Please have this reviewed and signed by Friday.
        
        Contact: legal@abccorp.com or (555) 987-6543
        """,
        "attachments": [{"filename": "contract_amendment_v2.pdf", "size": 1024000}]
    }
    
    # Process the email
    entities = parser._extract_entities(f"{sample_email['subject']} {sample_email['body']}")
    correlation = parser._calculate_correlation(
        sample_email["subject"], 
        sample_email["body"], 
        sample_email["attachments"]
    )
    categories = parser._categorize_email(
        sample_email["subject"], 
        sample_email["body"], 
        sample_email["attachments"]
    )
    standardized = parser._create_standardized_format(
        sample_email["subject"], 
        sample_email["body"], 
        sample_email["attachments"], 
        entities
    )
    
    # Create API-ready output
    api_output = {
        "email_id": "email_001",
        "processed_at": datetime.now().isoformat(),
        "classification": {
            "categories": categories,
            "priority_score": correlation,
            "priority_indicators": standardized["priority_indicators"]
        },
        "content": {
            "summary": standardized["summary"],
            "key_points": standardized["key_points"],
            "action_items": standardized["action_items"]
        },
        "entities": entities,
        "metadata": {
            "attachment_count": len(sample_email["attachments"]),
            "correlation_score": correlation
        }
    }
    
    print_section("API Integration Example")
    print("📤 Structured Output for CRM/API Integration:")
    print(json.dumps(api_output, indent=2, default=str))
    
    print_section("Database Schema Example")
    print("""
📋 Suggested Database Tables:

emails:
  - id, subject, sender, recipients, sent_date
  - body_text, body_html, correlation_score
  - created_at, processed_at

email_categories:
  - email_id, category_name

email_entities:
  - email_id, entity_type, entity_value

email_attachments:
  - email_id, filename, size, content_type

email_actions:
  - email_id, action_text, priority, due_date
    """)

def main():
    """Run the complete demo"""
    print_header("Email Parsing MCP Server - Complete Demo")
    print("""
🎯 This demo showcases the full capabilities of the email parsing system:
   • Entity extraction from email content
   • Content standardization and summarization  
   • Pattern analysis across multiple emails
   • MCP server automation capabilities
   • Integration examples for real-world use
    """)
    
    try:
        demo_entity_extraction()
        demo_email_standardization()
        demo_pattern_analysis()
        demo_mcp_capabilities()
        demo_integration_examples()
        
        print_header("Demo Complete!")
        print("""
✅ All demos completed successfully!

🚀 Your email parsing system is ready for:
   • Processing .msg files from Outlook
   • Automating email content analysis
   • Integrating with existing systems
   • Building email intelligence pipelines

📁 Next Steps:
   1. Add your .msg files to examples/sample_emails/
   2. Run: python -m src.email_parser.main
   3. Customize entity patterns for your use case
   4. Build MCP server integrations
   5. Create automated workflows

💡 Tips:
   • The system works without .msg files for testing
   • All patterns can be customized in parser.py
   • Add more categories based on your email types
   • Consider adding ML-based classification for advanced use cases
        """)
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()