import pandas as pd
import numpy as np
import re
from pathlib import Path

def extract_language(task_name):
    """Extract language code from task name"""
    match = re.search(r'_(amh|eng|ewe|fra|hau|ibo|kin|lin|lug|orm|sna|sot|swa|twi|vai|wol|xho|yor|zul)_', task_name)
    if match:
        return match.group(1)
    return None

def load_and_process_data():
    """Load all result files and process them"""
    results_dir = Path('data/results/result_cleaned')
    all_data = []
    
    for model_dir in results_dir.iterdir():
        if model_dir.is_dir():
            model_name = model_dir.name
            
            for csv_file in model_dir.glob('*.csv'):
                task_name = csv_file.stem
                
                try:
                    df = pd.read_csv(csv_file)
                    df['Model'] = model_name
                    df['Task'] = task_name
                    df['Language'] = df['Tasks'].apply(extract_language)
                    all_data.append(df)
                    
                except Exception as e:
                    print(f"Error processing {csv_file}: {e}")
    
    return pd.concat(all_data, ignore_index=True)

def calculate_detailed_averages(df):
    """Calculate detailed averages including model-language combinations"""
    
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
    language_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    language_stats = language_stats.reset_index()
    
    # Averages by model
    model_stats = df.groupby('Model').agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    model_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    model_stats = model_stats.reset_index()
    
    # Averages by task
    task_stats = df.groupby('Task').agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    task_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    task_stats = task_stats.reset_index()
    
    # Averages by model-language combination
    model_lang_stats = df.groupby(['Model', 'Language']).agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    model_lang_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    model_lang_stats = model_lang_stats.reset_index()
    
    # Averages by task type (afrimgsm, afrimmlu, afrixnli)
    df['Task_Type'] = df['Task'].str.extract(r'(afrimgsm|afrimmlu|afrixnli)')[0]
    task_type_stats = df.groupby(['Task_Type', 'Model']).agg({
        'Value': ['mean', 'count'],
        'Stderr': 'mean'
    }).round(4)
    task_type_stats.columns = ['Value_Avg', 'Count', 'Stderr_Avg']
    task_type_stats = task_type_stats.reset_index()
    
    return total_avg, language_stats, model_stats, task_stats, model_lang_stats, task_type_stats

def main():
    print("Loading and processing data...")
    df = load_and_process_data()
    
    print(f"Total records loaded: {len(df)}")
    print(f"Languages found: {sorted(df['Language'].unique())}")
    print(f"Models found: {sorted(df['Model'].unique())}")
    print(f"Tasks found: {sorted(df['Task'].unique())}")
    print("\n" + "="*60)
    
    # Calculate averages
    total_avg, language_stats, model_stats, task_stats, model_lang_stats, task_type_stats = calculate_detailed_averages(df)
    
    # Display results
    print("OVERALL AVERAGES:")
    print(f"Total Value Average: {total_avg['Total_Value_Avg']:.4f}")
    print(f"Total Stderr Average: {total_avg['Total_Stderr_Avg']:.4f}")
    print(f"Total Count: {total_avg['Total_Count']}")
    print("\n" + "="*60)
    
    print("AVERAGES BY LANGUAGE:")
    print(language_stats.to_string(index=False))
    print("\n" + "="*60)
    
    print("AVERAGES BY MODEL:")
    print(model_stats.to_string(index=False))
    print("\n" + "="*60)
    
    print("AVERAGES BY TASK:")
    print(task_stats.to_string(index=False))
    print("\n" + "="*60)
    
    print("AVERAGES BY MODEL-LANGUAGE COMBINATION:")
    print(model_lang_stats.to_string(index=False))
    print("\n" + "="*60)
    
    print("AVERAGES BY TASK TYPE AND MODEL:")
    print(task_type_stats.to_string(index=False))
    
    # Save results to CSV files
    language_stats.to_csv('language_averages.csv', index=False)
    model_stats.to_csv('model_averages.csv', index=False)
    task_stats.to_csv('task_averages.csv', index=False)
    model_lang_stats.to_csv('model_language_averages.csv', index=False)
    task_type_stats.to_csv('task_type_averages.csv', index=False)
    
    print("\n" + "="*60)
    print("Results saved to:")
    print("- language_averages.csv")
    print("- model_averages.csv") 
    print("- task_averages.csv")
    print("- model_language_averages.csv")
    print("- task_type_averages.csv")
    
    # Additional insights
    print("\n" + "="*60)
    print("KEY INSIGHTS:")
    
    # Best performing model
    best_model = model_stats.loc[model_stats['Value_Avg'].idxmax()]
    print(f"Best performing model: {best_model['Model']} (Value: {best_model['Value_Avg']:.4f})")
    
    # Best performing language
    best_language = language_stats.loc[language_stats['Value_Avg'].idxmax()]
    print(f"Best performing language: {best_language['Language']} (Value: {best_language['Value_Avg']:.4f})")
    
    # Best performing task
    best_task = task_stats.loc[task_stats['Value_Avg'].idxmax()]
    print(f"Best performing task: {best_task['Task']} (Value: {best_task['Value_Avg']:.4f})")
    
    # Worst performing language
    worst_language = language_stats.loc[language_stats['Value_Avg'].idxmin()]
    print(f"Worst performing language: {worst_language['Language']} (Value: {worst_language['Value_Avg']:.4f})")

if __name__ == "__main__":
    main() 