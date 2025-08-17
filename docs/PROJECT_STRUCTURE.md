# Email Parser Project Structure

## Overview

This project contains two main systems:
1. **Email Parser with MCP Server** - For parsing email files and AI analysis
2. **Data Ingestion System** - For Excel/CSV file processing and template mapping

## Directory Structure

```
email-parser/
├── src/
│   ├── email_parser/          # Email parsing and MCP server
│   │   ├── __init__.py
│   │   ├── ai_integration.py  # AI analysis with Ollama
│   │   ├── main.py           # Main MCP server entry point
│   │   ├── mcp_server.py     # MCP server implementation
│   │   ├── parser.py         # Email parsing logic
│   │   └── transports.py     # HTTP/WebSocket transports
│   │
│   └── data_ingestion/        # Excel/CSV processing system
│       ├── __init__.py
│       ├── cli.py            # Command-line interface
│       ├── config_manager.py # Configuration file manager
│       ├── mapper.py         # Core data mapping engine
│       └── README.md         # Data ingestion documentation
│
├── config/                    # Configuration files
│   ├── templates_config.json # Template definitions
│   └── file_mappings.json    # File-to-template mappings
│
├── template/                  # Excel template files
│   ├── Batchload files/
│   └── Change files/
│
├── reports/                   # Generated processing reports
├── output/                    # Processed file outputs
├── examples/                  # Sample files for testing
│
├── email_cli.py              # Email parser CLI (convenience script)
├── data_ingestion_cli.py     # Data ingestion CLI (convenience script)
├── pyproject.toml            # Project dependencies
└── README.md                 # Main project documentation
```

## Systems Overview

### 1. Email Parser System (`src/email_parser/`)

**Purpose**: Parse .msg email files and provide AI-powered analysis through various interfaces

**Key Features**:
- Parse .msg email files
- Extract entities (emails, phones, dates, etc.)
- AI analysis with Ollama Phi3
- MCP server for Claude Desktop integration
- HTTP/WebSocket APIs for web applications

**Entry Points**:
- `python email_cli.py` - CLI interface
- `python -m src.email_parser.main --mcp` - MCP server
- `python -m src.email_parser.transports --http` - HTTP server

### 2. Data Ingestion System (`src/data_ingestion/`)

**Purpose**: Process Excel/CSV files and map them to standardized templates

**Key Features**:
- Configuration-driven column mapping
- Multiple template support (Batchload, BUPA Medical)
- Smart fuzzy matching of column names
- Data transformation and standardization
- Quality reporting and analysis

**Entry Points**:
- `python data_ingestion_cli.py` - CLI interface
- Import `from data_ingestion import ConfigurableDataIngestionMapper`

## Configuration System

### Email Parser Configuration
- AI integration settings in source files
- MCP server configuration via command line arguments

### Data Ingestion Configuration
- **`config/templates_config.json`**: Template definitions, column mappings, transformations
- **`config/file_mappings.json`**: File pattern matching and processing rules

## Usage Examples

### Email Parser
```bash
# Parse single email
python email_cli.py parse-file email.msg --format json

# Start MCP server for Claude Desktop
python email_cli.py server --mcp

# AI analysis of email folder
python email_cli.py ai-analyze categorize ./emails --auto-save
```

### Data Ingestion
```bash
# Create configuration files
python data_ingestion_cli.py create-config

# Process files automatically
python data_ingestion_cli.py auto-process

# Generate mapping report
python data_ingestion_cli.py report --input "examples/Batchload files"

# Process single file
python data_ingestion_cli.py single --file "data.xlsx"
```

## Dependencies

### Core Dependencies
- `pandas` - DataFrame processing
- `openpyxl` - Excel file handling
- `extract-msg` - Email file parsing
- `fastmcp` - MCP server implementation

### Optional Dependencies
- `fastapi`, `uvicorn` - HTTP/WebSocket servers
- `ollama` - AI analysis integration
- `websockets` - WebSocket client support

## Development

Both systems are designed to be modular and extensible:

- **Email Parser**: Add new transport methods or AI integrations
- **Data Ingestion**: Add new templates via JSON configuration

The structured approach in `src/` allows for clean imports and better organization while maintaining backward compatibility through convenience scripts in the project root.
