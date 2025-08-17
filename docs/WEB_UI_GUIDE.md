# Web UI Guide

## Overview

The Web UI provides a simple browser-based interface for both email parsing and data ingestion functionality. It combines both features into a single, easy-to-use interface.

## Features

### Email Parser Section
- **Drag & Drop Upload**: Drop .msg files directly onto the upload area
- **Multi-file Processing**: Process multiple email files at once
- **Real-time Results**: See parsing results immediately
- **Entity Extraction**: Automatically extract emails, phones, dates, URLs
- **Categorization**: Automatic email classification

### Data Ingestion Section
- **Template Selection**: Choose from available processing templates
- **File Support**: Excel (.xlsx, .xls) and CSV files
- **Batch Processing**: Process multiple data files simultaneously
- **Configuration-Driven**: Uses existing JSON template configurations
- **Download Results**: Download processed files

## Getting Started

### 1. Install Dependencies

```bash
# Install network dependencies for web UI
source .venv/bin/activate
uv pip install ".[network]"
```

### 2. Start the Web UI

```bash
# Start on default port 8080
python web_ui.py

# Or specify custom host/port
python web_ui.py --host 0.0.0.0 --port 8080
```

### 3. Open in Browser

Navigate to: `http://localhost:8080`

## Usage

### Email Parsing
1. Select the "Email Parser" section (left side)
2. Drag .msg files onto the upload area or click to browse
3. Click "Parse Email Files" to process
4. View results showing:
   - Subject line
   - Sender information
   - Automatic categorization
   - Extracted entities

### Data Ingestion
1. Select the "Data Ingestion" section (right side)
2. Choose a template from the dropdown menu
3. Drag Excel/CSV files onto the upload area or click to browse
4. Click "Process Data Files" to process
5. View results and download processed files

## Templates

The Web UI automatically loads available templates from your `config/templates_config.json` file. Make sure you have your templates configured properly before using the data ingestion feature.

## API Endpoints

The Web UI also exposes REST API endpoints:

- `GET /` - Web interface
- `GET /health` - Health check
- `POST /api/email/upload` - Upload email files
- `POST /api/data/upload` - Upload data files
- `GET /api/data/templates` - Get available templates
- `GET /api/data/download/{file_id}` - Download processed files

## Troubleshooting

### Common Issues

1. **Import Errors**: Make sure you're in the project root and have activated the virtual environment
2. **Template Not Found**: Ensure `config/templates_config.json` exists with proper template definitions
3. **Upload Fails**: Check file formats (.msg for emails, .xlsx/.xls/.csv for data)
4. **Port Already in Use**: Use `--port` flag to specify a different port

### Logs

The application logs to the console. Look for error messages if uploads or processing fail.

## Architecture

The Web UI consists of:

- **FastAPI Backend**: Handles file uploads and processing
- **Single-page Frontend**: HTML/CSS/JavaScript interface
- **MCP Integration**: Uses existing email parser MCP server
- **Data Ingestion Integration**: Uses existing configuration-driven mapper

## Security Notes

- The Web UI runs on localhost by default for security
- Uploaded files are temporarily stored and cleaned up after processing
- Use `--host 0.0.0.0` only if you need external access (consider firewall rules)

## Development

To modify the UI:

1. Edit `src/web_ui.py` for backend changes
2. The HTML template is embedded in the Python file
3. Restart the server to see changes
4. Consider extracting HTML to separate files for larger modifications