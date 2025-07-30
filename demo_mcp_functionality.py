#!/usr/bin/env python3
"""
Demo MCP Server Functionality
Shows how the MCP tools work with sample data
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def demo_mcp_tools():
    """Demonstrate MCP server tools with sample data"""
    from email_parser.mcp_server import EmailParserMCPServer
    
    print("🚀 Email Parser MCP Server - Tools Demo")
    print("=" * 50)
    
    # Initialize server
    server = EmailParserMCPServer("demo-server")
    print("✅ MCP Server initialized")
    
    # Demo 1: Entity extraction from text
    print("\n📧 Demo 1: Entity Extraction from Text")
    print("-" * 40)
    
    sample_texts = [
        "Hi Sarah, please contact john.doe@company.com or call +1-555-987-6543 for the project update. The deadline is 03/15/2024 and budget is $50,000.",
        "Meeting scheduled for 12/25/2024 at the main office. Contact info@meetings.com for details. Catering budget: €2,500.",
        "Urgent: Please review the contract at https://docs.company.com/contract123 and respond by 01/30/2024. Legal fees: $15,000."
    ]
    
    for i, text in enumerate(sample_texts, 1):
        print(f"\n📝 Sample {i}: {text[:60]}...")
        
        # Extract entities using the MCP tool function directly
        entities = server.parser._extract_entities(text)
        
        for entity_type, items in entities.items():
            if items:
                print(f"  🔍 {entity_type.title()}: {', '.join(items)}")
    
    # Demo 2: Email categorization and analysis
    print("\n\n🏷️ Demo 2: Email Categorization and Analysis")
    print("-" * 40)
    
    sample_emails = [
        {
            "subject": "URGENT: Server maintenance tonight",
            "body": "All services will be down from 11 PM to 3 AM for critical security updates. Please inform your teams.",
            "type": "IT Alert"
        },
        {
            "subject": "Q4 Sales Meeting - Action Required",
            "body": "Please review the attached Q4 report and schedule your 1:1 meetings by Friday. Great results this quarter!",
            "type": "Business Meeting"
        },
        {
            "subject": "Invoice #2024-001 - Payment Due",
            "body": "Your invoice for $12,500 is due by January 31st. Please remit payment or contact billing@vendor.com.",
            "type": "Financial"
        }
    ]
    
    for email in sample_emails:
        print(f"\n📋 {email['type']}: {email['subject']}")
        
        # Categorize email
        categories = server.parser._categorize_email(email['subject'], email['body'], [])
        print(f"  🏷️  Categories: {', '.join(categories)}")
        
        # Calculate correlation
        correlation = server.parser._calculate_correlation(email['subject'], email['body'], [])
        print(f"  📊 Correlation Score: {correlation:.3f}")
        
        # Extract entities
        combined_text = f"{email['subject']} {email['body']}"
        entities = server.parser._extract_entities(combined_text)
        for entity_type, items in entities.items():
            if items:
                print(f"  🔍 {entity_type.title()}: {', '.join(items)}")
    
    # Demo 3: Standardized format generation
    print("\n\n📄 Demo 3: Standardized Email Format")
    print("-" * 40)
    
    complex_email = {
        "subject": "Project Alpha - Contract Review & Team Meeting",
        "body": """
        Hi Team,
        
        Please review the attached contract for Project Alpha by Friday.
        
        Key points:
        • Contract value: $150,000
        • Deadline: March 15th, 2024
        • New team member: sarah.jones@company.com
        
        Action items:
        1. Legal review by Wednesday
        2. Schedule kick-off meeting
        3. Update project timeline
        
        The client meeting is scheduled for next Tuesday. Please call 555-PROJECT if you have questions.
        
        Thanks,
        Project Manager
        """,
        "attachments": [
            {"filename": "contract_alpha_v1.pdf", "size": 1024000}
        ]
    }
    
    print(f"📧 Subject: {complex_email['subject']}")
    
    # Generate standardized format
    entities = server.parser._extract_entities(f"{complex_email['subject']} {complex_email['body']}")
    standardized = server.parser._create_standardized_format(
        complex_email['subject'], 
        complex_email['body'], 
        complex_email['attachments'], 
        entities
    )
    
    print(f"\n📝 Summary: {standardized['summary']}")
    
    if standardized['key_points']:
        print(f"\n🔑 Key Points:")
        for point in standardized['key_points']:
            print(f"    • {point}")
    
    if standardized['action_items']:
        print(f"\n✅ Action Items:")
        for action in standardized['action_items']:
            print(f"    → {action}")
    
    if standardized['priority_indicators']:
        print(f"\n⚠️  Priority Indicators: {', '.join(standardized['priority_indicators'])}")
    
    print(f"\n📎 Attachments: {standardized['attachment_summary']}")
    
    # Demo 4: Business workflow simulation
    print("\n\n💼 Demo 4: Business Workflow Simulation")
    print("-" * 40)
    
    # Simulate a batch of emails for pattern analysis
    email_batch = [
        ("Meeting Request", "alice@company.com", ["meeting"], 0.8),
        ("Invoice Payment", "billing@vendor.com", ["invoice", "urgent"], 0.6),
        ("Project Update", "bob@company.com", ["report"], 0.9),
        ("Meeting Reminder", "calendar@company.com", ["meeting", "follow_up"], 0.7),
        ("Support Ticket", "support@helpdesk.com", ["support", "urgent"], 0.5),
        ("Contract Review", "legal@company.com", ["contract"], 0.8),
    ]
    
    print("📊 Email Pattern Analysis:")
    
    # Category analysis
    category_counts = {}
    total_correlation = 0
    
    for subject, sender, categories, correlation in email_batch:
        total_correlation += correlation
        for category in categories:
            category_counts[category] = category_counts.get(category, 0) + 1
    
    print(f"\n📈 Statistics:")
    print(f"  📧 Total emails: {len(email_batch)}")
    print(f"  📊 Average correlation: {total_correlation / len(email_batch):.3f}")
    print(f"  🏷️  Category distribution:")
    
    for category, count in sorted(category_counts.items(), key=lambda x: x[1], reverse=True):
        percentage = (count / len(email_batch)) * 100
        print(f"    {category}: {count} emails ({percentage:.1f}%)")
    
    print("\n✅ MCP Server Demo Complete!")
    print("\n🚀 Ready for Integration:")
    print("  • Claude Desktop: Use stdio transport")
    print("  • Web Apps: Use HTTP API transport") 
    print("  • Real-time Apps: Use WebSocket transport")
    print("  • Python Apps: Import EmailParserMCPServer directly")

if __name__ == "__main__":
    asyncio.run(demo_mcp_tools())