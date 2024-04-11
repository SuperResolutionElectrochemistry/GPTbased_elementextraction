
#统计高熵合金元素组分出现次数
elements = ['NULL', 'Co', 'Cr', 'Cu', 'Fe', 'Mn', 'Mo', 'Nb', 'Ni', 'Ti', 'V', 'W', 'Zr', 'Sn', 'Ce']

elements_count = {'NULL':0, 'Co':0, 'Cr':0, 'Cu':0, 'Fe':0, 'Mn':0, 'Mo':0, 'Nb':0, 'Ni':0, 'Ti':0, 'V':0, 'W':0, 'Zr':0, 'Sn':0, 'Ce':0}

for i in range(len(high_entropy_elements_list)):
    for j in range(len(elements)):
        if elements[j] in high_entropy_elements_list[i]:
            elements_count[elements[j]] += 1
        print (high_entropy_elements_list[i])

            
# 将统计结果写入CSV文件
df = pd.DataFrame(elements_count.items(), columns=['元素', '出现次数'])
df.to_csv('./高熵合金元素组分统计-catrefine.csv', index=False, encoding='utf-8-sig')



                # GPToutput.split('\n')
                # for i in range(len(GPToutput.split('\n'))):
                #     if GPToutput.split('\n')[i] == 'Article research on High entropy materials or not:':
                #         ArticleResearch = GPToutput.split('\n')[i+1]
                #         if GPToutput.split('\n')[i+1] == 'Article Type: Research or Review':
                #             ArticleType = GPToutput.split('\n')[i+1]
                #             if GPToutput.split('\n')[i+2] == 'Elements:':
                #                 high_entropy_elements = GPToutput.split('\n')[i+1:]

                # ArticleResearchlist = ArticleResearchlist.append(ArticleResearch)
                # ArticleTypelist = ArticleTypelist.append(ArticleType)
                # high_entropy_elements_list.append(high_entropy_elements)
                # abstract_processedlist = abstract_processedlist.append(abstract)
                # title_processedlist = title_processedlist.append(title_list[row])