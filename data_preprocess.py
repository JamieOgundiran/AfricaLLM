import numpy as np
import pandas as pd
import os
from pathlib import Path

import warnings 
warnings.filterwarnings('ignore')

def preprocess_data(file_path):
    # Read the CSV file
    df = pd.read_csv(file_path, sep=';')
    
    # Define the columns to keep
    q_list = [
        'B_COUNTRY_ALPHA', 'B_COUNTRY', 'LNGE_ISO', 'Q27', 'Q28', 'Q29', 'Q30', 'Q31', 'Q32', 'Q33', 'Q34', 'Q35', 'Q37', 'Q38', 'Q39', 'Q40', 'Q41', 'Q122', 'Q123', 'Q124', 'Q125', 'Q126', 'Q127', 'Q128', 'Q129', 'Q132', 'Q133', 'Q134', 'Q135', 'Q136', 'Q137', 'Q138', 'Q158', 'Q159', 'Q160', 'Q161', 'Q162', 'Q169', 'Q170', 'Q196', 'Q197', 'Q198', 'Q224', 'Q225', 'Q226', 'Q227', 'Q228', 'Q229', 'Q230', 'Q231', 'Q232', 'Q233'
    ]
    
    # Filter the DataFrame to only those columns
    df_q = df[q_list]
    
    # Calculate averages for Q columns
    q_columns = [col for col in df_q.columns if col.startswith('Q')]
    avg_row = df_q[q_columns].mean().to_dict()
    
    # For non-Q columns, leave blank except B_COUNTRY = 'Avg'
    for col in df_q.columns:
        if col not in q_columns:
            avg_row[col] = ''
    avg_row['B_COUNTRY'] = 'Avg'
    
    # Ensure columns order matches original
    avg_row = {col: avg_row.get(col, '') for col in df_q.columns}
    
    # Append average row to DataFrame
    df_with_avg = pd.concat([df_q, pd.DataFrame([avg_row])], ignore_index=True)
    
    return df_with_avg

def process_all_data():
    # Get the data directory path
    data_dir = Path('data')
    
    # Create output directory if it doesn't exist
    output_dir = data_dir / 'processed'
    output_dir.mkdir(exist_ok=True)
    
    # Process each country directory
    for country_dir in data_dir.iterdir():
        if country_dir.is_dir() and country_dir.name != 'processed':
            print(f"Processing {country_dir.name}...")
            
            # Find CSV files in the country directory
            csv_files = list(country_dir.glob('*.csv'))
            
            for csv_file in csv_files:
                try:
                    # Process the file
                    processed_df = preprocess_data(csv_file)
                    
                    # Create output filename
                    output_file = output_dir / f"{country_dir.name}_{csv_file.stem}_processed.csv"
                    
                    # Save processed data
                    processed_df.to_csv(output_file, index=True)
                    print(f"Processed {csv_file.name} -> {output_file.name}")
                    
                except Exception as e:
                    print(f"Error processing {csv_file.name}: {str(e)}")

if __name__ == "__main__":
    process_all_data()