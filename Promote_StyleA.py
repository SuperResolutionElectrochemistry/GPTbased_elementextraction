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
        return "API time out"


for file in os.listdir('./TEST'):
    file = './TEST/' + file
    
    with open(file, newline='', encoding='utf-8') as csvfile:
        
        reader = pd.read_excel(file, sheet_name=0, header=0, index_col=0)
        
 
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
                
                while GPToutput == "API time out":
                    time.sleep(20)
                    GPToutput = Abstract_promote(abstract,a)
                    print(f"API time out，waiting for 20 seconds to request again")

                GPToutputlist.append(GPToutput)
                abstract_processedlist.append(abstract)
                title_processedlist.append(title_list[row])
                
                print(f"Title：{title_list[row]}")
                print(f"GPToutput：{GPToutput}")
                print(f"Already finish {counts} articles")
                print("-" * 50)
                time.sleep(0)
                if counts % 400 == 0:
                    temp = './temp/' + str(counts) + '.csv'
                    df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
                    df.to_csv(temp, index=False, encoding='utf-8-sig')            


df = pd.DataFrame(list(map(list, zip(*[GPToutputlist,title_processedlist,abstract_processedlist]))), columns=['output','title','abstract'])
df.to_csv('./paradigm of Extraction.csv', index=False, encoding='utf-8-sig')

