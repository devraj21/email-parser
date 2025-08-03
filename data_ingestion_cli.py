#!/usr/bin/env python3
"""
Data Ingestion CLI - Command line interface for processing batch files.

Usage:
    python data_ingestion_cli.py --help
    python data_ingestion_cli.py report --input "examples/Batchload files"
    python data_ingestion_cli.py process --input "examples/Batchload files" --output "output/standardized"
    python data_ingestion_cli.py single --file "examples/Batchload files/Group 2.csv" --output "output/group2_processed.xlsx"
"""

import argparse
import os
import sys
from typing import Optional
from data_ingestion_mapper import DataIngestionMapper

def generate_report(input_folder: str, template_type: str = "standard") -> None:
    """Generate and display mapping analysis report."""
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)
    
    mapper = DataIngestionMapper(template_type=template_type)
    report = mapper.generate_mapping_report(input_folder)
    print(report)

def process_batch(input_folder: str, output_folder: str, template_type: str = "standard") -> None:
    """Process all files in batch folder."""
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)
    
    print(f"Processing batch files from: {input_folder}")
    print(f"Template type: {template_type}")
    print(f"Output folder: {output_folder}")
    print("-" * 60)
    
    mapper = DataIngestionMapper(template_type=template_type)
    processed_files = mapper.process_batch(input_folder, output_folder)
    
    print(f"\nBatch processing completed!")
    print(f"Processed {len(processed_files)} files:")
    for file_path in processed_files:
        print(f"  ✓ {os.path.basename(file_path)}")
    
    if processed_files:
        print(f"\nAll processed files saved to: {output_folder}")
    else:
        print("\nNo files were successfully processed.")

def process_single_file(input_file: str, output_file: Optional[str] = None, template_type: str = "standard") -> None:
    """Process a single input file."""
    if not os.path.exists(input_file):
        print(f"Error: Input file '{input_file}' does not exist.")
        sys.exit(1)
    
    if output_file is None:
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(input_file))[0]
        template_suffix = f"_{template_type}" if template_type != "standard" else ""
        output_file = f"output/standardized_{base_name}{template_suffix}.xlsx"
    
    # Create output directory if it doesn't exist
    output_dir = os.path.dirname(output_file)
    if output_dir and not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    print(f"Processing file: {input_file}")
    print(f"Template type: {template_type}")
    print(f"Output file: {output_file}")
    print("-" * 60)
    
    try:
        mapper = DataIngestionMapper(template_type=template_type)
        result_df = mapper.process_file(input_file, output_file)
        
        print(f"\n✓ Successfully processed {len(result_df)} rows")
        print(f"✓ Output saved to: {output_file}")
        
        # Show sample of processed data
        print(f"\nSample processed data:")
        non_empty_cols = [col for col in result_df.columns if result_df[col].notna().any()][:8]
        if non_empty_cols and len(result_df) > 0:
            for col in non_empty_cols:
                val = result_df[col].iloc[0]
                if val is not None and str(val) != 'nan':
                    print(f"  {col}: {val}")
        
    except Exception as e:
        print(f"Error processing file: {e}")
        sys.exit(1)

def validate_files(input_folder: str, template_type: str = "standard") -> None:
    """Validate all files in the input folder and show quality metrics."""
    if not os.path.exists(input_folder):
        print(f"Error: Input folder '{input_folder}' does not exist.")
        sys.exit(1)
    
    print(f"Validating files in: {input_folder}")
    print(f"Template type: {template_type}")
    print("=" * 60)
    
    mapper = DataIngestionMapper(template_type=template_type)
    supported_extensions = ['.csv', '.xls', '.xlsx']
    
    total_files = 0
    valid_files = 0
    total_rows = 0
    total_mapped_columns = 0
    total_possible_columns = len(mapper.target_columns)
    
    for filename in os.listdir(input_folder):
        if any(filename.lower().endswith(ext) for ext in supported_extensions):
            total_files += 1
            filepath = os.path.join(input_folder, filename)
            
            try:
                df, file_type = mapper.read_input_file(filepath)
                mapping = mapper._find_column_mapping(df.columns.tolist())
                
                print(f"\n📁 {filename} ({file_type.upper()})")
                print(f"   Rows: {len(df)}")
                print(f"   Input Columns: {len(df.columns)}")
                print(f"   Mapped Columns: {len(mapping)}")
                print(f"   Coverage: {len(mapping)/total_possible_columns*100:.1f}%")
                
                # Data quality checks
                quality_issues = []
                
                # Check for empty rows
                empty_rows = df.isnull().all(axis=1).sum()
                if empty_rows > 0:
                    quality_issues.append(f"{empty_rows} empty rows")
                
                # Check for duplicate rows
                duplicate_rows = df.duplicated().sum()
                if duplicate_rows > 0:
                    quality_issues.append(f"{duplicate_rows} duplicate rows")
                
                # Check key field completion rates
                key_fields = ['Client Ref.', 'Surname', 'Forename']
                for key_field in key_fields:
                    if key_field in mapping:
                        input_col = mapping[key_field]
                        if input_col in df.columns:
                            missing_count = df[input_col].isnull().sum()
                            if missing_count > 0:
                                quality_issues.append(f"{missing_count} missing {key_field}")
                
                if quality_issues:
                    print(f"   ⚠️  Quality Issues: {', '.join(quality_issues)}")
                else:
                    print(f"   ✅ No quality issues detected")
                
                valid_files += 1
                total_rows += len(df)
                total_mapped_columns += len(mapping)
                
            except Exception as e:
                print(f"\n❌ {filename}: ERROR - {e}")
    
    # Summary
    print(f"\n" + "=" * 60)
    print(f"VALIDATION SUMMARY")
    print(f"=" * 60)
    print(f"Total Files: {total_files}")
    print(f"Valid Files: {valid_files}")
    print(f"Failed Files: {total_files - valid_files}")
    print(f"Total Rows: {total_rows}")
    if valid_files > 0:
        print(f"Average Mapping Coverage: {(total_mapped_columns/(valid_files * total_possible_columns))*100:.1f}%")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Data Ingestion Tool - Map varied input files to standard target schema",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate mapping analysis report
  python data_ingestion_cli.py report --input "examples/Batchload files"
  
  # Process all files in batch
  python data_ingestion_cli.py process --input "examples/Batchload files" --output "output/standardized"
  
  # Process single file
  python data_ingestion_cli.py single --file "examples/Batchload files/Group 2.csv"
  
  # Validate files for quality issues
  python data_ingestion_cli.py validate --input "examples/Batchload files"
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate mapping analysis report')
    report_parser.add_argument('--input', '-i', required=True, help='Input folder containing batch files')
    report_parser.add_argument('--template', '-t', choices=['standard', 'bupa'], default='standard', 
                             help='Template type: standard or bupa (default: standard)')
    
    # Process command
    process_parser = subparsers.add_parser('process', help='Process all files in batch')
    process_parser.add_argument('--input', '-i', required=True, help='Input folder containing batch files')
    process_parser.add_argument('--output', '-o', default='output/standardized', help='Output folder for processed files')
    process_parser.add_argument('--template', '-t', choices=['standard', 'bupa'], default='standard',
                              help='Template type: standard or bupa (default: standard)')
    
    # Single file command
    single_parser = subparsers.add_parser('single', help='Process a single file')
    single_parser.add_argument('--file', '-f', required=True, help='Input file to process')
    single_parser.add_argument('--output', '-o', help='Output file path (optional)')
    single_parser.add_argument('--template', '-t', choices=['standard', 'bupa'], default='standard',
                             help='Template type: standard or bupa (default: standard)')
    
    # Validate command
    validate_parser = subparsers.add_parser('validate', help='Validate files for quality issues')
    validate_parser.add_argument('--input', '-i', required=True, help='Input folder containing batch files')
    validate_parser.add_argument('--template', '-t', choices=['standard', 'bupa'], default='standard',
                               help='Template type: standard or bupa (default: standard)')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Execute commands
    try:
        if args.command == 'report':
            generate_report(args.input, args.template)
        elif args.command == 'process':
            process_batch(args.input, args.output, args.template)
        elif args.command == 'single':
            process_single_file(args.file, args.output, args.template)
        elif args.command == 'validate':
            validate_files(args.input, args.template)
    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()