#!/usr/bin/env python3
"""
Email Parser CLI - Complete Command Line Interface
Provides direct access to all MCP server tools via command line flags
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from email_parser.parser import EmailParser
from email_parser.ai_integration import create_ai_analyzer

def setup_parser():
    """Setup the argument parser with subcommands"""
    parser = argparse.ArgumentParser(
        description="Email Parser CLI - Access all MCP server tools",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Parse single file
  %(prog)s parse-file email.msg --format json

  # Parse folder with summary
  %(prog)s parse-folder ./emails --format summary --output results.json

  # Analyze patterns
  %(prog)s analyze-patterns ./emails --type categories --format detailed

  # Extract entities from text
  %(prog)s extract-entities --text "Contact john@example.com at 555-123-4567"

  # Server modes
  %(prog)s server --mcp                    # Start MCP server
  %(prog)s server --http --port 8000       # Start HTTP server
  %(prog)s server --websocket --port 8001  # Start WebSocket server
        """
    )
    
    # Create subparsers
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # Parse single file command
    parse_file_parser = subparsers.add_parser(
        "parse-file", 
        help="Parse a single .msg email file"
    )
    parse_file_parser.add_argument("file_path", help="Path to .msg file")
    parse_file_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                                 default="summary", help="Output format")
    parse_file_parser.add_argument("--output", "-o", help="Save output to file")
    parse_file_parser.add_argument("--auto-save", action="store_true", 
                                 help="Automatically save to output/emails/ with timestamp")
    parse_file_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # Parse folder command
    parse_folder_parser = subparsers.add_parser(
        "parse-folder",
        help="Parse all .msg files in a folder"
    )
    parse_folder_parser.add_argument("folder_path", help="Path to folder containing .msg files")
    parse_folder_parser.add_argument("--output-format", choices=["summary", "detailed", "json"],
                                   default="summary", help="Email output format")
    parse_folder_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                                   default="summary", help="Output format")
    parse_folder_parser.add_argument("--output", "-o", help="Save output to file")
    parse_folder_parser.add_argument("--auto-save", action="store_true", 
                                   help="Automatically save to output/analysis/ with timestamp")
    parse_folder_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # Analyze patterns command
    analyze_parser = subparsers.add_parser(
        "analyze-patterns",
        help="Analyze email patterns in a folder"
    )
    analyze_parser.add_argument("folder_path", help="Path to folder containing .msg files")
    analyze_parser.add_argument("--type", "-t", choices=["categories", "senders", "entities", "all"],
                               default="categories", help="Type of analysis to perform")
    analyze_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                               default="summary", help="Output format")
    analyze_parser.add_argument("--output", "-o", help="Save output to file")
    analyze_parser.add_argument("--auto-save", action="store_true", 
                               help="Automatically save to output/analysis/ with timestamp")
    analyze_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # Extract entities command
    entities_parser = subparsers.add_parser(
        "extract-entities",
        help="Extract entities from text"
    )
    entities_parser.add_argument("--text", required=True, help="Text to analyze")
    entities_parser.add_argument("--show-patterns", action="store_true", 
                               help="Show the regex patterns used")
    entities_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                                default="summary", help="Output format")
    entities_parser.add_argument("--output", "-o", help="Save output to file")
    entities_parser.add_argument("--auto-save", action="store_true", 
                               help="Automatically save to output/entities/ with timestamp")
    entities_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # AI analyze command
    ai_parser = subparsers.add_parser(
        "ai-analyze",
        help="AI-powered analysis using Ollama Phi3"
    )
    ai_subparsers = ai_parser.add_subparsers(dest="ai_command", help="AI analysis types")
    
    # AI analyze file
    ai_file_parser = ai_subparsers.add_parser("file", help="Analyze single email file with AI")
    ai_file_parser.add_argument("file_path", help="Path to .msg file")
    ai_file_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                               default="summary", help="Output format")
    ai_file_parser.add_argument("--output", "-o", help="Save output to file")
    ai_file_parser.add_argument("--auto-save", action="store_true", 
                               help="Automatically save to output/analysis/ with timestamp")
    ai_file_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # AI analyze text
    ai_text_parser = ai_subparsers.add_parser("text", help="Analyze arbitrary text with AI")
    ai_text_parser.add_argument("--text", required=True, help="Text to analyze")
    ai_text_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                               default="summary", help="Output format")
    ai_text_parser.add_argument("--output", "-o", help="Save output to file")
    ai_text_parser.add_argument("--auto-save", action="store_true", 
                               help="Automatically save to output/analysis/ with timestamp")
    ai_text_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # AI smart categorize
    ai_categorize_parser = ai_subparsers.add_parser("categorize", help="Smart categorization of email folder")
    ai_categorize_parser.add_argument("folder_path", help="Path to folder containing .msg files")
    ai_categorize_parser.add_argument("--format", choices=["json", "summary", "detailed"], 
                                     default="summary", help="Output format")
    ai_categorize_parser.add_argument("--output", "-o", help="Save output to file")
    ai_categorize_parser.add_argument("--auto-save", action="store_true", 
                                     help="Automatically save to output/analysis/ with timestamp")
    ai_categorize_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    # Server command
    server_parser = subparsers.add_parser(
        "server",
        help="Start various server modes"
    )
    server_group = server_parser.add_mutually_exclusive_group(required=True)
    server_group.add_argument("--mcp", action="store_true", help="Start MCP server (stdio)")
    server_group.add_argument("--http", action="store_true", help="Start HTTP server")
    server_group.add_argument("--websocket", action="store_true", help="Start WebSocket server")
    server_parser.add_argument("--port", type=int, default=8000, help="Port for HTTP/WebSocket server")
    server_parser.add_argument("--host", default="localhost", help="Host for HTTP/WebSocket server")
    
    # Demo command
    demo_parser = subparsers.add_parser(
        "demo",
        help="Run demonstration of functionality"
    )
    demo_parser.add_argument("--type", choices=["basic", "mcp", "all"], default="all",
                           help="Type of demo to run")
    demo_parser.add_argument("--quiet", "-q", action="store_true", help="Suppress progress messages")
    
    return parser

class EmailCLI:
    """Main CLI class"""
    
    def __init__(self):
        self.parser = EmailParser()
        self.ai_analyzer = create_ai_analyzer()  # Optional AI integration
        self.output_dir = Path("output")
        self._ensure_output_directories()
    
    def print_status(self, message: str, quiet: bool = False):
        """Print status message unless quiet mode"""
        if not quiet:
            print(f"🔍 {message}")
    
    def print_error(self, message: str):
        """Print error message"""
        print(f"❌ {message}", file=sys.stderr)
    
    def print_success(self, message: str, quiet: bool = False):
        """Print success message unless quiet mode"""
        if not quiet:
            print(f"✅ {message}")
    
    def _ensure_output_directories(self):
        """Ensure output directories exist"""
        directories = ["emails", "analysis", "entities", "reports"]
        for dir_name in directories:
            (self.output_dir / dir_name).mkdir(parents=True, exist_ok=True)
    
    def _get_output_path(self, category: str, name: str = None, extension: str = "json") -> Path:
        """Generate timestamped output path"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if name:
            filename = f"{name}_{timestamp}.{extension}"
        else:
            filename = f"{category}_{timestamp}.{extension}"
        
        return self.output_dir / category / filename
    
    def _auto_save_output(self, content: str, category: str, name: str = None, 
                         custom_path: str = None, quiet: bool = False) -> str:
        """Automatically save output with smart naming"""
        if custom_path:
            # Use custom path if provided
            filepath = Path(custom_path)
        else:
            # Generate automatic path
            filepath = self._get_output_path(category, name)
        
        try:
            # Ensure parent directory exists
            filepath.parent.mkdir(parents=True, exist_ok=True)
            
            with open(filepath, 'w') as f:
                f.write(content)
            
            self.print_success(f"Output saved to: {filepath}", quiet)
            return str(filepath)
            
        except Exception as e:
            self.print_error(f"Failed to save output: {e}")
            return None
    
    def format_output(self, data: Any, format_type: str) -> str:
        """Format output according to specified format"""
        if format_type == "json":
            return json.dumps(data, indent=2, default=str)
        elif format_type == "summary":
            return self._format_summary(data)
        elif format_type == "detailed":
            return self._format_detailed(data)
        else:
            return str(data)
    
    def _format_summary(self, data: Any) -> str:
        """Format data as summary"""
        if isinstance(data, dict):
            if "error" in data:
                return f"Error: {data['error']}"
            
            # Handle different data types
            if "emails" in data:  # Folder results
                lines = [f"📁 Folder Analysis Results"]
                lines.append(f"   Total files: {data.get('total_files', 0)}")
                lines.append(f"   Processed: {data.get('processed', 0)}")
                lines.append(f"   Failed: {data.get('failed', 0)}")
                
                if data.get("emails"):
                    lines.append("\n📧 Email Summaries:")
                    for email in data["emails"][:5]:  # Show first 5
                        lines.append(f"   • {email.get('subject', 'No subject')} ({email.get('sender', 'Unknown')})")
                
                return "\n".join(lines)
            
            elif "subject" in data:  # Single email
                lines = [f"📧 Email: {data['subject']}"]
                lines.append(f"   From: {data.get('sender', 'Unknown')}")
                lines.append(f"   Categories: {', '.join(data.get('categories', []))}")
                lines.append(f"   Correlation: {data.get('correlation_score', 0):.3f}")
                return "\n".join(lines)
            
            elif "analysis_type" in data:  # Pattern analysis
                lines = [f"📊 Pattern Analysis ({data['analysis_type']})"]
                lines.append(f"   Processed emails: {data.get('processed_emails', 0)}")
                
                if "category_analysis" in data:
                    lines.append("\n🏷️ Categories:")
                    for cat, stats in list(data["category_analysis"].get("categories", {}).items())[:5]:
                        lines.append(f"   • {cat}: {stats['count']} emails ({stats['percentage']:.1f}%)")
                
                return "\n".join(lines)
        
        return json.dumps(data, indent=2, default=str)
    
    def _format_detailed(self, data: Any) -> str:
        """Format data as detailed output"""
        return json.dumps(data, indent=2, default=str)
    
    def save_output(self, content: str, filepath: str, quiet: bool = False):
        """Save output to file (custom path)"""
        try:
            path = Path(filepath)
            path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(path, 'w') as f:
                f.write(content)
            self.print_success(f"Output saved to: {filepath}", quiet)
        except Exception as e:
            self.print_error(f"Failed to save output: {e}")
    
    def parse_email_file(self, file_path: str, format_type: str, quiet: bool = False) -> Dict[str, Any]:
        """Parse a single email file"""
        self.print_status(f"Parsing file: {file_path}", quiet)
        
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            if not path.suffix.lower() == '.msg':
                return {"error": f"Unsupported file type: {path.suffix}"}
            
            email_content = self.parser.parse_msg_file(path)
            if email_content is None:
                return {"error": "Failed to parse email file"}
            
            # Convert to dictionary format
            result = {
                "message_id": email_content.message_id,
                "subject": email_content.subject,
                "sender": email_content.sender,
                "recipients": email_content.recipients,
                "cc_recipients": email_content.cc_recipients,
                "bcc_recipients": email_content.bcc_recipients,
                "sent_date": email_content.sent_date.isoformat() if email_content.sent_date else None,
                "body_text": email_content.body_text,
                "body_html": email_content.body_html,
                "attachments": email_content.attachments,
                "priority": email_content.priority,
                "categories": email_content.categories,
                "correlation_score": email_content.correlation_score,
                "extracted_entities": email_content.extracted_entities,
                "standardized_format": email_content.standardized_format
            }
            
            self.print_success("Email parsed successfully", quiet)
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def parse_email_folder(self, folder_path: str, output_format: str = "summary", 
                          format_type: str = "summary", quiet: bool = False) -> Dict[str, Any]:
        """Parse all emails in a folder"""
        self.print_status(f"Parsing folder: {folder_path}", quiet)
        
        try:
            folder = Path(folder_path)
            if not folder.exists() or not folder.is_dir():
                return {"error": f"Folder not found or not a directory: {folder_path}"}
            
            msg_files = list(folder.glob("*.msg"))
            if not msg_files:
                return {"error": f"No .msg files found in {folder_path}"}
            
            results = {
                "total_files": len(msg_files),
                "processed": 0,
                "failed": 0,
                "emails": [],
                "statistics": {
                    "categories": {},
                    "senders": {},
                    "avg_correlation": 0.0
                }
            }
            
            total_correlation = 0.0
            
            for msg_file in msg_files:
                if not quiet:
                    print(f"  📧 Processing: {msg_file.name}")
                
                try:
                    email_content = self.parser.parse_msg_file(msg_file)
                    if email_content:
                        results["processed"] += 1
                        total_correlation += email_content.correlation_score
                        
                        # Update statistics
                        for category in email_content.categories:
                            results["statistics"]["categories"][category] = \
                                results["statistics"]["categories"].get(category, 0) + 1
                        
                        sender_domain = email_content.sender.split('@')[-1] if '@' in email_content.sender else email_content.sender
                        results["statistics"]["senders"][sender_domain] = \
                            results["statistics"]["senders"].get(sender_domain, 0) + 1
                        
                        # Format output based on requested format
                        if output_format == "detailed":
                            email_result = {
                                "file": msg_file.name,
                                "message_id": email_content.message_id,
                                "subject": email_content.subject,
                                "sender": email_content.sender,
                                "recipients": email_content.recipients,
                                "sent_date": email_content.sent_date.isoformat() if email_content.sent_date else None,
                                "categories": email_content.categories,
                                "correlation_score": email_content.correlation_score,
                                "extracted_entities": email_content.extracted_entities,
                                "standardized_format": email_content.standardized_format
                            }
                        else:  # summary
                            email_result = {
                                "file": msg_file.name,
                                "subject": email_content.subject,
                                "sender": email_content.sender,
                                "categories": email_content.categories,
                                "correlation_score": email_content.correlation_score,
                                "summary": email_content.standardized_format.get("summary", "")
                            }
                        
                        results["emails"].append(email_result)
                    else:
                        results["failed"] += 1
                        
                except Exception as e:
                    results["failed"] += 1
                    if not quiet:
                        print(f"    ❌ Error: {e}")
            
            # Calculate average correlation
            if results["processed"] > 0:
                results["statistics"]["avg_correlation"] = total_correlation / results["processed"]
            
            self.print_success(f"Processed {results['processed']}/{results['total_files']} files", quiet)
            return results
            
        except Exception as e:
            return {"error": str(e)}
    
    def analyze_email_patterns(self, folder_path: str, analysis_type: str = "categories", 
                             quiet: bool = False) -> Dict[str, Any]:
        """Analyze patterns in email folder"""
        self.print_status(f"Analyzing patterns in: {folder_path}", quiet)
        
        try:
            folder = Path(folder_path)
            if not folder.exists() or not folder.is_dir():
                return {"error": f"Folder not found: {folder_path}"}
            
            msg_files = list(folder.glob("*.msg"))
            if not msg_files:
                return {"error": f"No .msg files found in {folder_path}"}
            
            analysis_results = {
                "total_emails": len(msg_files),
                "analysis_type": analysis_type,
                "timestamp": Path(__file__).stat().st_mtime  # Use file mtime as timestamp
            }
            
            # Process all emails
            emails_data = []
            for msg_file in msg_files:
                try:
                    email_content = self.parser.parse_msg_file(msg_file)
                    if email_content:
                        emails_data.append(email_content)
                except Exception as e:
                    if not quiet:
                        print(f"  ⚠️ Skipping {msg_file.name}: {e}")
            
            if not emails_data:
                return {"error": "No emails could be processed"}
            
            analysis_results["processed_emails"] = len(emails_data)
            
            # Perform requested analysis
            if analysis_type in ["categories", "all"]:
                analysis_results["category_analysis"] = self._analyze_categories(emails_data)
            
            if analysis_type in ["senders", "all"]:
                analysis_results["sender_analysis"] = self._analyze_senders(emails_data)
            
            if analysis_type in ["entities", "all"]:
                analysis_results["entity_analysis"] = self._analyze_entities(emails_data)
            
            if analysis_type == "all":
                analysis_results["correlation_analysis"] = self._analyze_correlations(emails_data)
            
            self.print_success(f"Analysis complete: {len(emails_data)} emails processed", quiet)
            return analysis_results
            
        except Exception as e:
            return {"error": str(e)}
    
    def ai_analyze_email_file(self, file_path: str, quiet: bool = False) -> Dict[str, Any]:
        """AI-powered analysis of single email file"""
        self.print_status(f"AI analyzing email file: {file_path}", quiet)
        
        if not self.ai_analyzer:
            return {"error": "AI analysis not available. Ensure Ollama is running with Phi3 model installed"}
        
        try:
            path = Path(file_path)
            if not path.exists():
                return {"error": f"File not found: {file_path}"}
            
            if not path.suffix.lower() == '.msg':
                return {"error": f"Unsupported file type: {path.suffix}"}
            
            # Parse email first
            email_content = self.parser.parse_msg_file(path)
            if email_content is None:
                return {"error": "Failed to parse email file"}
            
            # Perform AI analysis
            ai_result = self.ai_analyzer.analyze_email(email_content)
            if ai_result is None:
                return {"error": "AI analysis failed"}
            
            result = {
                "file": str(path.name),
                "traditional_analysis": {
                    "subject": email_content.subject,
                    "sender": email_content.sender,
                    "categories": email_content.categories,
                    "correlation_score": email_content.correlation_score,
                    "extracted_entities": email_content.extracted_entities
                },
                "ai_analysis": {
                    "summary": ai_result.summary,
                    "categories": ai_result.categories,
                    "sentiment": ai_result.sentiment,
                    "priority_score": ai_result.priority_score,
                    "key_insights": ai_result.key_insights,
                    "action_items": ai_result.action_items,
                    "confidence": ai_result.confidence,
                    "model_used": ai_result.model_used
                }
            }
            
            self.print_success("AI analysis complete", quiet)
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def ai_analyze_text(self, text: str, quiet: bool = False) -> Dict[str, Any]:
        """AI-powered analysis of arbitrary text"""
        self.print_status("AI analyzing text", quiet)
        
        if not self.ai_analyzer:
            return {"error": "AI analysis not available. Ensure Ollama is running with Phi3 model installed"}
        
        try:
            result = self.ai_analyzer.analyze_text(text)
            self.print_success("AI text analysis complete", quiet)
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def ai_smart_categorize_folder(self, folder_path: str, quiet: bool = False) -> Dict[str, Any]:
        """AI-powered smart categorization of email folder"""
        self.print_status(f"AI categorizing folder: {folder_path}", quiet)
        
        if not self.ai_analyzer:
            return {"error": "AI analysis not available. Ensure Ollama is running with Phi3 model installed"}
        
        try:
            folder = Path(folder_path)
            if not folder.exists() or not folder.is_dir():
                return {"error": f"Folder not found: {folder_path}"}
            
            msg_files = list(folder.glob("*.msg"))
            if not msg_files:
                return {"error": f"No .msg files found in {folder_path}"}
            
            results = {
                "total_files": len(msg_files),
                "processed": 0,
                "failed": 0,
                "ai_categories": {},
                "sentiment_distribution": {},
                "priority_distribution": {"low": 0, "medium": 0, "high": 0, "critical": 0},
                "emails": []
            }
            
            for msg_file in msg_files:
                if not quiet:
                    print(f"  🤖 AI analyzing: {msg_file.name}")
                
                try:
                    email_content = self.parser.parse_msg_file(msg_file)
                    if email_content:
                        ai_result = self.ai_analyzer.analyze_email(email_content)
                        if ai_result:
                            results["processed"] += 1
                            
                            # Update category statistics
                            for category in ai_result.categories:
                                results["ai_categories"][category] = \
                                    results["ai_categories"].get(category, 0) + 1
                            
                            # Update sentiment distribution
                            sentiment = ai_result.sentiment
                            results["sentiment_distribution"][sentiment] = \
                                results["sentiment_distribution"].get(sentiment, 0) + 1
                            
                            # Update priority distribution
                            if ai_result.priority_score >= 0.9:
                                priority_level = "critical"
                            elif ai_result.priority_score >= 0.7:
                                priority_level = "high"
                            elif ai_result.priority_score >= 0.4:
                                priority_level = "medium"
                            else:
                                priority_level = "low"
                            
                            results["priority_distribution"][priority_level] += 1
                            
                            # Add email summary
                            results["emails"].append({
                                "file": msg_file.name,
                                "subject": email_content.subject,
                                "ai_summary": ai_result.summary,
                                "ai_categories": ai_result.categories,
                                "sentiment": ai_result.sentiment,
                                "priority_score": ai_result.priority_score,
                                "key_insights": ai_result.key_insights[:2],  # Limit for brevity
                                "action_items": ai_result.action_items[:2]
                            })
                        else:
                            results["failed"] += 1
                    else:
                        results["failed"] += 1
                        
                except Exception as e:
                    if not quiet:
                        print(f"    ❌ Error: {e}")
                    results["failed"] += 1
            
            self.print_success(f"AI categorization complete: {results['processed']}/{results['total_files']} files", quiet)
            return results
            
        except Exception as e:
            return {"error": str(e)}
    
    def extract_entities_from_text(self, text: str, show_patterns: bool = False, 
                                 quiet: bool = False) -> Dict[str, Any]:
        """Extract entities from arbitrary text"""
        self.print_status("Extracting entities from text", quiet)
        
        try:
            entities = self.parser._extract_entities(text)
            
            result = {
                "text": text,
                "entities": entities,
                "entity_count": sum(len(items) for items in entities.values())
            }
            
            if show_patterns:
                result["patterns"] = self.parser.entity_patterns
            
            self.print_success(f"Found {result['entity_count']} entities", quiet)
            return result
            
        except Exception as e:
            return {"error": str(e)}
    
    def _analyze_categories(self, emails_data):
        """Analyze email categories"""
        category_stats = {}
        total_correlation = 0.0
        
        for email in emails_data:
            total_correlation += email.correlation_score
            for category in email.categories:
                if category not in category_stats:
                    category_stats[category] = {"count": 0, "correlation_sum": 0.0}
                category_stats[category]["count"] += 1
                category_stats[category]["correlation_sum"] += email.correlation_score
        
        # Calculate averages
        for category, stats in category_stats.items():
            stats["avg_correlation"] = stats["correlation_sum"] / stats["count"]
            stats["percentage"] = (stats["count"] / len(emails_data)) * 100
            del stats["correlation_sum"]
        
        return {
            "total_categories": len(category_stats),
            "avg_correlation_overall": total_correlation / len(emails_data),
            "categories": dict(sorted(category_stats.items(), key=lambda x: x[1]["count"], reverse=True))
        }
    
    def _analyze_senders(self, emails_data):
        """Analyze sender patterns"""
        sender_stats = {}
        
        for email in emails_data:
            sender = email.sender
            if sender not in sender_stats:
                sender_stats[sender] = {
                    "count": 0,
                    "categories": set(),
                    "avg_correlation": 0.0,
                    "correlation_sum": 0.0
                }
            
            sender_stats[sender]["count"] += 1
            sender_stats[sender]["categories"].update(email.categories)
            sender_stats[sender]["correlation_sum"] += email.correlation_score
        
        # Calculate averages and convert sets to lists
        for sender, stats in sender_stats.items():
            stats["avg_correlation"] = stats["correlation_sum"] / stats["count"]
            stats["categories"] = list(stats["categories"])
            del stats["correlation_sum"]
        
        return {
            "total_senders": len(sender_stats),
            "senders": dict(sorted(sender_stats.items(), key=lambda x: x[1]["count"], reverse=True))
        }
    
    def _analyze_entities(self, emails_data):
        """Analyze extracted entities"""
        entity_stats = {}
        
        for email in emails_data:
            for entity_type, entities in email.extracted_entities.items():
                if entity_type not in entity_stats:
                    entity_stats[entity_type] = {"unique_count": 0, "total_mentions": 0, "values": set()}
                
                entity_stats[entity_type]["total_mentions"] += len(entities)
                entity_stats[entity_type]["values"].update(entities)
        
        # Convert sets to lists and calculate unique counts
        for entity_type, stats in entity_stats.items():
            stats["unique_count"] = len(stats["values"])
            stats["values"] = list(stats["values"])[:20]  # Limit to first 20
        
        return entity_stats
    
    def _analyze_correlations(self, emails_data):
        """Analyze correlation patterns"""
        correlations = [email.correlation_score for email in emails_data]
        
        return {
            "avg_correlation": sum(correlations) / len(correlations),
            "min_correlation": min(correlations),
            "max_correlation": max(correlations),
            "high_correlation_count": len([c for c in correlations if c > 0.7]),
            "low_correlation_count": len([c for c in correlations if c < 0.3])
        }

def main():
    """Main CLI entry point"""
    arg_parser = setup_parser()
    args = arg_parser.parse_args()
    
    if not args.command:
        arg_parser.print_help()
        return
    
    cli = EmailCLI()
    result = None
    
    try:
        if args.command == "parse-file":
            result = cli.parse_email_file(args.file_path, args.format, args.quiet)
        
        elif args.command == "parse-folder":
            output_fmt = getattr(args, 'output_format', args.format)
            result = cli.parse_email_folder(args.folder_path, output_fmt, args.format, args.quiet)
        
        elif args.command == "analyze-patterns":
            result = cli.analyze_email_patterns(args.folder_path, args.type, args.quiet)
        
        elif args.command == "extract-entities":
            result = cli.extract_entities_from_text(args.text, args.show_patterns, args.quiet)
        
        elif args.command == "ai-analyze":
            if args.ai_command == "file":
                result = cli.ai_analyze_email_file(args.file_path, args.quiet)
            elif args.ai_command == "text":
                result = cli.ai_analyze_text(args.text, args.quiet)
            elif args.ai_command == "categorize":
                result = cli.ai_smart_categorize_folder(args.folder_path, args.quiet)
            else:
                cli.print_error("No AI analysis command specified")
                sys.exit(1)
        
        elif args.command == "server":
            # Import server modules here to avoid import errors if not needed
            if args.mcp:
                from email_parser.main import run_mcp_server
                print("🚀 Starting MCP server...")
                run_mcp_server()
                return
            elif args.http:
                import asyncio
                from email_parser.transports import start_http_server
                print(f"🌐 Starting HTTP server on {args.host}:{args.port}")
                asyncio.run(start_http_server(args.host, args.port))
                return
            elif args.websocket:
                import asyncio
                from email_parser.transports import start_websocket_server
                print(f"🔌 Starting WebSocket server on {args.host}:{args.port}")
                asyncio.run(start_websocket_server(args.host, args.port))
                return
        
        elif args.command == "demo":
            if args.type in ["basic", "all"]:
                print("🎭 Running basic functionality demo...")
                # Run basic demo here
                from demo_mcp_functionality import demo_mcp_tools
                import asyncio
                asyncio.run(demo_mcp_tools())
            return
        
        # Handle output
        if result:
            if "error" in result:
                cli.print_error(result["error"])
                sys.exit(1)
            
            output = cli.format_output(result, args.format)
            print(output)
            
            # Handle file output (custom path or auto-save)
            if hasattr(args, 'output') and args.output:
                cli.save_output(output, args.output, args.quiet)
            elif hasattr(args, 'auto_save') and args.auto_save:
                # Determine category and name based on command
                if args.command == "parse-file":
                    category = "emails"
                    name = Path(args.file_path).stem
                elif args.command == "parse-folder":
                    category = "analysis"
                    name = f"folder_{Path(args.folder_path).name}"
                elif args.command == "analyze-patterns":
                    category = "analysis"  
                    name = f"patterns_{args.type}"
                elif args.command == "extract-entities":
                    category = "entities"
                    name = "entities"
                elif args.command == "ai-analyze":
                    category = "analysis"
                    if hasattr(args, 'ai_command'):
                        if args.ai_command == "file":
                            name = f"ai_file_{Path(args.file_path).stem}"
                        elif args.ai_command == "text":
                            name = "ai_text"
                        elif args.ai_command == "categorize":
                            name = f"ai_categorize_{Path(args.folder_path).name}"
                        else:
                            name = "ai_analysis"
                    else:
                        name = "ai_analysis"
                else:
                    category = "reports"
                    name = args.command
                
                cli._auto_save_output(output, category, name, quiet=args.quiet)
    
    except KeyboardInterrupt:
        print("\n🛑 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        cli.print_error(f"Unexpected error: {e}")
        if not args.quiet:
            import traceback
            traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()