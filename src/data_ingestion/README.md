# Data Ingestion Module

A configuration-driven system for processing Excel/CSV files and mapping them to standardized templates.

## Structure

```
src/data_ingestion/
├── __init__.py          # Module exports
├── cli.py              # Command-line interface
├── config_manager.py   # Configuration file manager
├── mapper.py           # Core data ingestion mapper
└── README.md           # This file
```

## Features

- **Configuration-Driven**: Uses JSON configuration files to define templates and mappings
- **Multiple Templates**: Supports different target schemas (Batchload, BUPA Medical, etc.)
- **Smart Column Mapping**: Intelligent fuzzy matching of input columns to target schema
- **Data Transformation**: Automatic standardization (dates, names, postcodes, gender)
- **Pattern Recognition**: Handles complex patterns like children/dependant relationships
- **Quality Reporting**: Detailed analysis of mapping coverage and data quality

## Usage

### Command Line Interface

```bash
# Using the convenience script from project root
python data_ingestion_cli.py --help

# Available commands:
python data_ingestion_cli.py create-config              # Create default config files
python data_ingestion_cli.py validate-config            # Validate configuration
python data_ingestion_cli.py auto-process               # Process all files automatically
python data_ingestion_cli.py report --input "folder"    # Generate mapping report
python data_ingestion_cli.py single --file "file.xlsx"  # Process single file
```

### Python API

```python
from data_ingestion import ConfigurableDataIngestionMapper, ConfigurationManager

# Create mapper with configuration
mapper = ConfigurableDataIngestionMapper(config_dir="config")

# Process single file
result_df = mapper.process_file("input.xlsx", "output.xlsx")

# Batch process with auto-detection
results = mapper.process_batch_auto(base_output_dir="output")

# Generate analysis report
report = mapper.generate_mapping_report("input_folder")
```

## Configuration Files

The system uses JSON configuration files located in the `config/` directory:

- **`templates_config.json`**: Template definitions, column mappings, and data transformations
- **`file_mappings.json`**: File-to-template mapping rules and processing options

## Dependencies

- `pandas`: DataFrame processing
- `openpyxl`: Excel file reading/writing
- `xlrd`: Legacy Excel file support

Install with:
```bash
pip install pandas openpyxl xlrd
```

## Template Types

### Template 1: Batchload Data Template
- **Use Case**: General customer demographic data
- **Target Schema**: 51 columns (personal details, addresses, family info)
- **File Pattern**: `examples/Batchload files/*.{csv,xls,xlsx}`

### Template 2: UK Membership Template (BUPA Medical)
- **Use Case**: Medical insurance membership changes
- **Target Schema**: 80 columns (medical insurance processing)
- **File Pattern**: `examples/Change files/*.{csv,xls,xlsx}`

## Output

The system generates:
- **Standardized Excel Files**: In consistent template format
- **Processing Reports**: JSON and human-readable summaries
- **Quality Metrics**: Coverage analysis and data validation results

Reports are saved to the `reports/` directory with detailed processing information.
