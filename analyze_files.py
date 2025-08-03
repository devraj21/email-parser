#!/usr/bin/env python3
"""
Analyze batch load files and template structure for data ingestion mapping.
"""

import pandas as pd
import os

def analyze_files():
    batchload_dir = 'examples/Batchload files'
    
    print("="*80)
    print("DATA INGESTION FILE ANALYSIS")
    print("="*80)
    
    # Check Group 1.xls
    try:
        filepath = os.path.join(batchload_dir, 'Group 1.xls')
        df = pd.read_excel(filepath)
        print('\nGroup 1.xls:')
        print('-'*50)
        print(f'Shape: {df.shape}')
        print(f'Columns ({len(df.columns)}):')
        for i, col in enumerate(df.columns[:15]):
            print(f'  {i+1:2d}. {col}')
        if len(df.columns) > 15:
            print(f'  ... and {len(df.columns) - 15} more columns')
        
        # Show sample data
        if len(df) > 0:
            print(f'\nSample data (first row with values):')
            for col in df.columns[:12]:
                val = df[col].iloc[0] if pd.notna(df[col].iloc[0]) else None
                if val is not None and str(val) != 'nan':
                    print(f'  {col}: {val}')
    except Exception as e:
        print(f'Error reading Group 1.xls: {e}')

    # Check Group 8.xlsx structure
    try:
        filepath = os.path.join(batchload_dir, 'Group 8.xlsx')
        df = pd.read_excel(filepath)
        print('\n\nGroup 8.xlsx:')
        print('-'*50)
        print(f'Shape: {df.shape}')
        print('Raw structure (first 4 rows, first 8 columns):')
        for i in range(min(4, len(df))):
            row_data = []
            for j, col in enumerate(df.columns[:8]):
                val = df[col].iloc[i]
                if pd.notna(val) and str(val).strip():
                    row_data.append(f'Col{j}: {str(val)[:20]}')
            if row_data:
                print(f'  Row {i}: {" | ".join(row_data)}')
                
        # Try to find actual headers
        print('\nLooking for header row...')
        for header_row in [1, 2, 3]:
            try:
                df_test = pd.read_excel(filepath, header=header_row)
                valid_cols = [col for col in df_test.columns if not str(col).startswith('Unnamed')]
                if len(valid_cols) > 5:  # If we find more than 5 named columns
                    print(f'Found headers at row {header_row}:')
                    for i, col in enumerate(valid_cols[:10]):
                        print(f'  {i+1:2d}. {col}')
                    break
            except:
                continue
                
    except Exception as e:
        print(f'Error reading Group 8.xlsx: {e}')

    # Summary of all files
    print('\n\n' + '='*80)
    print('FILE FORMAT SUMMARY')
    print('='*80)
    
    file_extensions = {'.csv': [], '.xls': [], '.xlsx': []}
    
    for filename in os.listdir(batchload_dir):
        if filename.endswith('.csv'):
            file_extensions['.csv'].append(filename)
        elif filename.endswith('.xls'):
            file_extensions['.xls'].append(filename)
        elif filename.endswith('.xlsx'):
            file_extensions['.xlsx'].append(filename)
    
    for ext, files in file_extensions.items():
        if files:
            print(f'\n{ext} files ({len(files)}): {", ".join(files)}')

if __name__ == "__main__":
    analyze_files()