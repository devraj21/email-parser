# Configuration-Driven Data Ingestion System

A comprehensive, JSON-configurable data ingestion system that allows users to define templates, column mappings, and file processing rules without modifying code.

## 🎯 Overview

The configuration-driven system provides:

- **📋 Template Management**: Define multiple target templates via JSON
- **🗂️ File Mapping**: Automatically route files to appropriate templates
- **🔧 Column Mapping**: Flexible column mapping rules with pattern matching
- **⚙️ Data Transformation**: Configurable data cleaning and standardization
- **🚀 Auto-Processing**: One-command processing of all configured files
- **📊 Validation & Reporting**: Configuration validation and detailed mapping reports

## 🛠️ Quick Start

### 1. Create Configuration Files

```bash
# Create default configuration files
python data_ingestion_cli_v2.py create-config

# Validate configuration
python data_ingestion_cli_v2.py validate-config
```

### 2. Process Files Automatically

```bash
# Process all files based on configuration
python data_ingestion_cli_v2.py auto-process

# Generate mapping report
python data_ingestion_cli_v2.py report --input "examples/Batchload files"
```

### 3. Process Individual Files

```bash
# Auto-detect template
python data_ingestion_cli_v2.py single --file "data.csv"

# Force specific template
python data_ingestion_cli_v2.py single --file "data.csv" --template medical_changes
```

## 📁 Configuration Files

### `config/templates_config.json`

Defines templates, column mappings, and data transformations:

```json
{
  "version": "1.0",
  "templates": {
    "standard": {
      "name": "Standard Demographic Template",
      "template_file": "template/Batchload files/Batchload Data Template.xlsx",
      "data_transformations": {
        "date_format": "DD/MM/YYYY",
        "gender_standardization": {"M": "Male", "F": "Female"}
      }
    },
    "medical_changes": {
      "name": "Medical Changes Template", 
      "template_file": "template/Change files/UK Membership Template - BUPA update June 2025_MEDICAL.xlsx",
      "sheet_name": "For Use",
      "use_first_row_as_headers": true
    }
  },
  "column_mappings": {
    "standard": {
      "personal_details": {
        "Surname": ["Surname", "SURNAME", "surname", "last_name"],
        "Forename": ["Forename", "first_name", "ForeNames"]
      }
    }
  }
}
```

### `config/file_mappings.json`

Defines which files use which templates:

```json
{
  "file_mappings": [
    {
      "name": "Standard Batch Files",
      "template": "standard",
      "input_patterns": [
        "examples/Batchload files/Group*.csv",
        "examples/Batchload files/Group*.xls"
      ],
      "output_folder": "output/standard"
    },
    {
      "name": "Medical Change Files", 
      "template": "medical_changes",
      "input_patterns": [
        "examples/Change files/*.csv",
        "examples/Change files/*.xls"  
      ],
      "output_folder": "output/medical_changes"
    }
  ]
}
```

## 🔧 Adding New Templates

### Step 1: Add Template Definition

Edit `config/templates_config.json`:

```json
{
  "templates": {
    "my_template": {
      "name": "My Custom Template",
      "description": "Template for my specific data format",
      "template_file": "templates/my_template.xlsx",
      "sheet_name": null,
      "header_row": 0,
      "output_suffix": "_custom",
      "data_transformations": {
        "date_format": "YYYY-MM-DD",
        "name_case": "title"
      }
    }
  }
}
```

### Step 2: Define Column Mappings

Add to the `column_mappings` section:

```json
{
  "column_mappings": {
    "my_template": {
      "basic_info": {
        "Customer_ID": ["id", "customer_id", "cust_id"],
        "Full_Name": ["name", "customer_name", "full_name"],
        "Email": ["email", "email_address", "contact_email"]
      },
      "address": {
        "Street": ["address", "address_1", "street"],
        "City": ["city", "town"],
        "Zip": ["zip", "postal_code", "postcode"]
      }
    }
  }
}
```

### Step 3: Add File Mapping

Edit `config/file_mappings.json`:

```json
{
  "file_mappings": [
    {
      "name": "My Custom Files",
      "template": "my_template", 
      "input_patterns": [
        "data/custom/*.csv",
        "imports/my_data*.xlsx"
      ],
      "exclude_patterns": [
        "**/template*.xlsx"
      ],
      "output_folder": "output/custom",
      "enabled": true
    }
  ]
}
```

### Step 4: Test Configuration

```bash
# Validate your changes
python data_ingestion_cli_v2.py validate-config

# List available templates
python data_ingestion_cli_v2.py list-templates

# Test with a sample file
python data_ingestion_cli_v2.py single --file "data/test.csv" --template my_template
```

## 🎛️ Advanced Configuration

### Pattern-Based Column Mapping

For dynamic columns like children/dependants:

```json
{
  "children_patterns": {
    "forename": ["child\\s*(\\d+)\\s*forename", "dependant\\s*(\\d+)\\s*first\\s*name"],
    "surname": ["child\\s*(\\d+)\\s*surname", "dependant\\s*(\\d+)\\s*surname"],
    "max_children": 5
  }
}
```

### Auto-Detection Rules

Configure automatic template detection:

```json
{
  "auto_detection": {
    "enabled": true,
    "detection_rules": [
      {
        "template": "medical_changes",
        "conditions": {
          "required_columns": ["Change", "Effective Date", "Group No"],
          "column_count_range": [60, 100]
        }
      }
    ]
  }
}
```

### File-Specific Overrides

Override template for specific files:

```json
{
  "specific_file_overrides": {
    "overrides": {
      "examples/special_file.xlsx": "custom_template",
      "data/medical_formatted.csv": "medical_changes"
    }
  }
}
```

## 📊 CLI Commands

### Configuration Management

```bash
# Create default configuration
python data_ingestion_cli_v2.py create-config

# Validate configuration
python data_ingestion_cli_v2.py validate-config

# List available templates
python data_ingestion_cli_v2.py list-templates
```

### File Processing

```bash
# Auto-process all configured files
python data_ingestion_cli_v2.py auto-process

# Process with custom output directory
python data_ingestion_cli_v2.py auto-process --output "results"

# Process single file
python data_ingestion_cli_v2.py single --file "data.csv"

# Force specific template
python data_ingestion_cli_v2.py single --file "data.csv" --template medical_changes --output "result.xlsx"
```

### Analysis & Reporting

```bash
# Generate mapping report for folder
python data_ingestion_cli_v2.py report --input "examples/Batchload files"

# Generate comprehensive report
python data_ingestion_cli_v2.py report
```

## 🔍 Configuration Schema Reference

### Template Configuration

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Human-readable template name |
| `description` | string | Template description |
| `template_file` | string | Path to Excel template file |
| `sheet_name` | string/null | Specific sheet name to read |
| `header_row` | number | Row number containing headers (0-based) |
| `use_first_row_as_headers` | boolean | Use first data row as column headers |
| `output_suffix` | string | Suffix for output filenames |

### Data Transformations

| Field | Type | Description |
|-------|------|-------------|
| `date_format` | string | Output date format ("DD/MM/YYYY" or "YYYY-MM-DD") |
| `gender_standardization` | object | Gender value mappings |
| `name_case` | string | Name formatting ("title", "upper", "lower") |
| `postcode_case` | string | Postcode formatting ("upper", "lower") |

### File Mapping Configuration

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Mapping rule name |
| `template` | string | Template to use |
| `input_patterns` | array | Glob patterns for input files |
| `exclude_patterns` | array | Patterns to exclude |
| `output_folder` | string | Output directory |
| `enabled` | boolean | Enable/disable this mapping |

## 🚀 Integration Examples

### Programmatic Usage

```python
from data_ingestion_mapper_v2 import ConfigurableDataIngestionMapper

# Initialize with custom config directory
mapper = ConfigurableDataIngestionMapper(config_dir="my_config")

# Process single file
result = mapper.process_file("data.csv", "output.xlsx")

# Process all configured files
results = mapper.process_batch_auto()

# Generate report
report = mapper.generate_mapping_report("data_folder")
print(report)
```

### Custom Configuration Loading

```python
from config_manager import ConfigurationManager

# Load configuration
config = ConfigurationManager("my_config")

# Validate
errors = config.validate_configuration()
if errors:
    print("Configuration errors:", errors)

# Get available templates
templates = config.get_available_templates()

# Resolve template for file
template = config.resolve_file_template("data.csv")
```

## 🛠️ Troubleshooting

### Common Issues

1. **Template file not found**
   ```
   Error: Template file not found for 'standard': template/Data Template.xlsx
   ```
   - Check file path in `templates_config.json`
   - Ensure template file exists

2. **Unknown template reference**
   ```
   Error: File mapping references unknown template: my_template
   ```
   - Add template definition to `templates_config.json`
   - Or disable the mapping by setting `"enabled": false`

3. **Sheet not found** 
   ```
   Error: Worksheet named 'For Use' not found
   ```
   - Set `"sheet_name": null` for default sheet
   - Or verify sheet name in Excel file

4. **No files processed**
   ```
   Warning: No files were processed. Check your configuration and file patterns.
   ```
   - Verify input patterns match actual file locations
   - Check exclude patterns aren't too broad
   - Ensure mappings are enabled

### Debugging Tips

- Use `validate-config` to check configuration
- Run `list-templates` to see available templates  
- Test with `single` command before batch processing
- Check file patterns with `report` command
- Review logs for detailed mapping information

## 📋 Migration from Old System

### From Template-Based CLI

Old approach:
```bash
python data_ingestion_cli.py process --input "files" --template medical_changes
```

New approach:
```bash
# Configure once in JSON files, then:
python data_ingestion_cli_v2.py auto-process
```

### Configuration Migration

1. **Extract existing mappings** from old `data_ingestion_mapper.py`
2. **Convert to JSON format** in `templates_config.json`
3. **Define file patterns** in `file_mappings.json`
4. **Test and validate** with new CLI

The configuration system provides much more flexibility and maintainability compared to the hardcoded template approach, making it easy to adapt to new data sources and requirements without code changes.