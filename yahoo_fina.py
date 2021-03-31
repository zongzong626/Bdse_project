from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np

tick = input("tick")

url = f"https://finance.yahoo.com/quote/{tick}.TW/financials?p={tick}.TW"


html = requests.get(url).text
soup = BeautifulSoup(html,'lxml')
table = soup.find_all("div" , class_ = "M(0) Whs(n) BdEnd Bdc($seperatorColor) D(itb)")
titles = table[0].find_all("div",class_ ="D(tbr) C($primaryColor)")
contexts = table[0].find_all("div",{"data-test" :"fin-row"})
titles = titles[0].find_all("div")


df = {}
li = []
for title in titles:
    if title.span != None:
        li.append(title.span.text)

df[li.pop(0)] = li


for context  in contexts:
    datas =  context.find_all("div",class_ = "D(tbr) fi-row Bgc($hoverBgColor):h")
    for data in datas:
        ls = []
        for co in data:
            if co.span == None:

                ls.append(np.NAN)
            else :

                ls.append(co.span.text)
        df[ls.pop(0)] = ls

df2 = pd.DataFrame(df)
df3 = df2.T
df3.columns = df3.iloc[0,:]
df3.drop("Breakdown",axis=0,inplace=True)
print(df3)














    # datas =  context.find_all("div")
    # for data in datas:
    #     print(data.text)








