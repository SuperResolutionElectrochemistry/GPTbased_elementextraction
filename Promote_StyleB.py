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


# main function to extract high entropy elements from abstracts
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
                timeout=10.0,  
                )
        return response['choices'][0]['message']['content'].strip()
    except :
        return "API time out"


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
                while GPToutput == "API time out":
                    time.sleep(20)
                    GPToutput = Catalytic_Extract(abstract,a)
                    print(f"API time out，waiting for 20s to request again")

                GPToutputlist.append(GPToutput)
                abstract_processedlist.append(abstract)
                title_processedlist.append(title_list[row])
                
                print(f"Title：{title_list[row]}")
                print(f"GPToutput：{GPToutput}")
                print(f"Already finish {counts} articles")
                print("-" * 50)
                time.sleep(0)

        df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
        df.to_csv('./' + file + 'secondclean.csv', index=False, encoding='utf-8-sig')

