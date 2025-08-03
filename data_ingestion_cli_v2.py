#!/usr/bin/env python3
"""
Configuration-Driven Data Ingestion CLI

Enhanced CLI that uses JSON configuration files to automatically process
files with the appropriate templates and mappings.
"""

import argparse
import os
import sys
from typing import Optional
from data_ingestion_mapper_v2 import ConfigurableDataIngestionMapper
from config_manager import create_default_configs

def auto_process_all(config_dir: str = "config", base_output_dir: str = "output") -> None:
    """Automatically process all files based on configuration mappings."""
    print("🚀 Starting automatic processing based on configuration...")
    print(f"Configuration directory: {config_dir}")
    print(f"Base output directory: {base_output_dir}")
    print("-" * 60)
    
    try:
        mapper = ConfigurableDataIngestionMapper(config_dir)
        results = mapper.process_batch_auto(base_output_dir=base_output_dir)
        
        print(f"\n✅ Automatic processing completed!")
        
        total_files = 0
        for template_name, files in results.items():
            print(f"\n📋 Template: {template_name}")
            print(f"   Processed {len(files)} files:")
            for file_path in files:
                print(f"     ✓ {os.path.basename(file_path)}")
            total_files += len(files)
        
        if total_files > 0:
            print(f"\n🎉 Total files processed: {total_files}")
        else:
            print("\n⚠️  No files were processed. Check your configuration and file patterns.")
            
    except Exception as e:
        print(f"❌ Error during automatic processing: {e}")
        sys.exit(1)

def generate_report(config_dir: str = "config", input_folder: str = None) -> None:
    """Generate comprehensive mapping analysis report."""
    try:
        mapper = ConfigurableDataIngestionMapper(config_dir)
        report = mapper.generate_mapping_report(input_folder)
        print(report)
    except Exception as e:
        print(f"❌ Error generating report: {e}")
        sys.exit(1)

def process_single_file(file_path: str, config_dir: str = "config", 
                       template_name: str = None, output_file: str = None) -> None:
    """Process a single file with configuration-driven mapping."""
    if not os.path.exists(file_path):
        print(f"❌ Error: Input file '{file_path}' does not exist.")
        sys.exit(1)
    
    print(f"📁 Processing file: {file_path}")
    print(f"⚙️  Configuration directory: {config_dir}")
    if template_name:
        print(f"🎯 Forced template: {template_name}")
    print("-" * 60)
    
    try:
        mapper = ConfigurableDataIngestionMapper(config_dir, template_name)
        result_df = mapper.process_file(file_path, output_file)
        
        print(f"\n✅ Successfully processed {len(result_df)} rows")
        if output_file:
            print(f"📄 Output saved to: {output_file}")
        
        # Show sample of processed data
        print(f"\n📊 Sample processed data:")
        non_empty_cols = [col for col in result_df.columns if result_df[col].notna().any()][:8]
        if non_empty_cols and len(result_df) > 0:
            for col in non_empty_cols:
                val = result_df[col].iloc[0]
                if val is not None and str(val) != 'nan':
                    print(f"   {col}: {val}")
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        sys.exit(1)

def validate_config(config_dir: str = "config") -> None:
    """Validate configuration files."""
    print(f"🔍 Validating configuration in: {config_dir}")
    print("-" * 60)
    
    try:
        from config_manager import ConfigurationManager
        config_manager = ConfigurationManager(config_dir)
        
        errors = config_manager.validate_configuration()
        if errors:
            print("❌ Configuration validation failed:")
            for error in errors:
                print(f"   • {error}")
            sys.exit(1)
        else:
            print("✅ Configuration validation passed!")
            
            # Show available templates
            templates = config_manager.get_available_templates()
            print(f"\n📋 Available templates ({len(templates)}):")
            for template in templates:
                config = config_manager.get_template_config(template)
                print(f"   • {template}: {config.get('name', 'No description')}")
            
            # Show file mappings
            mappings = config_manager.file_mappings_config.get("file_mappings", [])
            enabled_mappings = [m for m in mappings if m.get("enabled", True)]
            print(f"\n🗂️  Active file mappings ({len(enabled_mappings)}):")
            for mapping in enabled_mappings:
                print(f"   • {mapping['name']}: {mapping['template']} template")
                print(f"     Input patterns: {', '.join(mapping['input_patterns'][:3])}")
                if len(mapping['input_patterns']) > 3:
                    print(f"     ... and {len(mapping['input_patterns']) - 3} more")
                print(f"     Output: {mapping.get('output_folder', 'default')}")
                
    except Exception as e:
        print(f"❌ Error validating configuration: {e}")
        sys.exit(1)

def list_templates(config_dir: str = "config") -> None:
    """List available templates with their configurations."""
    try:
        from config_manager import ConfigurationManager
        config_manager = ConfigurationManager(config_dir)
        
        templates = config_manager.get_available_templates()
        
        print("📋 AVAILABLE TEMPLATES")
        print("=" * 50)
        
        for template_name in templates:
            config = config_manager.get_template_config(template_name)
            print(f"\n🎯 {template_name.upper()}")
            print(f"   Name: {config.get('name', 'N/A')}")
            print(f"   Description: {config.get('description', 'N/A')}")
            print(f"   Template File: {config.get('template_file', 'N/A')}")
            if config.get('sheet_name'):
                print(f"   Sheet: {config['sheet_name']}")
            
            # Show column mapping counts
            mappings = config_manager.get_column_mappings(template_name)
            flat_mappings = config_manager.flatten_column_mappings(template_name)
            print(f"   Column Mappings: {len(flat_mappings)} defined")
            
    except Exception as e:
        print(f"❌ Error listing templates: {e}")
        sys.exit(1)

def create_configs(config_dir: str = "config") -> None:
    """Create default configuration files."""
    print(f"🛠️  Creating default configuration files in: {config_dir}")
    
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
        print(f"   📁 Created directory: {config_dir}")
    
    create_default_configs()
    print("✅ Configuration files created successfully!")
    print("\n📝 Next steps:")
    print("   1. Edit config/templates_config.json to add/modify templates")
    print("   2. Edit config/file_mappings.json to define which files use which templates")
    print("   3. Run 'validate-config' to check your configuration")
    print("   4. Run 'auto-process' to process files automatically")

def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Configuration-Driven Data Ingestion Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
🎯 Configuration-Based Processing:
   This tool uses JSON configuration files to define templates and file mappings.
   
📁 Configuration Files:
   • config/templates_config.json - Define templates and column mappings
   • config/file_mappings.json - Define which files use which templates
   
🚀 Examples:
   # Create default configuration files
   python data_ingestion_cli_v2.py create-config
   
   # Validate configuration
   python data_ingestion_cli_v2.py validate-config
   
   # Automatically process all files based on configuration
   python data_ingestion_cli_v2.py auto-process
   
   # Generate mapping report
   python data_ingestion_cli_v2.py report --input "examples/Batchload files"
   
   # Process single file (auto-detect template)
   python data_ingestion_cli_v2.py single --file "examples/Change files/AON.xls"
   
   # Process single file with specific template
   python data_ingestion_cli_v2.py single --file "data.csv" --template template_2
        """
    )
    
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Auto-process command
    auto_parser = subparsers.add_parser('auto-process', help='Automatically process all files based on configuration')
    auto_parser.add_argument('--config-dir', '-c', default='config', help='Configuration directory (default: config)')
    auto_parser.add_argument('--output', '-o', default='output', help='Base output directory (default: output)')
    
    # Report command
    report_parser = subparsers.add_parser('report', help='Generate mapping analysis report')
    report_parser.add_argument('--config-dir', '-c', default='config', help='Configuration directory (default: config)')
    report_parser.add_argument('--input', '-i', help='Input folder to analyze (optional)')
    
    # Single file command
    single_parser = subparsers.add_parser('single', help='Process a single file')
    single_parser.add_argument('--file', '-f', required=True, help='Input file to process')
    single_parser.add_argument('--config-dir', '-c', default='config', help='Configuration directory (default: config)')
    single_parser.add_argument('--template', '-t', help='Force specific template (overrides auto-detection)')
    single_parser.add_argument('--output', '-o', help='Output file path (optional)')
    
    # Validate config command
    validate_parser = subparsers.add_parser('validate-config', help='Validate configuration files')
    validate_parser.add_argument('--config-dir', '-c', default='config', help='Configuration directory (default: config)')
    
    # List templates command
    list_parser = subparsers.add_parser('list-templates', help='List available templates')
    list_parser.add_argument('--config-dir', '-c', default='config', help='Configuration directory (default: config)')
    
    # Create config command
    create_parser = subparsers.add_parser('create-config', help='Create default configuration files')
    create_parser.add_argument('--config-dir', '-c', default='config', help='Configuration directory (default: config)')
    
    # Parse arguments
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(0)
    
    # Execute commands
    try:
        if args.command == 'auto-process':
            auto_process_all(args.config_dir, args.output)
        elif args.command == 'report':
            generate_report(args.config_dir, args.input)
        elif args.command == 'single':
            process_single_file(args.file, args.config_dir, args.template, args.output)
        elif args.command == 'validate-config':
            validate_config(args.config_dir)
        elif args.command == 'list-templates':
            list_templates(args.config_dir)
        elif args.command == 'create-config':
            create_configs(args.config_dir)
            
    except KeyboardInterrupt:
        print("\n\n🛑 Operation cancelled by user.")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()