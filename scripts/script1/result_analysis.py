import pandas as pd
import numpy as np
import re
from pathlib import Path

def extract_language(task_name):
    """Extract language code from task name"""
    # Pattern to match language codes like amh, eng, fra, etc.
    match = re.search(r'_(amh|eng|ewe|fra|hau|ibo|kin|lin|lug|orm|sna|sot|swa|twi|vai|wol|xho|yor|zul)_', task_name)
    if match:
        return match.group(1)
    return None

def load_and_process_data():
    """Load all result files and process them"""
    results_dir = Path('data/results/result_cleaned')
    all_data = []
    
    # Process each model directory
    for model_dir in results_dir.iterdir():
        if model_dir.is_dir():
            model_name = model_dir.name
            
            # Process each CSV file in the model directory
            for csv_file in model_dir.glob('*.csv'):
                task_name = csv_file.stem  # filename without extension
                
                try:
                    df = pd.read_csv(csv_file)
                    
                    # Add model and task information
                    df['Model'] = model_name
                    df['Task'] = task_name
                    
                    # Extract language from task names
                    df['Language'] = df['Tasks'].apply(extract_language)
                    
                    all_data.append(df)
                    
                except Exception as e:
                    print(f"Error processing {csv_file}: {e}")
    
    return pd.concat(all_data, ignore_index=True)

def calculate_averages(df):
    """Calculate averages for total and by language"""
    
    # Convert Stderr to numeric, handling empty strings
    df['Stderr'] = pd.to_numeric(df['Stderr'], errors='coerce')
    
    # Overall averages
    total_avg = {
        'Total_Value_Avg': df['Value'].mean(),
        'Total_Stderr_Avg': df['Stderr'].mean(),
        'Total_Count': len(df)
    }
    
    # Averages by language
    language_stats = df.groupby('Language').agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    
    # Flatten column names
    language_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    language_stats = language_stats.reset_index()
    
    # Averages by model
    model_stats = df.groupby('Model').agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    
    # Flatten column names
    model_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    model_stats = model_stats.reset_index()
    
    # Averages by task
    task_stats = df.groupby('Task').agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    
    # Flatten column names
    task_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    task_stats = task_stats.reset_index()
    
    return total_avg, language_stats, model_stats, task_stats

def main():
    print("Loading and processing data...")
    df = load_and_process_data()
    
    print(f"Total records loaded: {len(df)}")
    print(f"Languages found: {sorted(df['Language'].unique())}")
    print(f"Models found: {sorted(df['Model'].unique())}")
    print(f"Tasks found: {sorted(df['Task'].unique())}")
    print("\n" + "="*50)
    
    # Calculate averages
    total_avg, language_stats, model_stats, task_stats = calculate_averages(df)
    
    # Display results
    print("OVERALL AVERAGES:")
    print(f"Total Value Average: {total_avg['Total_Value_Avg']:.4f}")
    print(f"Total Stderr Average: {total_avg['Total_Stderr_Avg']:.4f}")
    print(f"Total Count: {total_avg['Total_Count']}")
    print("\n" + "="*50)
    
    print("AVERAGES BY LANGUAGE:")
    print(language_stats.to_string(index=False))
    print("\n" + "="*50)
    
    print("AVERAGES BY MODEL:")
    print(model_stats.to_string(index=False))
    print("\n" + "="*50)
    
    print("AVERAGES BY TASK:")
    print(task_stats.to_string(index=False))
    
    # Save results to CSV files
    language_stats.to_csv('language_averages.csv', index=False)
    model_stats.to_csv('model_averages.csv', index=False)
    task_stats.to_csv('task_averages.csv', index=False)
    
    print("\n" + "="*50)
    print("Results saved to:")
    print("- language_averages.csv")
    print("- model_averages.csv") 
    print("- task_averages.csv")

if __name__ == "__main__":
    main() 