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
    with codecs.open(f'data/{country}/Ethiopia.csv', encoding='utf-8-sig') as f:
    # with codecs.open(f'data/{country}/{country}.csv', encoding='utf-8-sig') as f:
        for row in csv.DictReader(f, skipinitialspace=True):
            if row['B_COUNTRY'] == 'Avg':
            # if row['B_COUNTRY'] == 'Avg_First':
                ans_item = {'B_COUNTRY': row['B_COUNTRY'], 'B_COUNTRY_ALPHA': row['B_COUNTRY_ALPHA']}
                for q in q_list:
                    k = 'Q' + q
                    ans_item[k] = int(float(row[k]))
                print('Ans: ', ans_item)
    f.close()

    dir_path = f"data/{country}/Finetune"
    if os.path.exists(dir_path) == False:
        os.makedirs(dir_path)

    with jsonlines.open(f"{dir_path}/WVQ_{country}_test3.jsonl", "a") as writer:
        with open("data/WVQ.jsonl", "r+", encoding="utf8") as f:
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

generateFintuneData("Ethiopia")