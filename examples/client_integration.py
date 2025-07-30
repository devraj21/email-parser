#!/usr/bin/env python3
"""
Example client integrations for Email Parser MCP Server
Shows how to connect to the MCP server using different transports
"""

import asyncio
import json
import sys
from pathlib import Path
from typing import Any, Dict

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

try:
    import websockets
    import httpx
except ImportError:
    print("Warning: websockets and httpx not installed. Install with: uv pip install websockets httpx")
    websockets = None
    httpx = None

def print_header(title: str):
    """Print formatted header"""
    print(f"\n{'='*60}")
    print(f"🔌 {title}")
    print(f"{'='*60}")

def print_result(result: Dict[str, Any]):
    """Print formatted result"""
    print("📋 Result:")
    print(json.dumps(result, indent=2, default=str))

class HTTPClient:
    """HTTP client for MCP server"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.client = None
    
    async def __aenter__(self):
        if httpx is None:
            raise ImportError("httpx is required for HTTP client")
        self.client = httpx.AsyncClient()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.client:
            await self.client.aclose()
    
    async def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a single email file"""
        response = await self.client.post(
            f"{self.base_url}/api/parse/file",
            json={"file_path": file_path}
        )
        return response.json()
    
    async def parse_folder(self, folder_path: str, output_format: str = "summary") -> Dict[str, Any]:
        """Parse all emails in a folder"""
        response = await self.client.post(
            f"{self.base_url}/api/parse/folder",
            json={"folder_path": folder_path, "output_format": output_format}
        )
        return response.json()
    
    async def analyze_patterns(self, folder_path: str, analysis_type: str = "categories") -> Dict[str, Any]:
        """Analyze email patterns"""
        response = await self.client.post(
            f"{self.base_url}/api/analyze/patterns",
            json={"folder_path": folder_path, "analysis_type": analysis_type}
        )
        return response.json()
    
    async def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        response = await self.client.post(
            f"{self.base_url}/api/extract/entities",
            json={"text": text}
        )
        return response.json()

class WebSocketClient:
    """WebSocket client for MCP server"""
    
    def __init__(self, url: str = "ws://localhost:8001/ws/client1"):
        self.url = url
        self.websocket = None
        self.request_counter = 0
    
    async def __aenter__(self):
        if websockets is None:
            raise ImportError("websockets is required for WebSocket client")
        self.websocket = await websockets.connect(self.url)
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.websocket:
            await self.websocket.close()
    
    async def _send_request(self, action: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """Send request and wait for response"""
        self.request_counter += 1
        request = {
            "request_id": f"req_{self.request_counter}",
            "action": action,
            "params": params
        }
        
        await self.websocket.send(json.dumps(request))
        response = await self.websocket.recv()
        return json.loads(response)
    
    async def parse_file(self, file_path: str) -> Dict[str, Any]:
        """Parse a single email file"""
        return await self._send_request("parse_file", {"file_path": file_path})
    
    async def parse_folder(self, folder_path: str, output_format: str = "summary") -> Dict[str, Any]:
        """Parse all emails in a folder"""
        return await self._send_request("parse_folder", {
            "folder_path": folder_path,
            "output_format": output_format
        })
    
    async def analyze_patterns(self, folder_path: str, analysis_type: str = "categories") -> Dict[str, Any]:
        """Analyze email patterns"""
        return await self._send_request("analyze_patterns", {
            "folder_path": folder_path,
            "analysis_type": analysis_type
        })
    
    async def extract_entities(self, text: str) -> Dict[str, Any]:
        """Extract entities from text"""
        return await self._send_request("extract_entities", {"text": text})

async def demo_http_client():
    """Demonstrate HTTP client usage"""
    print_header("HTTP Client Demo")
    
    try:
        async with HTTPClient() as client:
            # Test entity extraction
            print("\n📧 Testing entity extraction...")
            sample_text = """
            Hi team,
            
            Please contact sarah@company.com or call +1-555-987-6543 for the project update.
            The deadline is 03/15/2024 and the budget is $50,000.
            
            More info: https://project.company.com
            """
            
            result = await client.extract_entities(sample_text)
            print_result(result)
            
            # Test folder parsing (will fail if no folder exists, but shows the API)
            print("\n📁 Testing folder parsing...")
            folder_result = await client.parse_folder("examples/sample_emails", "summary")
            print_result(folder_result)
            
    except Exception as e:
        print(f"❌ HTTP client demo failed: {e}")
        print("Make sure the HTTP server is running: python -m src.email_parser.transports --transport http")

async def demo_websocket_client():
    """Demonstrate WebSocket client usage"""
    print_header("WebSocket Client Demo")
    
    try:
        async with WebSocketClient() as client:
            # Test entity extraction
            print("\n📧 Testing entity extraction via WebSocket...")
            sample_text = """
            Meeting scheduled for 12/25/2024 at 2 PM.
            Contact: admin@company.com or (555) 123-4567
            Budget approved: €75,000
            """
            
            result = await client.extract_entities(sample_text)
            print_result(result)
            
            # Test pattern analysis
            print("\n📊 Testing pattern analysis...")
            analysis_result = await client.analyze_patterns("examples/sample_emails", "all")
            print_result(analysis_result)
            
    except Exception as e:
        print(f"❌ WebSocket client demo failed: {e}")
        print("Make sure the WebSocket server is running: python -m src.email_parser.transports --transport websocket")

async def demo_mcp_stdio_client():
    """Demonstrate stdio MCP client (simulated)"""
    print_header("MCP Stdio Client Demo")
    
    print("""
🔧 MCP Stdio Integration Example:

For Claude Desktop integration, add this to your configuration:

{
  "mcpServers": {
    "email-parser": {
      "command": "python",
      "args": ["-m", "src.email_parser.main", "--mcp"],
      "cwd": "/path/to/email-parser"
    }
  }
}

Available tools in Claude:
• parse_email_file - Parse individual .msg files
• parse_email_folder - Batch process email folders  
• analyze_email_patterns - Analyze communication patterns
• extract_entities_from_text - Extract structured data from text

Available prompts:
• Email Analysis Report - Generate comprehensive email analysis
• Email Compliance Check - Security and compliance analysis

Available resources:
• config://parser-settings - Current parser configuration
• schema://email-content - EmailContent data structure
    """)

class BusinessWorkflowExamples:
    """Real-world business workflow examples"""
    
    @staticmethod
    async def compliance_audit_workflow():
        """Example: Compliance audit workflow"""
        print_header("Compliance Audit Workflow")
        
        print("""
🔍 Automated Compliance Audit Process:

1. **Batch Email Processing**
   - Parse all emails from compliance folder
   - Extract sensitive data (PII, financial info)
   - Categorize by risk level

2. **Pattern Analysis**
   - Identify unusual communication patterns
   - Flag emails with compliance keywords
   - Track external communications

3. **Report Generation**
   - Generate compliance summary
   - List potential violations
   - Create audit trail

Example Implementation:
        """)
        
        # Simulate the workflow
        sample_code = '''
async def compliance_audit(folder_path: str):
    async with HTTPClient() as client:
        # Step 1: Parse all emails
        emails = await client.parse_folder(folder_path, "detailed")
        
        # Step 2: Analyze for compliance issues
        patterns = await client.analyze_patterns(folder_path, "all")
        
        # Step 3: Generate compliance report
        high_risk_emails = [
            email for email in emails.get("emails", [])
            if any(cat in ["urgent", "contract", "support"] 
                  for cat in email.get("categories", []))
        ]
        
        return {
            "total_emails": emails.get("total_files", 0),
            "high_risk_count": len(high_risk_emails),
            "compliance_score": calculate_compliance_score(patterns),
            "recommendations": generate_recommendations(high_risk_emails)
        }
        '''
        
        print(sample_code)
    
    @staticmethod
    async def customer_service_analytics():
        """Example: Customer service analytics"""
        print_header("Customer Service Analytics")
        
        print("""
📊 Customer Service Email Analytics:

1. **Response Time Analysis**
   - Track email response patterns
   - Identify bottlenecks
   - Measure customer satisfaction indicators

2. **Issue Classification**
   - Automatically categorize support requests
   - Priority scoring based on content
   - Route emails to appropriate teams

3. **Performance Metrics**
   - Agent performance tracking
   - Customer sentiment analysis
   - Process improvement insights

Integration with CRM systems, helpdesk platforms, and reporting tools.
        """)
    
    @staticmethod
    async def sales_intelligence():
        """Example: Sales intelligence workflow"""
        print_header("Sales Intelligence Workflow")
        
        print("""
💼 Sales Email Intelligence:

1. **Lead Qualification**
   - Extract contact information
   - Identify budget and timeline mentions
   - Score lead quality

2. **Opportunity Tracking**
   - Track deal progression through emails
   - Extract contract values and dates
   - Monitor competitor mentions

3. **Relationship Mapping**
   - Identify key stakeholders
   - Track communication frequency
   - Map organizational relationships

Perfect for CRM integration and sales process automation.
        """)

async def main():
    """Run all client integration demos"""
    print_header("Email Parser MCP Server - Client Integration Examples")
    
    # Basic client demos
    await demo_http_client()
    await demo_websocket_client()
    await demo_mcp_stdio_client()
    
    # Business workflow examples
    workflows = BusinessWorkflowExamples()
    await workflows.compliance_audit_workflow()
    await workflows.customer_service_analytics()
    await workflows.sales_intelligence()
    
    print_header("Integration Guide Complete!")
    print("""
✅ Client Integration Options:

🌐 **HTTP REST API**
   - Best for: Web applications, external integrations
   - Start: python -m src.email_parser.transports --transport http
   - Endpoint: http://localhost:8000

🔌 **WebSocket**
   - Best for: Real-time applications, streaming
   - Start: python -m src.email_parser.transports --transport websocket  
   - Endpoint: ws://localhost:8001/ws/your-client-id

📡 **MCP Stdio** 
   - Best for: Claude Desktop, LLM integrations
   - Start: python -m src.email_parser.main --mcp
   - Protocol: Model Context Protocol over stdio

🚀 **Next Steps**:
   1. Choose your integration method
   2. Install network dependencies: uv pip install ".[network]"
   3. Start the appropriate server
   4. Build your email intelligence application!

💡 **Use Cases**:
   • Automated email classification and routing
   • Compliance monitoring and auditing  
   • Customer service analytics
   • Sales intelligence and CRM integration
   • Email-driven workflow automation
    """)

if __name__ == "__main__":
    asyncio.run(main())