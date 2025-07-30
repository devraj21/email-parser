#!/usr/bin/env python3
"""
Email Parser - Command Line Usage
Parse single .msg files or entire folders
"""

import argparse
import json
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from email_parser.parser import EmailParser

def parse_single_file(file_path, output_format="summary"):
    """Parse a single .msg file"""
    parser = EmailParser()
    email_path = Path(file_path)
    
    if not email_path.exists():
        print(f"❌ File not found: {file_path}")
        return None
    
    if not email_path.suffix.lower() == '.msg':
        print(f"❌ Not a .msg file: {file_path}")
        return None
    
    print(f"📧 Parsing: {email_path.name}")
    email_content = parser.parse_msg_file(email_path)
    
    if not email_content:
        print("❌ Failed to parse email")
        return None
    
    if output_format == "summary":
        result = {
            "file": email_path.name,
            "subject": email_content.subject,
            "sender": email_content.sender,
            "recipients": email_content.recipients,
            "sent_date": email_content.sent_date.isoformat() if email_content.sent_date else None,
            "categories": email_content.categories,
            "correlation_score": email_content.correlation_score,
            "summary": email_content.standardized_format.get("summary", ""),
            "entities": email_content.extracted_entities
        }
    else:  # detailed
        result = {
            "file": email_path.name,
            "message_id": email_content.message_id,
            "subject": email_content.subject,
            "sender": email_content.sender,
            "recipients": email_content.recipients,
            "cc_recipients": email_content.cc_recipients,
            "bcc_recipients": email_content.bcc_recipients,
            "sent_date": email_content.sent_date.isoformat() if email_content.sent_date else None,
            "body_text": email_content.body_text,
            "attachments": email_content.attachments,
            "categories": email_content.categories,
            "correlation_score": email_content.correlation_score,
            "extracted_entities": email_content.extracted_entities,
            "standardized_format": email_content.standardized_format
        }
    
    return result

def parse_folder(folder_path, output_format="summary"):
    """Parse all .msg files in a folder"""
    parser = EmailParser()
    folder = Path(folder_path)
    
    if not folder.exists() or not folder.is_dir():
        print(f"❌ Folder not found: {folder_path}")
        return None
    
    # Find all .msg files
    msg_files = list(folder.glob("*.msg"))
    if not msg_files:
        print(f"❌ No .msg files found in: {folder_path}")
        return None
    
    print(f"📁 Found {len(msg_files)} .msg files in {folder.name}")
    
    results = {
        "folder": str(folder),
        "total_files": len(msg_files),
        "processed": 0,
        "failed": 0,
        "emails": []
    }
    
    for msg_file in msg_files:
        print(f"  📧 Processing: {msg_file.name}")
        
        try:
            email_content = parser.parse_msg_file(msg_file)
            
            if email_content:
                if output_format == "summary":
                    email_result = {
                        "file": msg_file.name,
                        "subject": email_content.subject,
                        "sender": email_content.sender,
                        "categories": email_content.categories,
                        "correlation_score": email_content.correlation_score,
                        "summary": email_content.standardized_format.get("summary", "")
                    }
                else:  # detailed
                    email_result = {
                        "file": msg_file.name,
                        "message_id": email_content.message_id,
                        "subject": email_content.subject,
                        "sender": email_content.sender,
                        "recipients": email_content.recipients,
                        "sent_date": email_content.sent_date.isoformat() if email_content.sent_date else None,
                        "body_text": email_content.body_text[:500] + "..." if len(email_content.body_text) > 500 else email_content.body_text,
                        "categories": email_content.categories,
                        "correlation_score": email_content.correlation_score,
                        "extracted_entities": email_content.extracted_entities,
                        "key_points": email_content.standardized_format.get("key_points", []),
                        "action_items": email_content.standardized_format.get("action_items", [])
                    }
                
                results["emails"].append(email_result)
                results["processed"] += 1
                print(f"    ✅ Success: {email_content.subject[:50]}...")
            else:
                results["failed"] += 1
                print(f"    ❌ Failed to parse")
                
        except Exception as e:
            results["failed"] += 1
            print(f"    ❌ Error: {e}")
    
    return results

def print_results(results, output_format):
    """Print results in a readable format"""
    if isinstance(results, dict) and "emails" in results:
        # Folder results
        print(f"\n📊 Results Summary:")
        print(f"  📁 Folder: {results['folder']}")
        print(f"  📧 Total files: {results['total_files']}")
        print(f"  ✅ Processed: {results['processed']}")
        print(f"  ❌ Failed: {results['failed']}")
        
        if results["emails"]:
            print(f"\n📋 Processed Emails:")
            for email in results["emails"]:
                print(f"  📧 {email['file']}")
                print(f"     Subject: {email['subject']}")
                print(f"     Sender: {email['sender']}")
                print(f"     Categories: {', '.join(email['categories'])}")
                if 'summary' in email:
                    print(f"     Summary: {email['summary']}")
                print()
    else:
        # Single file result
        if results:
            print(f"\n📧 Email Details:")
            print(f"  File: {results['file']}")
            print(f"  Subject: {results['subject']}")
            print(f"  Sender: {results['sender']}")
            print(f"  Categories: {', '.join(results['categories'])}")
            print(f"  Correlation Score: {results['correlation_score']:.3f}")
            
            if 'entities' in results:
                print(f"  Extracted Entities:")
                for entity_type, items in results['entities'].items():
                    if items:
                        print(f"    {entity_type.title()}: {', '.join(items)}")

def main():
    parser = argparse.ArgumentParser(description="Parse .msg email files")
    parser.add_argument("path", help="Path to .msg file or folder containing .msg files")
    parser.add_argument("--format", choices=["summary", "detailed", "json"], 
                       default="summary", help="Output format")
    parser.add_argument("--output", help="Save results to file")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    
    if path.is_file():
        print("🔍 Parsing single file...")
        results = parse_single_file(args.path, args.format)
    elif path.is_dir():
        print("🔍 Parsing folder...")
        results = parse_folder(args.path, args.format)
    else:
        print(f"❌ Path not found: {args.path}")
        return
    
    if not results:
        print("❌ No results to display")
        return
    
    if args.format == "json":
        output = json.dumps(results, indent=2, default=str)
        print(output)
        
        if args.output:
            with open(args.output, 'w') as f:
                f.write(output)
            print(f"📄 Results saved to: {args.output}")
    else:
        print_results(results, args.format)
        
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(results, f, indent=2, default=str)
            print(f"📄 Results saved to: {args.output}")

if __name__ == "__main__":
    main()