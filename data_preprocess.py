import numpy as np
import pandas as pd
import os
from pathlib import Path
import re,random,os,_frozen_importlib_external
from datasets import load_dataset
import codecs,csv
import jsonlines
import os


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

q_list = ['27', '28', '29', '30', '31', '32', '33', '34', '35', '37', '38', '39', '40', '41', '122', '123', '124', '125', '126', '127', '128', '129', '132', '133', '134', '135', '136', '137', '138', '158', '159', '160', '161', '162', '169', '170', '196', '197', '198', '224', '225', '226', '227', '228', '229', '230', '231', '232', '233']

def getPrompt(item, t, hasContext=False):
    #from llm_response import get_response_from_llm
    content = item['q_content']
    option = item['option']
    nums = re.findall(r"\d+",option)

    # if t % 2 == 1:
    #     p_prompt = getPassivePrompt(content)
    #     content = get_response_from_llm('gpt4', [p_prompt])[0]

    if '?' in content:
        prompt = f"Give me the answer from {min(nums)} to {max(nums)}: {content} {option}. You can only choose one option."
    else:
        prompt = f"Give me the answer from {min(nums)} to {max(nums)}: Do you agree with {content}? {option}. You can only choose one option."
 
    # if hasContext == True:
    #     num = random.randint(0, len(contexts)-1)
    #     cur_context = contexts[num]
    #     prompt = cur_context + ' ' + prompt

    return prompt
  

def generateFintuneData(country): 
    ans_item = dict()
    try:
        with codecs.open(f'data/{country}/{country}.csv', encoding='utf-8-sig') as f:
            # Read the first line to get headers
            header_line = f.readline().strip()
            headers = header_line.split(',')
            
            # Create a new reader with the headers
            f.seek(0)  # Go back to start of file
            reader = csv.DictReader(f, fieldnames=headers)
            
            print("Columns:", headers)
            found_avg = False
            for row in reader:
                if row['B_COUNTRY'] == 'Avg':
                    found_avg = True
                    ans_item = {'B_COUNTRY': row['B_COUNTRY'], 'B_COUNTRY_ALPHA': row['B_COUNTRY_ALPHA']}
                    for q in q_list:
                        k = 'Q' + q
                        try:
                            ans_item[k] = int(float(row[k]))
                        except (KeyError, ValueError) as e:
                            print(f"Error processing column {k}: {str(e)}")
                            print(f"Row data: {row}")
                            raise
                    print('Ans item populated:', ans_item)
                    break  # Exit after finding the Avg row
            
            if not found_avg:
                print("Warning: No 'Avg' row found in the CSV file")
                return

    except Exception as e:
        print(f"Error reading file: {str(e)}")
        return

    dir_path = f"data/{country}/Finetune"
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)

    with jsonlines.open(f"{dir_path}/WVQ_{country}.jsonl", "a") as writer:
        with open("data/WVQ.jsonl", "r+", encoding="utf8") as f:
            t = 0
            for item in jsonlines.Reader(f):
                prompt = getPrompt(item, t)
                print("\n" + item['q_id'], ' ', item['q_content'] + "\n")
                print('Q' + item['q_id'])
                print("\n" + prompt + "\n")
                
                q_key = 'Q' + item['q_id']
                if q_key not in ans_item:
                    print(f"Warning: {q_key} not found in ans_item. Available keys: {list(ans_item.keys())}")
                    continue
                    
                ans = ans_item[q_key]
                if ans < 0:
                    ans = 0 - ans
                new_item = {"messages": [{"role": "system", "content": f"You are an {country} chatbot that know {country} very well."}, 
                                        {"role": "user", "content": prompt}, 
                                        {"role": "assistant", "content": str(ans)}]}
                writer.write(new_item)
                t += 1
        with open("data/data_500_types_mini.jsonl", "r+", encoding="utf8") as f:
            t = 0
            for item in jsonlines.Reader(f):
                prompt = getPrompt(item, t)
                print(item['q_id'], ' ', item['q_content'])
                print(prompt)
                # prompt = translate(prompt)
                # print(prompt)
                ans = ans_item['Q'+item['q_id']]
                if ans < 0:
                    ans = 0 - ans
                new_item = {"messages": [{"role": "system", "content": f"You are an {country} chatbot that know {country} very well."}, 
                                        {"role": "user", "content": prompt}, 
                                        {"role": "assistant", "content": str(ans)}]}
                writer.write(new_item)
                t += 1
    print('ok!')

def generateData4Llama(country):
    def formatting_func(example):
        text = f"### Question: {example['messages'][1]['content']}\n ### Answer: {example['messages'][2]['content']}"
        return text
    
    path_name = f'data/{country}/Finetune/WVQ_{country}'
    dataset = load_dataset('json', data_files=f'{path_name}.jsonl', split='train')

    with jsonlines.open(f'{path_name}_llama.jsonl',mode='a') as writer:
        for item in dataset:
            text = formatting_func(item)
            new_item = {'text': text}
            writer.write(new_item)
    print('ok!')


if __name__ == '__main__':
    #process_all_data()
    #generateFintuneData('Zimbabwe')
    #generateData4Llama('Zimbabwe') 
    print(0)   