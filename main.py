import re,random,os,_frozen_importlib_external
import codecs,csv
import jsonlines

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

    with jsonlines.open(f"{dir_path}/WVQ_{country}_test3.jsonl", "a") as writer:
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

if __name__ == '__main__':
    import os

    data_root = 'data'
    for country in os.listdir(data_root):
        country_path = os.path.join(data_root, country)
        # skip anything that isn’t a directory
        if not os.path.isdir(country_path):
            continue

        # optional: skip any non-country folders
        if country.lower() in {'wvq.jsonl', 'data_500_types_mini.jsonl'}:
            continue

        print(f"--- Processing {country} ---")
        try:
            generateFintuneData(country)
        except Exception as e:
            print(f"Error processing {country}: {e}")
