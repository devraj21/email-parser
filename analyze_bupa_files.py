#!/usr/bin/env python3
"""
Analyze BUPA Medical Template and Change Files structure.
"""

import pandas as pd
import os

def analyze_bupa_template_and_files():
    print('ANALYZING BUPA MEDICAL TEMPLATE AND CHANGE FILES')
    print('='*70)

    # Analyze BUPA Medical Template
    try:
        bupa_template_path = 'template/Change files/UK Membership Template - BUPA update June 2025_MEDICAL.xlsx'
        
        # Check all sheets
        xl_file = pd.ExcelFile(bupa_template_path)
        print(f'\nBUPA Template Sheets: {xl_file.sheet_names}')
        
        # Read the 'For Use' sheet which contains the actual template
        df_bupa = pd.read_excel(bupa_template_path, sheet_name='For Use')
        print(f'\nBUPA Medical Template - For Use Sheet ({len(df_bupa.columns)} columns):')
        print('-'*60)
        
        # Get proper column names from first row if available
        if len(df_bupa) > 0:
            bupa_columns = []
            for i, col in enumerate(df_bupa.columns):
                # Check if first row has a better column name
                potential_header = df_bupa.iloc[0, i] if pd.notna(df_bupa.iloc[0, i]) else None
                if potential_header and str(potential_header) != 'nan' and not str(col).startswith('Unnamed'):
                    bupa_columns.append(str(potential_header))
                elif not str(col).startswith('Unnamed'):
                    bupa_columns.append(str(col))
                else:
                    bupa_columns.append(f'Column_{i+1}')
            
            print('Template columns:')
            for i, col in enumerate(bupa_columns[:30]):  # Show first 30
                print(f'  {i+1:2d}. {col}')
            if len(bupa_columns) > 30:
                print(f'  ... and {len(bupa_columns) - 30} more columns')
            
            # Show sample data from row 2 onwards (row 1 might be headers)
            print(f'\nSample data (from row 2):')
            if len(df_bupa) > 1:
                for i, col in enumerate(df_bupa.columns[:10]):
                    val = df_bupa[col].iloc[1] if pd.notna(df_bupa[col].iloc[1]) else None
                    if val is not None and str(val) != 'nan':
                        col_name = bupa_columns[i] if i < len(bupa_columns) else f'Col_{i}'
                        print(f'  {col_name}: {val}')
        
    except Exception as e:
        print(f'Error reading BUPA template: {e}')

    print('\n' + '='*70)

    # Analyze Change Files
    change_files_dir = 'examples/Change files'
    print(f'\nCHANGE FILES ANALYSIS:')
    print('-'*50)

    change_files = []
    for filename in os.listdir(change_files_dir):
        if filename.endswith(('.csv', '.xls', '.xlsx')) and not filename.startswith('UK Membership'):
            change_files.append(filename)
    
    for filename in sorted(change_files):
        filepath = os.path.join(change_files_dir, filename)
        try:
            if filename.endswith('.csv'):
                df = pd.read_csv(filepath)
                file_type = 'CSV'
            else:
                df = pd.read_excel(filepath)
                file_type = 'Excel'
            
            print(f'\n📁 {filename} ({file_type}):')
            print(f'   Shape: {df.shape}')
            print(f'   Columns ({len(df.columns)}):')
            for i, col in enumerate(df.columns[:12]):
                print(f'     {i+1:2d}. {col}')
            if len(df.columns) > 12:
                print(f'     ... and {len(df.columns) - 12} more columns')
            
            # Show sample data for first few key columns
            if len(df) > 0:
                print(f'   Sample data (first row):')
                sample_count = 0
                for col in df.columns[:10]:
                    if sample_count >= 6:  # Limit to 6 sample fields
                        break
                    val = df[col].iloc[0] if pd.notna(df[col].iloc[0]) else None
                    if val is not None and str(val) != 'nan':
                        display_val = str(val)[:35] + ('...' if len(str(val)) > 35 else '')
                        print(f'     {col}: {display_val}')
                        sample_count += 1
                        
        except Exception as e:
            print(f'\n❌ {filename}: Error - {e}')

    # Summary comparison
    print('\n' + '='*70)
    print('TEMPLATE COMPARISON SUMMARY:')
    print('='*70)
    
    try:
        # Original template
        orig_template = pd.read_excel('template/Data Template.xlsx')
        print(f'Original Template: {len(orig_template.columns)} columns')
        
        # BUPA template
        bupa_template = pd.read_excel('template/Change files/UK Membership Template - BUPA update June 2025_MEDICAL.xlsx')
        print(f'BUPA Medical Template: {len(bupa_template.columns)} columns')
        
        # Find common and different columns
        orig_cols = set(orig_template.columns)
        bupa_cols = set(bupa_template.columns)
        
        common_cols = orig_cols.intersection(bupa_cols)
        orig_only = orig_cols - bupa_cols
        bupa_only = bupa_cols - orig_cols
        
        print(f'Common columns: {len(common_cols)}')
        print(f'Original template only: {len(orig_only)}')
        print(f'BUPA template only: {len(bupa_only)}')
        
        if bupa_only:
            print(f'\nBUPA-specific columns:')
            for col in sorted(bupa_only):
                print(f'  - {col}')
                
    except Exception as e:
        print(f'Error in template comparison: {e}')

if __name__ == "__main__":
    analyze_bupa_template_and_files()