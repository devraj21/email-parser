#!/usr/bin/env python3
"""
Simple test script for MCP server functionality
"""

import asyncio
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

async def test_mcp_server():
    """Test MCP server initialization and basic functionality"""
    try:
        from email_parser.mcp_server import EmailParserMCPServer
        
        print("🚀 Initializing MCP Server...")
        server = EmailParserMCPServer()
        print("✅ MCP Server initialized successfully!")
        
        # Test entity extraction directly through the parser
        print("\n🔍 Testing entity extraction...")
        sample_text = "Contact john@example.com or call 555-123-4567. Budget: $10,000"
        entities = server.parser._extract_entities(sample_text)
        print(f"📧 Extracted entities: {entities}")
        
        # Test email categorization
        print("\n🏷️ Testing email categorization...")
        subject = "URGENT: Meeting tomorrow"
        body = "Please attend the important meeting tomorrow at 2 PM"
        categories = server.parser._categorize_email(subject, body, [])
        print(f"📋 Categories: {categories}")
        
        print("\n✅ All basic tests passed!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Make sure fastmcp is installed: uv pip install fastmcp")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

async def test_network_transports():
    """Test network transport availability"""
    try:
        print("\n🌐 Testing network transport dependencies...")
        
        import fastapi
        print(f"✅ FastAPI: {fastapi.__version__}")
        
        import uvicorn
        print(f"✅ Uvicorn: {uvicorn.__version__}")
        
        import websockets
        print(f"✅ WebSockets: {websockets.__version__}")
        
        print("✅ All network dependencies available!")
        return True
        
    except ImportError as e:
        print(f"❌ Network dependency missing: {e}")
        print("Install with: uv pip install \".[network]\"")
        return False

async def main():
    """Run all tests"""
    print("🧪 Email Parser MCP Server - Test Suite")
    print("=" * 50)
    
    # Test basic MCP server
    mcp_success = await test_mcp_server()
    
    # Test network transports
    network_success = await test_network_transports()
    
    print("\n" + "=" * 50)
    if mcp_success and network_success:
        print("🎉 All tests passed! MCP server is ready to use.")
        print("\nNext steps:")
        print("1. Start MCP server: python -m src.email_parser.main --mcp")
        print("2. Start HTTP server: python -m src.email_parser.transports --transport http")
        print("3. Test client integration: python examples/client_integration.py")
    else:
        print("❌ Some tests failed. Please check the error messages above.")

if __name__ == "__main__":
    asyncio.run(main())