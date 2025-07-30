"""
Network transports for MCP Server
Provides HTTP and WebSocket support for remote clients
"""

import asyncio
import json
import logging
from typing import Any, Dict, Optional
from pathlib import Path

try:
    import uvicorn
    from fastapi import FastAPI, WebSocket, HTTPException
    from fastapi.middleware.cors import CORSMiddleware
    from fastapi.responses import JSONResponse
except ImportError:
    print("Warning: FastAPI/uvicorn not installed. Install with: uv pip install fastapi uvicorn")
    FastAPI = None

from .mcp_server import EmailParserMCPServer

logger = logging.getLogger(__name__)

class HTTPTransport:
    """HTTP transport for MCP server"""
    
    def __init__(self, mcp_server: EmailParserMCPServer, host: str = "localhost", port: int = 8000):
        if FastAPI is None:
            raise ImportError("FastAPI is required for HTTP transport. Install with: uv pip install fastapi uvicorn")
        
        self.mcp_server = mcp_server
        self.host = host
        self.port = port
        self.app = FastAPI(
            title="Email Parser MCP Server",
            description="MCP Server for email parsing and analysis",
            version="1.0.0"
        )
        
        # Add CORS middleware
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup HTTP API routes"""
        
        @self.app.get("/")
        async def root():
            return {
                "name": "Email Parser MCP Server",
                "version": "1.0.0",
                "status": "running",
                "endpoints": {
                    "parse_file": "/api/parse/file",
                    "parse_folder": "/api/parse/folder", 
                    "analyze_patterns": "/api/analyze/patterns",
                    "extract_entities": "/api/extract/entities",
                    "health": "/health"
                }
            }
        
        @self.app.get("/health")
        async def health_check():
            return {"status": "healthy", "service": "email-parser-mcp"}
        
        @self.app.post("/api/parse/file")
        async def parse_file_endpoint(request: Dict[str, Any]):
            """Parse a single email file"""
            try:
                file_path = request.get("file_path")
                if not file_path:
                    raise HTTPException(status_code=400, detail="file_path is required")
                
                # Use the MCP server's tool directly
                result = await self._call_mcp_tool("parse_email_file", {"file_path": file_path})
                return result
                
            except Exception as e:
                logger.error(f"Error in parse_file_endpoint: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/parse/folder")
        async def parse_folder_endpoint(request: Dict[str, Any]):
            """Parse all emails in a folder"""
            try:
                folder_path = request.get("folder_path")
                output_format = request.get("output_format", "summary")
                
                if not folder_path:
                    raise HTTPException(status_code=400, detail="folder_path is required")
                
                result = await self._call_mcp_tool("parse_email_folder", {
                    "folder_path": folder_path,
                    "output_format": output_format
                })
                return result
                
            except Exception as e:
                logger.error(f"Error in parse_folder_endpoint: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/analyze/patterns")
        async def analyze_patterns_endpoint(request: Dict[str, Any]):
            """Analyze email patterns"""
            try:
                folder_path = request.get("folder_path")
                analysis_type = request.get("analysis_type", "categories")
                
                if not folder_path:
                    raise HTTPException(status_code=400, detail="folder_path is required")
                
                result = await self._call_mcp_tool("analyze_email_patterns", {
                    "folder_path": folder_path,
                    "analysis_type": analysis_type
                })
                return result
                
            except Exception as e:
                logger.error(f"Error in analyze_patterns_endpoint: {e}")
                raise HTTPException(status_code=500, detail=str(e))
        
        @self.app.post("/api/extract/entities")
        async def extract_entities_endpoint(request: Dict[str, Any]):
            """Extract entities from text"""
            try:
                text = request.get("text")
                if not text:
                    raise HTTPException(status_code=400, detail="text is required")
                
                result = await self._call_mcp_tool("extract_entities_from_text", {"text": text})
                return result
                
            except Exception as e:
                logger.error(f"Error in extract_entities_endpoint: {e}")
                raise HTTPException(status_code=500, detail=str(e))
    
    async def _call_mcp_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool and return the result"""
        try:
            # Access the tools from the MCP server
            tools = self.mcp_server.mcp._tools
            if tool_name not in tools:
                raise ValueError(f"Tool {tool_name} not found")
            
            tool_func = tools[tool_name].func
            result = tool_func(**args)
            
            # Handle async tools if needed
            if asyncio.iscoroutine(result):
                result = await result
            
            return result
            
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def run(self):
        """Run the HTTP server"""
        logger.info(f"Starting HTTP transport on {self.host}:{self.port}")
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

class WebSocketTransport:
    """WebSocket transport for MCP server"""
    
    def __init__(self, mcp_server: EmailParserMCPServer, host: str = "localhost", port: int = 8001):
        if FastAPI is None:
            raise ImportError("FastAPI is required for WebSocket transport")
        
        self.mcp_server = mcp_server
        self.host = host
        self.port = port
        self.app = FastAPI(title="Email Parser MCP WebSocket Server")
        self.active_connections: Dict[str, WebSocket] = {}
        
        self._setup_websocket_routes()
    
    def _setup_websocket_routes(self):
        """Setup WebSocket routes"""
        
        @self.app.websocket("/ws/{client_id}")
        async def websocket_endpoint(websocket: WebSocket, client_id: str):
            await websocket.accept()
            self.active_connections[client_id] = websocket
            logger.info(f"Client {client_id} connected via WebSocket")
            
            try:
                while True:
                    # Receive message from client
                    message = await websocket.receive_text()
                    request_data = json.loads(message)
                    
                    # Process the request
                    response = await self._process_websocket_request(request_data)
                    
                    # Send response back
                    await websocket.send_text(json.dumps(response))
                    
            except Exception as e:
                logger.error(f"WebSocket error for client {client_id}: {e}")
            finally:
                if client_id in self.active_connections:
                    del self.active_connections[client_id]
                logger.info(f"Client {client_id} disconnected")
        
        @self.app.get("/ws/status")
        async def websocket_status():
            return {
                "active_connections": len(self.active_connections),
                "connected_clients": list(self.active_connections.keys())
            }
    
    async def _process_websocket_request(self, request_data: Dict[str, Any]) -> Dict[str, Any]:
        """Process WebSocket request"""
        try:
            action = request_data.get("action")
            params = request_data.get("params", {})
            request_id = request_data.get("request_id")
            
            # Map actions to MCP tools
            tool_mapping = {
                "parse_file": "parse_email_file",
                "parse_folder": "parse_email_folder",
                "analyze_patterns": "analyze_email_patterns",
                "extract_entities": "extract_entities_from_text"
            }
            
            if action not in tool_mapping:
                return {
                    "request_id": request_id,
                    "error": f"Unknown action: {action}",
                    "available_actions": list(tool_mapping.keys())
                }
            
            tool_name = tool_mapping[action]
            result = await self._call_mcp_tool(tool_name, params)
            
            return {
                "request_id": request_id,
                "action": action,
                "result": result,
                "status": "success"
            }
            
        except Exception as e:
            logger.error(f"Error processing WebSocket request: {e}")
            return {
                "request_id": request_data.get("request_id"),
                "error": str(e),
                "status": "error"
            }
    
    async def _call_mcp_tool(self, tool_name: str, args: Dict[str, Any]) -> Dict[str, Any]:
        """Call an MCP tool (same as HTTP transport)"""
        try:
            tools = self.mcp_server.mcp._tools
            if tool_name not in tools:
                raise ValueError(f"Tool {tool_name} not found")
            
            tool_func = tools[tool_name].func
            result = tool_func(**args)
            
            if asyncio.iscoroutine(result):
                result = await result
            
            return result
            
        except Exception as e:
            logger.error(f"Error calling MCP tool {tool_name}: {e}")
            return {"error": str(e)}
    
    async def broadcast_message(self, message: Dict[str, Any]):
        """Broadcast message to all connected clients"""
        if not self.active_connections:
            return
        
        message_text = json.dumps(message)
        disconnected_clients = []
        
        for client_id, websocket in self.active_connections.items():
            try:
                await websocket.send_text(message_text)
            except Exception as e:
                logger.error(f"Failed to send message to client {client_id}: {e}")
                disconnected_clients.append(client_id)
        
        # Clean up disconnected clients
        for client_id in disconnected_clients:
            del self.active_connections[client_id]
    
    async def run(self):
        """Run the WebSocket server"""
        logger.info(f"Starting WebSocket transport on {self.host}:{self.port}")
        
        config = uvicorn.Config(
            app=self.app,
            host=self.host,
            port=self.port,
            log_level="info"
        )
        server = uvicorn.Server(config)
        await server.serve()

# Convenience functions
async def start_http_server(host: str = "localhost", port: int = 8000):
    """Start HTTP transport server"""
    mcp_server = EmailParserMCPServer()
    transport = HTTPTransport(mcp_server, host, port)
    await transport.run()

async def start_websocket_server(host: str = "localhost", port: int = 8001):
    """Start WebSocket transport server"""
    mcp_server = EmailParserMCPServer()
    transport = WebSocketTransport(mcp_server, host, port)
    await transport.run()

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Email Parser MCP Network Transports")
    parser.add_argument("--transport", choices=["http", "websocket"], default="http")
    parser.add_argument("--host", default="localhost")
    parser.add_argument("--port", type=int, default=8000)
    
    args = parser.parse_args()
    
    if args.transport == "http":
        asyncio.run(start_http_server(args.host, args.port))
    elif args.transport == "websocket":
        port = args.port if args.port != 8000 else 8001  # Default WebSocket port
        asyncio.run(start_websocket_server(args.host, port))