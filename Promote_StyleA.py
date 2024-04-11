import openai
import pandas as pd
import csv
import os
import xlrd
import time
import requests

ArticleResearchlist = []
ArticleTypelist = []
high_entropy_elements_list = []
abstract_processedlist = []
title_processedlist = []
ArticleResearch = []
ArticleType = []
high_entropy_elements = []
abstract_processed = []
title_processed = []
GPToutputlist = []
GPToutput = []
a = 1
counts = 0

def api_exchange():
    # Set up GPT API key
    with open('./api_key.txt', 'r') as f:
        api_key = f.read()
    
    return api_key


# 函数来提取文献摘要中的高熵合金元素组分
def Abstract_promote(abstract,a):
    
    openai.api_key = api_exchange()
    openai.api_base = "https://api.kwwai.top/v1"
    
    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                         {"role": "system", "content": f"You are a research chemist focus on High Entropy materials."},
                         {"role": "user", "content": f" High entropy materials is defined as materials consisting of at least five different metals. It is also been named as High Entropy Alloys or HEAs. "},
                         {"role": "user", "content": f" The identification of ORR and HER: Oxygen Reduction Reaction or ORR is a electrocatalytic reaction turning Oxygen into H2O, and it is different from Oxygen Evolution Reaction ; Hydrogen Evolution Reaction is a reaction that occurs on electrocatalyst in water, turning H2O into H2, which is different from Hydrogenation and hydrogen stroage. "},
                         {"role": "user", "content": f" According to previous result, Hydrogen Evolution Reaction could be misunderstood with HEAs or HEA, but it is not. "},
                         {"role": "user", "content": f" I will submit a Abstract of a research article ,identify if this article is studying high entropy materials: if yes,reply'Research on high entropy materials';if not, reply'Other Research'"},
                         {"role": "user", "content": f" Analysis the detail research field of this article, identify if this article is studying catalyst or catalytic: if yes,reply'Catalytic Research';if not, reply'Other Research'"},
                         {"role": "user", "content": f" Analysis the specified research field of this article, identify if this article is studying Oxygen Reduction Reaction in electrocatalyst : if yes,reply'Research on ORR';if not, reply'Other Research'"},
                         {"role": "user", "content": f" If this abstract from the article studies high entropy materials,recognize it is a review article or a research article, reply 'research' or 'review',if don't belong to both, reply 'NULL'"},
                         {"role": "user", "content": f" If this abstract from a research article, summarize the abstract and analysis the metal elements that authors choosen as the compound of High entropy materials they investigated, if there were no metal elements mentioned or Empty Input or any information is not provided or you are unsure, reply 'NULL'"},
                         {"role": "user", "content": f" Your answer should be standardized with the following chart: \nArticle research on High entropy materials or not:\nDetailed Research Field:\nSpecified Research Field:\nArticle Type: Research or Review\nElements: 1, 2, 3, \n. To be noted, if you are unsure, please reply 'NULL', and the elements should be symbolized with English abbreviation only, for example, if the elements are Iron, Cobalt, Nickel, please reply 'Fe, Co, Ni'"},
                         {"role": "user", "content": f" Abstact:{abstract}"}
                     ],
                                timeout=10.0,  
                )
        return response['choices'][0]['message']['content'].strip()
    except :
        return "API请求超时"


for file in os.listdir('./TEST'):
    file = './TEST/' + file
    
    with open(file, newline='', encoding='utf-8') as csvfile:
        
        reader = pd.read_excel(file, sheet_name=0, header=0, index_col=0)
        
        # for row in range(len(reader['Abstract'])):
        #     abstract_list = reader['Abstract']  # 假设文献摘要在CSV的第一列
        for row in range(len(reader['Abstract'])):
            title_list = reader['Article Title']
            abstract_list = reader['Abstract']  
            abstract = abstract_list[row]
            counts += 1
            if counts > 0:
                GPToutput = Abstract_promote(abstract,a)
                a += 1
                if a == 4:
                    a = 1
                #当extract_high_entropy_elements(abstract)超时时，会返回"API请求超时"，这里判断一下，如果返回的是"API请求超时"，则等待20秒后再次请求
                while GPToutput == "API请求超时":
                    time.sleep(20)
                    GPToutput = Abstract_promote(abstract,a)
                    print(f"API请求超时，等待20秒后再次请求")

                GPToutputlist.append(GPToutput)
                abstract_processedlist.append(abstract)
                title_processedlist.append(title_list[row])
                
                print(f"标题：{title_list[row]}")
                print(f"GPToutput：{GPToutput}")
                print(f"已提取{counts}条文献摘要")
                print("-" * 50)
                time.sleep(0)
                if counts % 400 == 0:
                    temp = './temp/' + str(counts) + '.csv'
                    #     df = pd.DataFrame(high_entropy_elements_list, columns=['高熵合金元素组分'])
                    #     df.to_csv(temp, index=False, encoding='utf-8-sig')
                    df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
                    df.to_csv(temp, index=False, encoding='utf-8-sig')


        

            

# 将提取的高熵合金元素组分写入CSV文件
df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
df.to_csv('./高熵合金元素组分处理结果-catrefine.csv', index=False, encoding='utf-8-sig')

