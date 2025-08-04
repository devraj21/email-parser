#!/usr/bin/env python3
"""
Data Ingestion Mapper - Maps varied input files to standard target schema template.

This module handles:
1. Reading various input file formats (.csv, .xls, .xlsx)
2. Mapping columns from input files to target schema template
3. Data transformation and validation
4. Output generation in target format
"""

import pandas as pd
import os
import re
from typing import Dict, List, Tuple, Any, Optional
from datetime import datetime
import logging

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class DataIngestionMapper:
    """
    Maps various customer demographic data files to a standardized template.
    Supports multiple template types: 'standard' and 'bupa'.
    """
    
    def __init__(self, template_type: str = "standard", template_path: str = None):
        """
        Initialize the mapper with the target template.
        
        Args:
            template_type: Type of template ('standard' or 'bupa')
            template_path: Optional custom path to template file
        """
        self.template_type = template_type
        
        # Set default template paths based on type
        if template_path is None:
            if template_type == "bupa":
                self.template_path = "template/Change files/UK Membership Template - BUPA update June 2025_MEDICAL.xlsx"
            else:  # standard
                self.template_path = "template/Data Template.xlsx"
        else:
            self.template_path = template_path
            
        self.target_columns = self._load_target_schema()
        self.column_mappings = self._create_column_mappings()
        
    def _load_target_schema(self) -> List[str]:
        """Load the target schema column structure from template."""
        try:
            if self.template_type == "bupa":
                # For BUPA template, read from 'For Use' sheet and use first row as headers
                df_template = pd.read_excel(self.template_path, sheet_name='For Use')
                if len(df_template) > 0:
                    # Extract proper column names from first row
                    bupa_columns = []
                    for i, col in enumerate(df_template.columns):
                        potential_header = df_template.iloc[0, i] if pd.notna(df_template.iloc[0, i]) else None
                        if potential_header and str(potential_header) != 'nan' and not str(col).startswith('Unnamed'):
                            bupa_columns.append(str(potential_header))
                        elif not str(col).startswith('Unnamed'):
                            bupa_columns.append(str(col))
                        else:
                            bupa_columns.append(f'Column_{i+1}')
                    return bupa_columns
                else:
                    return df_template.columns.tolist()
            else:
                # Standard template
                df_template = pd.read_excel(self.template_path)
                return df_template.columns.tolist()
                
        except Exception as e:
            logger.error(f"Error loading target schema: {e}")
            # Fallback schemas based on template type
            if self.template_type == "bupa":
                return self._get_bupa_fallback_schema()
            else:
                return self._get_standard_fallback_schema()
    
    def _get_standard_fallback_schema(self) -> List[str]:
        """Fallback schema for standard template."""
        return [
            'Group Number', 'Name', 'Client Ref.', 'Hmc Blank', 'Location', 'Scale', 'T.O.C',
            'Ni Number', 'Surname', 'Initial', 'Forename', 'Title', 'Dob', 'Sex',
            'Address 1', 'Address 2', 'Address 3', 'Address 4', 'Post Code', 'Work Email Address',
            'Spouse Surname', 'S Initial', 'S Forename', 'S Dob', 'S Sex', 'No of Deps',
            'Child 1 Surname', 'Child 1 Initial', 'Child 1 Forename', 'Child 1 Dob', 'Child 1 Sex',
            'Child 2 Surname', 'Child 2 Initial', 'Child 2 Forename', 'Child 2 Dob', 'Child 2 Sex',
            'Child 3 Surname', 'Child 3 Initial', 'Child 3 Forename', 'Child 3 Dob', 'Child 3 Sex',
            'Child 4 Surname', 'Child 4 Initial', 'Child 4 Forename', 'Child 4 Dob', 'Child 4 Sex',
            'Child 5 Surname', 'Child 5 Initial', 'Child 5 Forename', 'Child 5 Dob', 'Child 5 Sex'
        ]
    
    def _get_bupa_fallback_schema(self) -> List[str]:
        """Fallback schema for BUPA template based on analysis."""
        return [
            'Ind', 'Date', 'number', 'name', 'Description', 'Reference', 'Column_7', 'Column_8',
            'Column_9', 'Column_10', 'Column_11', 'Column_12', 'Column_13', 'Column_14', 'Column_15',
            'Column_16', 'Column_17', 'Column_18', 'Information', 'of Cover', 'Relationship',
            'Surname', 'First Name', 'Title', 'Sex', 'Date of Birth', 'Relationship1', 'Surname1',
            'First Name1', 'Title1', 'Sex1', 'Date of Birth1', 'Relationship2', 'Surname2',
            'First Name2', 'Title2', 'Sex2', 'Date of Birth2', 'Relationship3', 'Surname3',
            'First Name3', 'Title3', 'Sex3', 'Date of Birth3', 'Relationship4', 'Surname4',
            'First Name4', 'Title4', 'Sex4', 'Date of Birth4', 'Relationship5', 'Surname5'
        ]  # Truncated for brevity - would include all 80 columns
    
    def _create_column_mappings(self) -> Dict[str, List[str]]:
        """
        Create mapping rules from common input column names to target schema.
        
        Returns:
            Dictionary mapping target columns to possible input column names
        """
        if self.template_type == "bupa":
            return self._create_bupa_mappings()
        else:
            return self._create_standard_mappings()
    
    def _create_standard_mappings(self) -> Dict[str, List[str]]:
        """Create mappings for standard template."""
        return {
            # Basic demographic info
            'Group Number': ['Group No', 'group_number', 'group no', 'scheme_number', 'Scheme Number'],
            'Name': ['Name', 'name', 'company_name', 'Company Name'],
            'Client Ref.': ['Client Ref', 'client_ref', 'payroll_number', 'Payroll Number', 'staff_number', 'Staff number'],
            'Location': ['Location', 'LOCATION', 'location', 'geographical_location', 'Geographical Location'],
            'T.O.C': ['Type of Cover', 'TOC', 'Level Of Cover', 'level_of_cover', 'Option selected'],
            'Ni Number': ['National Insurance', 'ni_number', 'NI Number', 'NiNumber', 'National insurance number'],
            
            # Personal details
            'Surname': ['Surname', 'SURNAME', 'surname', 'last_name'],
            'Forename': ['Forename', 'FORENAME', 'forename', 'first_name', 'First name', 'ForeNames'],
            'Title': ['Title', 'TITLE', 'title'],
            'Dob': ['DOB', 'dob', 'Date of Birth', 'date_of_birth', 'DateOfBirth'],
            'Sex': ['Sex', 'sex', 'Gender', 'gender', 'GENDER'],
            
            # Address fields
            'Address 1': ['Address 1', 'address_1', 'address1', 'Building', 'Street', 'Address line 1'],
            'Address 2': ['Address 2', 'address_2', 'address2', 'Sub-Street', 'Address line 2'],
            'Address 3': ['Address 3', 'address_3', 'address3', 'City/Town', 'Town', 'Address line 3'],
            'Address 4': ['Address 4', 'address_4', 'address4', 'County', 'State'],
            'Post Code': ['POST CODE', 'Post Code', 'post_code', 'postcode', 'Postcode', 'Post code'],
            
            # Contact info
            'Work Email Address': ['WORK EMAIL ADDRESS', 'work_email', 'Work Email', 'Email', 'email'],
            
            # Spouse details
            'Spouse Surname': ['Spouse Surname', 'spouse_surname', 'S SURNAME'],
            'S Forename': ['S FORENAME', 's_forename', 'Spouse Forename', 'spouse_forename'],
            'S Dob': ['S DOB', 's_dob', 'Spouse DOB', 'spouse_dob'],
            'S Sex': ['S Sex', 's_sex', 'Spouse Sex', 'spouse_sex'],
            
            # Children - will be handled dynamically for multiple children
        }
    
    def _create_bupa_mappings(self) -> Dict[str, List[str]]:
        """Create mappings for BUPA medical template."""
        return {
            # BUPA-specific core fields
            'Ind': ['Change', 'Instruction', 'Action Type', 'Change Type', 'Employee reason for change'],
            'Date': ['Effective Date', 'date', 'change_date', 'Date', 'EFFECTIVE DATE'],
            'number': ['Group No', 'Group Number', 'group_number', 'scheme_number'],
            'name': ['Group Name', 'Company Name', 'group_name', 'Name'],
            'Description': ['Product', 'Product Description', 'Benefit', 'product', 'PRODUCT'],
            'Reference': ['Client Ref', 'Employee Number', 'Staff number', 'Payroll Number', 'Employee Number', 'payroll_number'],
            
            # Personal details mapped to BUPA fields
            'Surname': ['Surname', 'SURNAME', 'surname', 'last_name'],
            'First Name': ['Forename', 'FORENAME', 'forename', 'first_name', 'First name', 'ForeNames'],
            'Title': ['Title', 'TITLE', 'title'],
            'Date of Birth': ['DOB', 'dob', 'Date of Birth', 'date_of_birth', 'DateOfBirth'],
            'Sex': ['Sex', 'sex', 'Gender', 'gender', 'GENDER'],
            
            # Coverage information
            'of Cover': ['Type of Cover', 'Type Of Cover', 'Level Of Cover', 'level_of_cover', 'Option selected', 'Scale'],
            'Information': ['Location', 'LOCATION', 'location', 'geographical_location', 'National Insurance', 'ni_number'],
            
            # Family members (BUPA supports multiple relationships)
            'Relationship': ['Relationship', 'relationship', 'Type Of Cover'],
            'Surname1': ['Spouse Surname', 'spouse_surname', 'S SURNAME', 'Dependant Surname'],
            'First Name1': ['S FORENAME', 's_forename', 'Spouse Forename', 'spouse_forename', 'Dependant First Name'],
            'Title1': ['Spouse Title', 'spouse_title', 'S Title'],
            'Sex1': ['S Sex', 's_sex', 'Spouse Sex', 'spouse_sex', 'Spouse Gender'],
            'Date of Birth1': ['S DOB', 's_dob', 'Spouse DOB', 'spouse_dob', 'Spouse Date of Birth'],
        }
    
    def _normalize_column_name(self, col_name: str) -> str:
        """Normalize column names for matching."""
        return re.sub(r'[^\w\s]', '', str(col_name).strip().lower())
    
    def _find_column_mapping(self, input_columns: List[str]) -> Dict[str, str]:
        """
        Find the best mapping between input columns and target schema.
        
        Args:
            input_columns: List of column names from input file
            
        Returns:
            Dictionary mapping target columns to input columns
        """
        mapping = {}
        normalized_input = {self._normalize_column_name(col): col for col in input_columns}
        
        for target_col, possible_names in self.column_mappings.items():
            for possible_name in possible_names:
                normalized_possible = self._normalize_column_name(possible_name)
                if normalized_possible in normalized_input:
                    mapping[target_col] = normalized_input[normalized_possible]
                    break
        
        # Handle children columns dynamically
        mapping.update(self._map_children_columns(input_columns))
        
        return mapping
    
    def _map_children_columns(self, input_columns: List[str]) -> Dict[str, str]:
        """Map children columns dynamically."""
        child_mapping = {}
        
        # Pattern for child columns
        child_patterns = [
            (r'child\s*(\d+)\s*forename', 'Child {} Forename'),
            (r'child\s*(\d+)\s*surname', 'Child {} Surname'),
            (r'child\s*(\d+)\s*sex', 'Child {} Sex'),
            (r'child\s*(\d+)\s*dob', 'Child {} Dob'),
            (r'child\s*forename\s*(\d+)', 'Child {} Forename'),
            (r'child\s*surname\s*(\d+)', 'Child {} Surname'),
            (r'dependant\s*(\d+)\s*first\s*name', 'Child {} Forename'),
            (r'dependant\s*(\d+)\s*surname', 'Child {} Surname'),
        ]
        
        for input_col in input_columns:
            normalized = self._normalize_column_name(input_col)
            for pattern, target_template in child_patterns:
                match = re.search(pattern, normalized)
                if match:
                    child_num = int(match.group(1))
                    if child_num <= 5:  # We only support up to 5 children in template
                        target_col = target_template.format(child_num)
                        if target_col in self.target_columns:
                            child_mapping[target_col] = input_col
        
        return child_mapping
    
    def _standardize_data(self, df: pd.DataFrame, mapping: Dict[str, str]) -> pd.DataFrame:
        """
        Standardize and clean the data according to target schema requirements.
        
        Args:
            df: Input dataframe
            mapping: Column mapping dictionary
            
        Returns:
            Standardized dataframe
        """
        # Create output dataframe with target schema
        output_df = pd.DataFrame(columns=self.target_columns)
        
        # Map and copy data
        for target_col, input_col in mapping.items():
            if input_col in df.columns and target_col in output_df.columns:
                output_df[target_col] = df[input_col]
        
        # Data cleaning and standardization
        
        # Standardize dates
        date_columns = ['Dob', 'S Dob'] + [f'Child {i} Dob' for i in range(1, 6)]
        for col in date_columns:
            if col in output_df.columns:
                output_df[col] = pd.to_datetime(output_df[col], errors='coerce', dayfirst=True).dt.strftime('%d/%m/%Y')
        
        # Standardize gender/sex
        sex_columns = ['Sex', 'S Sex'] + [f'Child {i} Sex' for i in range(1, 6)]
        for col in sex_columns:
            if col in output_df.columns:
                output_df[col] = output_df[col].str.upper().map({'M': 'Male', 'F': 'Female', 'MALE': 'Male', 'FEMALE': 'Female'}).fillna(output_df[col])
        
        # Clean up names and text fields
        text_columns = ['Forename', 'Surname', 'Title', 'S Forename', 'Spouse Surname'] + \
                      [f'Child {i} Forename' for i in range(1, 6)] + [f'Child {i} Surname' for i in range(1, 6)]
        for col in text_columns:
            if col in output_df.columns:
                output_df[col] = output_df[col].astype(str).str.strip().str.title()
                output_df[col] = output_df[col].replace('Nan', '')
        
        # Clean postcode
        if 'Post Code' in output_df.columns:
            output_df['Post Code'] = output_df['Post Code'].astype(str).str.upper().str.strip()
        
        return output_df
    
    def read_input_file(self, file_path: str) -> Tuple[pd.DataFrame, str]:
        """
        Read input file regardless of format.
        
        Args:
            file_path: Path to input file
            
        Returns:
            Tuple of (dataframe, file_type)
        """
        file_ext = os.path.splitext(file_path)[1].lower()
        
        try:
            if file_ext == '.csv':
                df = pd.read_csv(file_path)
                return df, 'csv'
            elif file_ext == '.xls':
                df = pd.read_excel(file_path)
                return df, 'xls'
            elif file_ext == '.xlsx':
                # Try different header rows for xlsx files
                df = pd.read_excel(file_path)
                # If columns are unnamed, try header=1
                if any(str(col).startswith('Unnamed') for col in df.columns):
                    df = pd.read_excel(file_path, header=1)
                return df, 'xlsx'
            else:
                raise ValueError(f"Unsupported file format: {file_ext}")
        except Exception as e:
            logger.error(f"Error reading file {file_path}: {e}")
            raise
    
    def process_file(self, input_file_path: str, output_file_path: str = None) -> pd.DataFrame:
        """
        Process a single input file and map it to target schema.
        
        Args:
            input_file_path: Path to input file
            output_file_path: Optional path for output file
            
        Returns:
            Processed dataframe in target schema format
        """
        logger.info(f"Processing file: {input_file_path}")
        
        # Read input file
        df, file_type = self.read_input_file(input_file_path)
        logger.info(f"Read {len(df)} rows from {file_type} file")
        
        # Find column mappings
        mapping = self._find_column_mapping(df.columns.tolist())
        logger.info(f"Found {len(mapping)} column mappings")
        
        # Log mapping for review
        for target, source in mapping.items():
            logger.info(f"  {target} <- {source}")
        
        # Standardize data
        standardized_df = self._standardize_data(df, mapping)
        
        # Save output if path provided
        if output_file_path:
            self._save_output(standardized_df, output_file_path)
        
        return standardized_df
    
    def process_batch(self, input_folder: str, output_folder: str = "output/standardized") -> List[str]:
        """
        Process all files in a batch folder.
        
        Args:
            input_folder: Path to folder containing input files
            output_folder: Path to folder for output files
            
        Returns:
            List of processed file paths
        """
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        
        processed_files = []
        supported_extensions = ['.csv', '.xls', '.xlsx']
        
        for filename in os.listdir(input_folder):
            if any(filename.lower().endswith(ext) for ext in supported_extensions):
                input_path = os.path.join(input_folder, filename)
                output_filename = f"standardized_{os.path.splitext(filename)[0]}.xlsx"
                output_path = os.path.join(output_folder, output_filename)
                
                try:
                    self.process_file(input_path, output_path)
                    processed_files.append(output_path)
                    logger.info(f"Successfully processed: {filename}")
                except Exception as e:
                    logger.error(f"Failed to process {filename}: {e}")
        
        return processed_files
    
    def _save_output(self, df: pd.DataFrame, output_path: str):
        """Save processed dataframe to output file."""
        output_ext = os.path.splitext(output_path)[1].lower()
        
        if output_ext == '.csv':
            df.to_csv(output_path, index=False)
        elif output_ext in ['.xlsx', '.xls']:
            df.to_excel(output_path, index=False)
        else:
            # Default to Excel
            output_path = os.path.splitext(output_path)[0] + '.xlsx'
            df.to_excel(output_path, index=False)
        
        logger.info(f"Output saved to: {output_path}")
    
    def generate_mapping_report(self, input_folder: str) -> str:
        """
        Generate a report showing mapping analysis for all files.
        
        Args:
            input_folder: Path to input files folder
            
        Returns:
            Mapping report as string
        """
        report = []
        report.append("DATA INGESTION MAPPING REPORT")
        report.append("=" * 50)
        report.append(f"Target Schema: {len(self.target_columns)} columns")
        report.append(f"Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append("")
        
        for filename in os.listdir(input_folder):
            if any(filename.lower().endswith(ext) for ext in ['.csv', '.xls', '.xlsx']):
                try:
                    input_path = os.path.join(input_folder, filename)
                    df, file_type = self.read_input_file(input_path)
                    mapping = self._find_column_mapping(df.columns.tolist())
                    
                    report.append(f"File: {filename} ({file_type.upper()})")
                    report.append(f"  Rows: {len(df)}")
                    report.append(f"  Input Columns: {len(df.columns)}")
                    report.append(f"  Mapped Columns: {len(mapping)}")
                    report.append(f"  Coverage: {len(mapping)/len(self.target_columns)*100:.1f}%")
                    
                    # Show mappings
                    if mapping:
                        report.append("  Mappings:")
                        for target, source in sorted(mapping.items()):
                            report.append(f"    {target} <- {source}")
                    
                    # Show unmapped input columns
                    unmapped_input = [col for col in df.columns if col not in mapping.values()]
                    if unmapped_input:
                        report.append("  Unmapped Input Columns:")
                        for col in unmapped_input[:5]:  # Show first 5
                            report.append(f"    {col}")
                        if len(unmapped_input) > 5:
                            report.append(f"    ... and {len(unmapped_input) - 5} more")
                    
                    report.append("")
                    
                except Exception as e:
                    report.append(f"File: {filename} - ERROR: {e}")
                    report.append("")
        
        return "\n".join(report)


def main():
    """Main function for testing and demonstration."""
    # Initialize mapper
    mapper = DataIngestionMapper()
    
    # Generate mapping report
    print("Generating mapping analysis report...")
    report = mapper.generate_mapping_report("examples/Batchload files")
    print(report)
    
    # Process sample file
    print("\n" + "="*70)
    print("PROCESSING SAMPLE FILE")
    print("="*70)
    
    try:
        sample_file = "examples/Batchload files/Group 2.csv"
        if os.path.exists(sample_file):
            result_df = mapper.process_file(sample_file)
            print(f"\nProcessed {len(result_df)} rows")
            print(f"Output columns: {len(result_df.columns)}")
            
            # Show sample of processed data
            print("\nSample processed data:")
            non_empty_cols = [col for col in result_df.columns if result_df[col].notna().any()][:8]
            if non_empty_cols and len(result_df) > 0:
                for col in non_empty_cols:
                    val = result_df[col].iloc[0]
                    if pd.notna(val):
                        print(f"  {col}: {val}")
    except Exception as e:
        print(f"Error processing sample file: {e}")


if __name__ == "__main__":
    main()