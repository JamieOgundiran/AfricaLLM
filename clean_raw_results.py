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

def clean_afriqa_raw_result_file(input_file_path, output_file_path):
    """
    Clean an AfriQA raw result file and save it as a CSV with F1 scores only
    
    Args:
        input_file_path: Path to the raw .txt file
        output_file_path: Path to save the cleaned .csv file
    """
    print(f"Processing AfriQA: {input_file_path}")
    
    # Read the raw file
    with open(input_file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse the data
    lines = [line.strip() for line in content.split('\n') if line.strip()]
    
    # Skip header and separator lines
    data_lines = []
    for line in lines:
        if not line.startswith('|') or set(line.strip()) <= {'|', '-'}:
            continue
        data_lines.append(line)
    
    # Extract F1 scores
    results = []
    current_task = ""
    
    for line in data_lines:
        items = [item.strip() for item in line.strip('|').split('|')]
        
        # Skip empty lines
        if len(items) < 7:
            continue
            
        task = items[0]
        metric = items[4] if len(items) > 4 else ""
        value = items[6] if len(items) > 6 else ""
        
        # Update current task if not empty
        if task:
            current_task = task
        
        # Only process F1 score lines
        if metric == "f1" and value and value != "N/A":
            # Extract language and prompt number from task name
            # Format: afriqa_{lang}_prompt_{num}
            if current_task.startswith("afriqa_"):
                parts = current_task.split("_")
                if len(parts) >= 4:
                    language = parts[1]  # e.g., "swa" from "afriqa_swa_prompt_1"
                    prompt_num = parts[3]  # e.g., "1" from "afriqa_swa_prompt_1"
                    
                    try:
                        f1_score = float(value)
                        results.append({
                            'Language': language,
                            'Prompt': f'prompt_{prompt_num}',
                            'F1_Score': f1_score
                        })
                    except ValueError:
                        print(f"Could not convert value '{value}' to float for task {current_task}")
    
    # Create output directory if it doesn't exist
    output_file_path.parent.mkdir(parents=True, exist_ok=True)
    
    # Write to CSV
    if results:
        df = pd.DataFrame(results)
        df.to_csv(output_file_path, index=False)
        print(f"Saved: {output_file_path} ({len(results)} rows)")
    else:
        print(f"No F1 scores found in {input_file_path}")

def process_all_raw_results():
    """
    Process all raw result files and save them in the cleaned format
    """
    raw_dir = Path('results/result_raw')
    cleaned_dir = Path('results/result_cleaned')
    
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
                
                # Special handling for AfriQA files
                if task_name == 'afriqa':
                    try:
                        clean_afriqa_raw_result_file(txt_file, output_file)
                        print(f"AfriQA file processed successfully: {output_file}")
                    except Exception as e:
                        print(f"Error processing AfriQA {txt_file}: {e}")
                else:
                    try:
                        clean_raw_result_file(txt_file, output_file)
                    except Exception as e:
                        print(f"Error processing {txt_file}: {e}")
                    # Further clean the output CSV (only for non-AfriQA files)
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