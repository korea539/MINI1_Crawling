import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup as bs
import time
from tqdm import trange


page_no = 1
url = f"https://www.mfds.go.kr/brd/m_228/list.do?page={page_no}&srchFr=&srchTo=&srchWord=&srchTp=&itm_seq_1=0&itm_seq_2=0&multi_itm_seq=0&company_cd=&company_nm="
response = requests.get(url)
html = bs(response.text, "html.parser")
post_no = 1
# bs select 가져오기
title = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > a")

# 리스트 형태에서 문자열 형태로 변환
title_str = title[0].get_text()
# 문자열 형태 변환 후 분리
title_split = title_str.split()
# 나눠진 문자열을 다시 하나의 제목으로 합치기
title_join = " ".join(title_split)

part = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > div > p:nth-of-type(1)")
part_str = part[0].get_text().split(" | ")[-1]
view = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > div > p:nth-of-type(2)")
view_str = int(view[0].get_text().split(" | ")[-1])
day = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.right_column")
day_str = pd.to_datetime(day[0].get_text())


title_list = []
for i in range(1, 11):
    post_no = i
    title = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > a")
    title_str = title[0].get_text()
    title_split = title_str.split()
    title_join = " ".join(title_split)
    title_list.append(title_join)

part_list = []
for i in range(1, 11):
    post_no = i
    part = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > div > p:nth-of-type(1)")
    part_str = part[0].get_text().split(" | ")[-1]
    part_list.append(part_str)
    
view_list = []
for i in range(1, 11):
    post_no = i
    view = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > div > p:nth-of-type(2)")
    view_str = view[0].get_text().split(" | ")[-1]
    view_int = int(view_str)
    view_list.append(view_int)
    
day_list = []
for i in range(1, 11):
    post_no = i
    day = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.right_column")
    day_str = day[0].get_text()
    day_list.append(day_str)
    
df = pd.DataFrame(zip(title_list, view_list, part_list, day_list), columns = ['제목', '조회수', '담당부서', '날짜'])


# 1 페이지부터 10 페이지의 데이터를 불러오는 함수 제작
edu_list = []
for page_no in trange(1, 11):
    url = f"https://www.mfds.go.kr/brd/m_228/list.do?page={page_no}&srchFr=&srchTo=&srchWord=&srchTp=&itm_seq_1=0&itm_seq_2=0&multi_itm_seq=0&company_cd=&company_nm="
    response = requests.get(url)
    html = bs(response.text, "html.parser")

    title_list = []
    for i in range(1, 11):
        post_no = i
        title = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > a")
        title_str = title[0].get_text()
        title_split = title_str.split()
        title_join = " ".join(title_split)
        title_list.append(title_join)

    part_list = []
    for i in range(1, 11):
        post_no = i
        part = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > div > p:nth-of-type(1)")
        part_str = part[0].get_text().split(" | ")[-1]
        part_list.append(part_str)
    
    view_list = []
    for i in range(1, 11):
        post_no = i
        view = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.center_column > div > p:nth-of-type(2)")
        view_str = view[0].get_text().split(" | ")[-1]
        view_int = int(view_str)
        view_list.append(view_int)
    
    day_list = []
    for i in range(1, 11):
        post_no = i
        day = html.select(f"#content > div.bbs_list01 > ul > li:nth-of-type({post_no}) > div.right_column")
        day_str = day[0].get_text()
        day_list.append(day_str)
    
    df = pd.DataFrame(zip(title_list, view_list, part_list, day_list), columns = ['제목', '조회수', '담당부서', '날짜'])
    edu_list.append(df)
    time.sleep(0.01)


# 리스트를 데이터 프레임으로 합치기
df_edu = pd.concat(edu_list)
# 결측치 제거 및 index를 리셋
df_edu.dropna()
df_edu.reset_index(drop = True, inplace=True)


# 파일로 저장
df_edu.to_csv("mfds_edu_promo.csv", encoding="cp949")
