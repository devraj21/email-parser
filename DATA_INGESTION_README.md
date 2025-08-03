# Data Ingestion System

A powerful system for ingesting varied customer demographic data files and mapping them to standardized target schema templates. **Now supports both Standard and BUPA Medical templates!**

## Overview

This data ingestion system can process multiple file formats (.csv, .xls, .xlsx) containing customer demographic data and automatically map the columns to your target schema. It supports **two template types**:

- **Standard Template**: Original demographic data template (`template/Data Template.xlsx`)
- **BUPA Medical Template**: UK Membership Template for BUPA medical changes (`template/Change files/UK Membership Template - BUPA update June 2025_MEDICAL.xlsx`)

The system handles:

- **Automatic Column Mapping**: Intelligently maps input columns to target schema based on column names
- **Data Standardization**: Cleans and standardizes data formats (dates, gender, names, etc.)
- **Multiple File Formats**: Supports CSV, XLS, and XLSX files
- **Batch Processing**: Process entire folders of files at once
- **Quality Validation**: Detects data quality issues and provides reports
- **Flexible Output**: Generate standardized Excel files in your target format

## Quick Start

### Installation

Ensure you have the required dependencies installed:

```bash
# Activate virtual environment
source .venv/bin/activate

# Install required packages
uv pip install pandas openpyxl xlrd
```

### Basic Usage

#### Standard Template (Default)
```bash
# Generate mapping analysis report
python data_ingestion_cli.py report --input "examples/Batchload files"

# Process all files in batch
python data_ingestion_cli.py process --input "examples/Batchload files" --output "output/standardized"

# Process single file
python data_ingestion_cli.py single --file "examples/Batchload files/Group 2.csv"

# Validate files for quality issues
python data_ingestion_cli.py validate --input "examples/Batchload files"
```

#### BUPA Medical Template
```bash
# Generate BUPA mapping analysis report
python data_ingestion_cli.py report --input "examples/Change files" --template bupa

# Process change files with BUPA template
python data_ingestion_cli.py process --input "examples/Change files" --output "output/bupa_standardized" --template bupa

# Process single change file with BUPA template
python data_ingestion_cli.py single --file "examples/Change files/Benifex Dental.csv" --template bupa

# Validate change files with BUPA template
python data_ingestion_cli.py validate --input "examples/Change files" --template bupa
```

## Target Schema Templates

The system supports two different target schema templates:

### Standard Template (`template/Data Template.xlsx`)

The original standardized template with 51 columns including:

### Core Fields
- **Group Number**: Insurance group identifier
- **Name**: Company/organization name
- **Client Ref.**: Unique client reference (employee number, etc.)
- **Location**: Geographic location
- **T.O.C**: Type of Cover (insurance coverage level)
- **Ni Number**: National Insurance number

### Personal Details
- **Surname**, **Forename**, **Title**: Personal names
- **Dob**: Date of birth
- **Sex**: Gender (standardized to Male/Female)
- **Address 1-4**: Address components
- **Post Code**: Postal code
- **Work Email Address**: Work email

### Family Information
- **Spouse Surname**, **S Forename**, **S Dob**, **S Sex**: Spouse details
- **Child 1-5 Surname/Forename/Dob/Sex**: Up to 5 children details

### BUPA Medical Template (`template/Change files/UK Membership Template - BUPA update June 2025_MEDICAL.xlsx`)

The BUPA-specific template with 80 columns for medical insurance changes, including:

#### BUPA Core Fields
- **Ind**: Action indicator (A=Addition, D=Deletion, C=Change)
- **Date**: Effective date of change
- **number**: Group number identifier
- **name**: Group/company name
- **Description**: Product description (Medical, Dental, etc.)
- **Reference**: Employee/client reference number

#### Personal Details (BUPA Format)
- **Surname**, **First Name**, **Title**: Primary member details
- **Date of Birth**: Birth date
- **Sex**: Gender
- **of Cover**: Type/level of coverage
- **Information**: Additional information (location, NI number, etc.)

#### Family Members (Multiple Relationships)
- **Relationship**: Type of relationship (Spouse, Child, etc.)
- **Surname1**, **First Name1**, **Title1**, **Sex1**, **Date of Birth1**: First dependent
- **Relationship2**, **Surname2**, **First Name2**, etc.: Additional dependents (up to 5+)

The BUPA template is designed for processing membership changes, additions, and deletions for medical insurance policies.

## File Processing Results

### Standard Template Processing
✅ **Group 1.xls** - 27.5% coverage (14/51 columns mapped)
✅ **Group 2.csv** - 56.9% coverage (29/51 columns mapped) 
✅ **Group 5.csv** - 49.0% coverage (25/51 columns mapped)
✅ **Group 7.xls** - 21.6% coverage (11/51 columns mapped)

⚠️ **Group 3.xls, Group 6.xls, Group 9.xls** - High coverage (74.5%) but data format issues
⚠️ **Group 4.xls, Group 8.xlsx** - No column mapping due to header structure issues

### BUPA Template Processing
✅ **Benifex Dental.csv** - 22.5% coverage (18/80 columns mapped)
✅ **Bupa Dental Changes File April 25.xlsx** - 22.5% coverage (18/80 columns mapped)
✅ **AON.xls** - 11.2% coverage (9/80 columns mapped)
✅ **Darwin IDT 2604799562 Dental-JLC.xls** - 8.8% coverage (7/80 columns mapped)

⚠️ **Darwin IDT 2607094844 PMI-JLC.xls** - No column mapping due to header structure issues

## Column Mapping Logic

The system uses intelligent fuzzy matching to map input columns to target schema. Mapping rules differ by template type:

### Standard Template Mappings
```
Input Column → Target Column
'Staff number' → 'Client Ref.'
'First name' → 'Forename'  
'Surname' → 'Surname'
'Date of birth' → 'Dob'
'Gender' → 'Sex'
'National insurance number' → 'Ni Number'
'Address line 1' → 'Address 1'
'Town' → 'Address 3'
'County' → 'Address 4'
'Post code' → 'Post Code'
'Dependant 1 first name' → 'Child 1 Forename'
'Child 2 Surname' → 'Child 2 Surname'
```

### BUPA Template Mappings
```
Input Column → Target Column
'Change' → 'Ind'
'Effective Date' → 'Date'
'Group No' → 'number'
'Group Name' → 'name'
'Product' → 'Description'
'Employee Number' → 'Reference'
'Forename' → 'First Name'
'Surname' → 'Surname'
'Date of Birth' → 'Date of Birth'
'Sex' → 'Sex'
'Type of Cover' → 'of Cover'
'Location' → 'Information'
'S Forename' → 'First Name1'
'Spouse Surname' → 'Surname1'
```

## Data Standardization

The system automatically:

- **Dates**: Converts to DD/MM/YYYY format
- **Gender**: Standardizes M/F to Male/Female
- **Names**: Applies title case formatting
- **Postcodes**: Converts to uppercase
- **Empty Values**: Handles null/empty cells appropriately

## Output Files

### Standard Template Output
Processed files are saved to `output/standardized/` as Excel files with:
- All 51 standard target schema columns
- Standardized data formatting
- Consistent structure across all files
- Only mapped data populated (unmapped columns remain empty)

### BUPA Template Output
Processed files are saved to `output/bupa_standardized/` as Excel files with:
- All 80 BUPA target schema columns
- BUPA-specific data formatting
- Consistent BUPA structure across all files
- Change indicators and effective dates properly formatted

## Quality Validation

The validation report identifies:
- Empty rows
- Duplicate records  
- Missing key fields (Client Ref, Surname, Forename)
- Column mapping coverage percentage

## Advanced Usage

### Programmatic Usage

```python
from data_ingestion_mapper import DataIngestionMapper

# Initialize with standard template (default)
mapper = DataIngestionMapper()
# or explicitly
mapper = DataIngestionMapper(template_type="standard")

# Initialize with BUPA template
mapper_bupa = DataIngestionMapper(template_type="bupa")

# Process single file
result_df = mapper.process_file("input.csv", "output.xlsx")

# Process batch
processed_files = mapper.process_batch("input_folder", "output_folder")

# Generate mapping report
report = mapper.generate_mapping_report("input_folder")
print(report)
```

### Custom Template

To use a different target schema template:

```python
# Use custom template path
mapper = DataIngestionMapper(template_type="standard", 
                           template_path="path/to/your/template.xlsx")

# Use custom BUPA template
mapper = DataIngestionMapper(template_type="bupa", 
                           template_path="path/to/your/bupa_template.xlsx")
```

## Troubleshooting

### Common Issues

1. **No Column Mappings Found**
   - Check if headers are in the first row
   - Some files may have headers in row 2 or 3
   - Verify column names match expected patterns

2. **Data Format Errors**
   - Usually related to mixed data types in columns
   - Check for non-text values in name fields
   - Verify date formats are recognizable

3. **Missing Dependencies**
   ```bash
   uv pip install pandas openpyxl xlrd
   ```

### File-Specific Issues

#### Standard Template Files
- **Group 4.xls, Group 8.xlsx**: Header detection issues - may need manual header row specification
- **Group 3.xls, Group 6.xls, Group 9.xls**: High mapping success but data type formatting issues

#### BUPA Template Files  
- **Darwin IDT 2607094844 PMI-JLC.xls**: Header detection issues - appears to have non-standard column structure
- **All BUPA files**: Lower coverage percentages are normal due to the 80-column template structure

## Next Steps

1. **Manual Review**: Check processed files in:
   - `output/standardized/` for standard template results
   - `output/bupa_standardized/` for BUPA template results
2. **Quality Control**: Review validation reports for data quality issues
3. **Integration**: Import standardized files into your target systems
4. **Template Selection**: Choose appropriate template type for your data source
5. **Customization**: Adjust column mappings for your specific needs

## Support

For issues with specific files or mapping logic, review the detailed logs and mapping reports generated by the system. The system provides comprehensive logging of all mapping decisions and data transformations.