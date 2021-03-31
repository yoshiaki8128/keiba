import requests
from bs4 import BeautifulSoup
import pandas 
import time
import sys
import re
import itertools

#レースID作成
#レースIDは、年・競馬場・開催回数・日数・何回目で構成
YEAR = ['2020']
CODE = [str(num + 1).zfill(2) for num in range(10)]
RACE_COUNT = ['01']
DAYS = ['01']
RACE_NUM = ['01']
race_ids = list(itertools.product(YEAR,CODE,RACE_COUNT,DAYS,RACE_NUM))
#URL作成
SITE_URL = ["https://race.netkeiba.com/race/result.html?race_id={}".format(''.join(race_id)) for race_id in race_ids]

result_df = pandas.DataFrame()

for sitename,race_id in zip(SITE_URL,race_ids):
    time.sleep(2)

    try:
        #HTML取得
        res = requests.get(sitename)    
        #例外処理
        res.raise_for_status()

        soup = BeautifulSoup(res.content,"lxml")
        
        #タイトル
        title_text = soup.find('title').get_text()
        print(title_text)

        #順位
        ranks = soup.find_all('div',class_ = 'Rank')
        ranks_list =[]
        for rank in ranks:
            rank = rank.get_text()
            ranks_list.append(rank)
        print(ranks_list)
        #馬名
        horse_names = soup.find_all('span',class_ = 'Hores_Name')
        horse_names_list = []
        for horse_name in horse_names:
            #馬名のみ
            horse_name = horse_name.get_text().lstrip().rstrip('¥n')
            horse_names_list.append(horse_name)
        print(horse_names_list)
        #人気
        populars = soup.find_all('span',class_ = 'OddsPeople')
        populars_list = []
        for popular in populars:
            popular = popular.get_text()
            populars_list.append(popular)
        print(populars_list)
        #枠
        frames = soup.find_all('td',class_ = re.compile("Num Wake"))
        frames_list = []
        for frame in frames:
            frame = frame.get_text().replace('¥n','')
            frames_list.append(frame)
        print(frames_list)
        #距離、コース
        distance_course = soup.find_all('span')
        distance_course = re.search(r',[0-9]+m',str(distance_course))
        distance = re.sub("¥¥D","",distance_course)
        course = distance_course.group()[0]
        print(distance_course)
        
        df = pandas.DataFrame({
            'レースID':''.join(race_id),
            '順位':ranks_list,
            '枠':frames_list,
            '馬名':horse_names_list,
            'コース':course,
            '距離':distance,
            '人気':populars_list,
        })

        result_df = pandas.concat( [result_df,df],axis=0) 



    
    except:
        print(sys.exc_info())
        print("サイトが取得できませんでした")