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
    # 设置你的ChatGPT API密钥
    with open('./api_key.txt', 'r') as f:
        api_key = f.read()
    
    return api_key


# 函数来提取文献摘要中的高熵合金元素组分
def Catalytic_Extract(abstract,a):

    openai.api_key = api_exchange()
    openai.api_base = "https://api.kwwai.top/v1"

    try:
        response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                         {"role": "system", "content": f"You are a research chemist focus on High Entropy materials."},
                         {"role": "user", "content": f" High entropy materials is defined as materials consisting of at least five different metals. It is also been named as High Entropy Alloys or HEAs. "},
                         {"role": "user", "content": f" The definition of Catalytic: making a chemical reaction happen more quickly by using a catalyst"},
                         {"role": "user", "content": f" High entropy materials is defined as materials consisting of at least five different metals. It is also been named as High Entropy Alloys or HEAs. "},
                         {"role": "user", "content": f" The definition of ORR: Oxygen Reduction Reaction or ORR is a electrocatalytic reaction into H2O, and it is different from Oxygen Evolution Reaction(OER) and Hydrogen Evolution Reaction(HER)."},
                         {"role": "user", "content": f" Abstact:{abstract}"},
                         {"role": "user", "content": f" title:{a}"},
                         {"role": "user", "content": f" This is a Abstract from a article, analysis this abstract with title, answer the questions as follows, all section should be fill, if you are uncertain about specific item,fill NULL"},
                         {"role": "user", "content": f" If the counts of Elements is less than five, please check your answer, read the abstract and title again and reply again"},
                         {"role": "user", "content": f" Your reply must be strictly standardized as the following questions: "},
                         {"role": "user", "content": f" Article research on Catalytic: Yes or No "},
                         {"role": "user", "content": f" Article research on Oxygen Reduction Reaction: Yes or No "},
                         {"role": "user", "content": f" Article research on High entropy materials: Yes or No"},
                         {"role": "user", "content": f" Article Type: Research or Review "},
                         {"role": "user", "content": f" Specific Elements: 1, 2, 3, etc."},
                         {"role": "user", "content": f" To be noted, if you are unsure, please reply 'NULL', and the elements should be symbolized with English abbreviation only, for example, if the elements are Iron, Cobalt, Nickel, please reply 'Fe, Co, Ni'"},
                     ],
                #prompt=f"This a Abstract about High-Entropy-Alloys, identify and summarize the elements that authors choosen as the compound of HEAs they investigated, please reply the elements list only, if there were no metal elements inside, please reply NULL \n{abstract}\n元素组分：",
                timeout=10.0,  # 设置超时时间（以秒为单位），这里设置为10秒
                )
        return response['choices'][0]['message']['content'].strip()
    except :
        return "API请求超时"


for file in os.listdir('./TEST'):
    file = './TEST/' + file
    
    with open(file, newline='', encoding='utf-8') as csvfile:
        
        reader = pd.read_excel(file, sheet_name=0, header=0, index_col=0,)       
        for row in range(len(reader['Abstract'])):
            #row = row + 1
            title_list = reader['Article Title']
            abstract_list = reader['Abstract']  
            abstract = abstract_list[row]
            counts += 1
            if counts > 0:
                GPToutput = Catalytic_Extract(abstract,a)
                a += 1
                if a == 4:
                    a = 1
                #当extract_high_entropy_elements(abstract)超时时，会返回"API请求超时"，这里判断一下，如果返回的是"API请求超时"，则等待20秒后再次请求
                while GPToutput == "API请求超时":
                    time.sleep(20)
                    GPToutput = Catalytic_Extract(abstract,a)
                    print(f"API请求超时，等待20秒后再次请求")

                GPToutputlist.append(GPToutput)
                abstract_processedlist.append(abstract)
                title_processedlist.append(title_list[row])
                
                print(f"标题：{title_list[row]}")
                print(f"GPToutput：{GPToutput}")
                print(f"已提取{counts}条文献摘要")
                print("-" * 50)
                time.sleep(0)
                #if counts % 400 == 0:
                    #temp = './temp/' + str(counts) + '.csv'
                    #     df = pd.DataFrame(high_entropy_elements_list, columns=['高熵合金元素组分'])
                    #     df.to_csv(temp, index=False, encoding='utf-8-sig')
                    #df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
                    #df.to_csv(temp, index=False, encoding='utf-8-sig')


        # 将提取的高熵合金元素组分写入CSV文件
        df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
        df.to_csv('./' + file + 'secondclean.csv', index=False, encoding='utf-8-sig')

