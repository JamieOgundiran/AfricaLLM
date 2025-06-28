import csv
import re
import os
from pathlib import Path
import pandas as pd

def clean_raw_result_file(input_file_path, output_file_path):
    """
    Clean a raw result file and save it as a cleaned CSV using the notebook logic
    
    Args:
        input_file_path: Path to the raw .txt file
        output_file_path: Path to save the cleaned .csv file
    """
    print(f"Processing: {input_file_path}")
    
    # Read the raw file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Clean the data and extract rows
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    # Remove header and separator
    lines = [line for line in lines if not set(line.strip()) <= {'|', '-'}]
    
    # Get the header from the first row
    header_line = lines[0]
    all_headers = [h.strip() for h in header_line.strip('|').split('|')]
    # Filter out empty headers (columns with no names like arrows and symbols)
    headers = [h for h in all_headers if h]
    # Remove the header row from lines
    lines = lines[1:]
    
    # Prepare rows
    rows = []
    last_task = ""
    for line in lines:
        all_items = [item.strip() for item in line.strip('|').split('|')]
        # Filter out items corresponding to empty headers
        items = [all_items[i] for i in range(len(all_items)) if i < len(all_headers) and all_headers[i].strip()]
        
        # If the task column is empty, fill it with the last task name
        if items[0] == '':
            items[0] = last_task
        else:
            last_task = items[0]
        rows.append(items)
    
    # Create output directory if it doesn't exist
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to CSV with all columns (Tasks, Version, Filter, n-shot, Metric, Value, Stderr)
    with open(output_file_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        writer.writerows(rows)
    
    print(f"Saved: {output_file_path} ({len(rows)} rows)")

def further_clean_csv_file(csv_path):
    """
    Further clean the CSV file as per notebook logic:
    - Remove rows where Filter == 'remove_whitespace'
    - Drop columns: Filter, n-shot, Version
    - Remove the first row (index 0)
    """
    df = pd.read_csv(csv_path)
    if 'Filter' in df.columns:
        df = df[df['Filter'] != 'remove_whitespace']
    for col in ['Filter', 'n-shot', 'Version']:
        if col in df.columns:
            df.drop(columns=[col], inplace=True)
    # Remove the first row (index 0)
    df = df.iloc[1:]
    df.to_csv(csv_path, index=False)
    print(f"Further cleaned: {csv_path}")

def process_all_raw_results():
    """
    Process all raw result files and save them in the cleaned format
    """
    raw_dir = Path('data/results/result_raw')
    cleaned_dir = Path('data/results/result_cleaned')
    
    if not raw_dir.exists():
        print(f"Raw results directory not found: {raw_dir}")
        return
    
    # Process each model directory
    for model_dir in raw_dir.iterdir():
        if model_dir.is_dir():
            model_name = model_dir.name
            print(f"\nProcessing model: {model_name}")
            
            # Create corresponding cleaned directory
            cleaned_model_dir = cleaned_dir / model_name
            cleaned_model_dir.mkdir(parents=True, exist_ok=True)
            
            # Process each .txt file in the model directory
            for txt_file in model_dir.glob('*.txt'):
                task_name = txt_file.stem  # e.g., 'afrimgsm' from 'afrimgsm.txt'
                output_file = cleaned_model_dir / f"{task_name}_{model_name.lower()}.csv"
                
                try:
                    clean_raw_result_file(txt_file, output_file)
                except Exception as e:
                    print(f"Error processing {txt_file}: {e}")
                # Further clean the output CSV
                try:
                    further_clean_csv_file(output_file)
                except Exception as e:
                    print(f"Error further cleaning {output_file}: {e}")

def main():
    print("Starting to clean raw result files...")
    process_all_raw_results()
    print("\nCleaning completed!")

if __name__ == "__main__":
    main() 