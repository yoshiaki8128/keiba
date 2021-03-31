import requests
from bs4 import BeautifulSoup
import pandas 
import time
import sys
import re
import itertools

sitename = "https://race.netkeiba.com/race/result.html?race_id=202001010101"
 
 

try:
    #HTML取得
    res = requests.get(sitename)    
    #例外処理
    res.raise_for_status()

    soup = BeautifulSoup(res.content,"lxml")
        
    #タイトル
    title_text = soup.find('title').get_text()
    print(title_text)

    #馬名
    horse_names = soup.find_all('span',class_ = 'Hores_Name')
    horse_names_list = []
    for horse_name in horse_names:
        #馬名のみ
        horse_name = horse_name.get_text().lstrip().rstrip('¥n')
        horse_names_list.append(horse_name)
    print(horse_names_list)


    
except:
    print(sys.exc_info())
    print("サイトが取得できませんでした")