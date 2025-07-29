# fotmob player stat crawling
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys     #enter key
from selenium.webdriver.support.ui import WebDriverWait
# from selenium.common.exceptions import NoSuchElementException
from bs4 import BeautifulSoup
import pymysql
import time

league = input("Choose the league What you want to insert: ")

url ="https://www.fotmob.com/"   # 리그 전체
user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"
options=Options()
options.add_argument("--start-maximized")
options.add_experimental_option("detach",True)
options.add_argument("lang=en-US")  # 브라우저 언어 설정을 영어로
options.add_argument("--disable-features=Translate")  # 자동 번역 방지
options.add_argument('user-agent='+ user_agent)

driver = webdriver.Chrome(options=options)
driver.get(url)     #url 접속
driver.implicitly_wait(7)
time.sleep(2)

#검색창 입력
if league == "1" :
    league = "Premier League"    # 20 / 2~22
elif league == "2":
    league = "LaLiga"          # 20 / 2~22
elif league == "3":
    league = "Bundesliga"        # 18 / 2~20
elif league == "4":
    league = "Serie A"           # 20 / 2~22
elif league == "5":
    league = "Ligue 1"           # 18 / 2~20
elif league == "6":
    league = "Eredivisie"        # 4  / 2~6

input_league = driver.find_element(By.CSS_SELECTOR,'#__next > header > section > div > div.css-kabrls-SearchBoxCSS.ee94nqm0 > div > div.css-16pz7yp-InputWrapper.ee94nqm6 > div > input')
input_league.send_keys(league)  # 검색창 입력     # 리그마다 변경필요
driver.implicitly_wait(7)

#최상단 리그 링크 클릭
search_btn = driver.find_element(By.CSS_SELECTOR,'#__next > header > section > div > div.css-kabrls-SearchBoxCSS.ee94nqm0 > div > div.css-2lil2b-SearchResultsBox.ee94nqm1 > div.css-rpnuoc-SearchBoxResults.ee94nqm2 > div > div:nth-child(1) > a > div')
search_btn.click()
driver.implicitly_wait(7)
time.sleep(5)

#클럽 링크 접속 2~22 / 2:1등 3:2등  ...
for i in range(15,15 + 1):           # 리그마다 변경필요
    click_club = driver.find_element(By.CSS_SELECTOR,f'#main-content > section > div > section > div > section > div.css-10wb1x-Column-LeftColumn.e15hvem01 > div:nth-child(1) > section > article > div > div > div > div:nth-child({i+1})')
    click_club.click()                              
    driver.implicitly_wait(7)
    time.sleep(3)              

    #스쿼드 접속
    # click_squad = driver.find_element(By.LINK_TEXT,'Squad')
    click_squad = driver.find_element(By.CSS_SELECTOR,'#main-content > section > div > div > section > nav > a:nth-child(4)')

    click_squad.click()
    driver.implicitly_wait(7)
    time.sleep(3)

    html_squad = driver.page_source
    soup_squad = BeautifulSoup(html_squad,"html.parser")
    club = soup_squad.find('span',class_="css-2irgse-TextOnDesktop eptdz4j1").text

    # 클럽 내 선수들 기본 정보
    name,number,height,country,position,age,p_foot,value,photo = [],[],[],[],[],[],[],[],[]
    # 클럽 내 선수들 리그 스탯
    c_sheets,saved_penal,g_conceded,matches,minutes,goals,assists,started,rating = [],[],[],[],[],[],[],[],[]
    # GK 개수 세기
    cnt_gk = []   

    #스쿼드 내 모든 선수들
    cnt_player = 0
    player_all = soup_squad.find_all('tr',class_="css-1209rpp-SquadTr e7m07zq9") 
    for indiv in range(2,len(player_all)+1): 
        click_player1 = driver.find_element(By.CSS_SELECTOR,f"#main-content > section > div > div.css-yx0osv-Column.e152ovrx0 > div.css-7xqg4w-CardCSS.e1mlfzv61 > table > tbody > tr:nth-child({indiv}) > td.css-l5mpv5-SquadPlayerTd.e7m07zq10 > a")
        click_player1.click()                               
        driver.implicitly_wait(7)
        time.sleep(3)
    
        # player page
        html_player = driver.page_source  # Selenium에서 현재 렌더링된 페이지 HTML 가져오기
        soup_player_indiv = BeautifulSoup(html_player,"html.parser")

        type_league_stat = soup_player_indiv.find('h2',class_="css-1a7b1vt-HeaderText e1sj9c203")


        if type_league_stat == None:         # 리그 스탯이 없으면 뒤로가기
            driver.execute_script("window.history.back();")
            driver.implicitly_wait(5)
            time.sleep(1.5)

        elif "2024/2025" not in type_league_stat.text:     # 다른 시즌 스탯이면 뒤로가기   # 리그마다 변경필요
            driver.execute_script("window.history.back();")
            driver.implicitly_wait(5)
            time.sleep(1.5)
        
        else:
            print(f"clear{cnt_player}")
            cnt_player += 1
            league_stat_name = soup_player_indiv.find_all('span',class_="css-1xy07gm-StatTitle e1sj9c204")
            cnt_rating = []
            for stat in league_stat_name:
                cnt_rating.append(stat.text.strip())

            if "Rating" not in cnt_rating:       # 리그 스탯에서 평점이 없으면 뒤로가기
                driver.execute_script("window.history.back();")
                driver.implicitly_wait(5)   
                time.sleep(1.5)
            
            else:  
                #사진
                player_Icon=soup_player_indiv.find('img',class_="Image PlayerImage ImageWithFallback")
                icon=player_Icon.attrs['src']   # url
                if icon.count("/") != 5:
                    url_num = None
                else:
                    url_num=icon.split("/")[5][:-4]
                

                # 이름
                player_name = soup_player_indiv.find('h1', class_="css-1btnu16-PlayerNameCSS etnb9n41").text


                # 포지션
                player_position = soup_player_indiv.find('div', class_="css-1g41csj-PositionsCSS ek22dvl6").text

                # player 기본 정보
                player_stat_name = soup_player_indiv.find_all('div', class_="css-tp32vr-StatTitleCSS e1e6xf3b1")
                player_stat_value = soup_player_indiv.find_all('div', class_="css-to3w1c-StatValueCSS e1e6xf3b2")
                                                                        
                # 기본 정보 딕셔너리
                player_data = {"name": player_name,"position": player_position,"height": None,"number": None,"p_foot": None,"country": None,"value": None,"age":None }

                for idx, stat in enumerate(player_stat_name):
                    if stat.text == "Height":
                        str_height = player_stat_value[idx].text
                        player_data["height"] = str_height[:-3]
                    elif stat.text == "Shirt":
                        player_data["number"] = player_stat_value[idx].text
                    elif stat.text == "Preferred foot":
                        player_data["p_foot"] = player_stat_value[idx].text
                    elif stat.text == "Country":
                        player_data["country"] = player_stat_value[idx].text
                    elif stat.text == "Market value":
                        def value_func(value_indiv):
                            if "M" in value_indiv:  # 100만단위
                                fin_value=float(value_indiv[1:-1])*1000000
                            elif "K" in value_indiv:   # 1000단위
                                fin_value=float(value_indiv[1:-1])*1000
                            return fin_value                          
                        player_data["value"] = value_func(player_stat_value[idx].text)
                    elif "years" in player_stat_value[idx].text:
                        str_age = player_stat_value[idx].text
                        player_data["age"] = str_age[:2]
                    
                # else:
                if player_data["name"] not in name:
                    name.append(player_data["name"])
                    position.append(player_data["position"])
                    height.append(player_data["height"])
                    number.append(player_data["number"])
                    p_foot.append(player_data["p_foot"])
                    country.append(player_data["country"])
                    value.append(player_data["value"])
                    age.append(player_data["age"])                     
                    photo.append(url_num)
                time.sleep(0.5)

                def str_slice_num(str):
                            for i in range(len(str)):
                                if str[i].isalpha():
                                    return [str[:i],str[i:]]
                # 리그 스탯 
                league_stat_value = soup_player_indiv.find_all('div',class_="css-vohuhg-StatBox e1sj9c206")
                # player중 에서 포지션마다 다른 특성은 따로 저장                  
                if player_position == "Keeper":  # GK
                    cnt_gk.append("keepers")    
                    GK_league_data = {"c_sheets":None,"g_conceded":None,"saved_penal":None,"matches":None,"minutes":None,"rating":None}
                    
                    for idx in range(len(league_stat_value)):
                        stat = str_slice_num(league_stat_value[idx].text)
                        if stat[1] == "Clean sheets":
                            GK_league_data["c_sheets"] = stat[0]
                        elif stat[1] == "Goals conceded":
                            GK_league_data["g_conceded"] = stat[0]
                        elif stat[1] == "Saved penalties":
                            GK_league_data["saved_penal"] = stat[0]
                        elif stat[1] == "Matches":
                            GK_league_data["matches"] = stat[0]
                        elif stat[1] == "Minutes played":
                            min_0 = stat[0]
                            if ',' in stat[0]:
                                min_1 = min_0.replace(",","")
                                GK_league_data["minutes"] = min_1
                            else:
                                GK_league_data["minutes"] = min_0
                        elif stat[1] == "Rating":
                            GK_league_data["rating"] = float(stat[0])
                        
                    c_sheets.append(GK_league_data["c_sheets"])
                    g_conceded.append(GK_league_data["g_conceded"])
                    saved_penal.append(GK_league_data["saved_penal"])
                    matches.append(GK_league_data["matches"])
                    minutes.append(GK_league_data["minutes"])
                    rating.append(GK_league_data["rating"])                   

                    driver.execute_script("window.history.back();")
                    driver.implicitly_wait(5)
                    time.sleep(1.5)
                
                else:
                    none_GK_league_data = {"goals":None,"assists":None,"started":None,"matches":None,"minutes":None,"rating":None}
                    for idx in range(len(league_stat_value)):
                        stat = str_slice_num(league_stat_value[idx].text)

                        if stat[1] == "Goals":
                            none_GK_league_data["goals"] = stat[0]
                        elif stat[1] == "Assists":
                            none_GK_league_data["assists"] = stat[0]
                        elif stat[1] == "Started":
                            none_GK_league_data["started"] = stat[0]
                        elif stat[1] == "Matches":
                            none_GK_league_data["matches"] = stat[0]
                        elif stat[1] == "Minutes played":
                            min_0 = stat[0]
                            if "," in min_0:    # 1000 이 넘는 출전 시간
                                min_1 = min_0.replace(",","")
                                none_GK_league_data["minutes"] = min_1
                            else:               # 1000 미만 출전 시간
                                none_GK_league_data["minutes"] = min_0
                        elif stat[1] == "Rating":
                            none_GK_league_data["rating"] = stat[0]

                    goals.append(none_GK_league_data["goals"])
                    assists.append(none_GK_league_data["assists"])
                    started.append(none_GK_league_data["started"])
                    matches.append(none_GK_league_data["matches"])
                    minutes.append(none_GK_league_data["minutes"])
                    rating.append(none_GK_league_data["rating"])
                    
                    driver.execute_script("window.history.back();")
                    driver.implicitly_wait(5)
                    time.sleep(1.5)  
    time.sleep(3.5)
    
    # GK, none_GK 분류
    count_gk=len(cnt_gk)

    photo_gk = photo[:count_gk]           ;   photo_none_gk = photo[count_gk:]
    name_gk = name[:count_gk]             ;   name_none_gk = name[count_gk:] 
    number_gk = number[:count_gk]         ;   number_none_gk = number[count_gk:]
    height_gk = height[:count_gk]         ;   height_none_gk = height[count_gk:] 
    country_gk = country[:count_gk]       ;   country_none_gk = country[count_gk:]
    position_gk = position[:count_gk]     ;   position_none_gk = position[count_gk:] 
    age_gk = age[:count_gk]               ;   age_none_gk = age[count_gk:]
    p_foot_gk = p_foot[:count_gk]         ;   p_foot_none_gk = p_foot[count_gk:] 
    value_gk = value[:count_gk]           ;   value_none_gk = value[count_gk:]
    matches_gk = matches[:count_gk]       ;   matches_none_gk = matches[count_gk:] 
    minutes_gk = minutes[:count_gk]       ;   minutes_none_gk = minutes[count_gk:]
    rating_gk = rating[:count_gk]         ;   rating_none_gk = rating[count_gk:]

    # 클럽 내 선수 SQL에 입력
    conn,cur = None,None
    sql = ""

    conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
    cur = conn.cursor()

    p_id1 = None ; p_id2 = None 
    for k in range(len(name_gk)):       # 리그마다 변경필요
        sql = "insert into gk_player values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (p_id1,league,club,name_gk[k],number_gk[k],height_gk[k],country_gk[k],position_gk[k],age_gk[k],p_foot_gk[k],value_gk[k],c_sheets[k],saved_penal[k],g_conceded[k],matches_gk[k],minutes_gk[k],rating_gk[k],photo_gk[k])
        cur.execute(sql,val)

    for m in range(len(name_none_gk)):  # 리그마다 변경필요
        sql = "insert into none_gk_player values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        val = (p_id2,league,club,name_none_gk[m],number_none_gk[m],height_none_gk[m],country_none_gk[m],position_none_gk[m],age_none_gk[m],p_foot_none_gk[m],value_none_gk[m],matches_none_gk[m],minutes_none_gk[m],goals[m],assists[m],started[m],rating_none_gk[m],photo_none_gk[m])
        cur.execute(sql,val)

    conn.commit()
    conn.close()

    print(f"{i}번째 클럽 입력 완료")

    driver.execute_script("window.history.back();")     # back to club overview
    driver.implicitly_wait(5)
    time.sleep(4)
    driver.execute_script("window.history.back();")     # back to league overview
    driver.implicitly_wait(5)
    time.sleep(4)

driver.quit()
print(f"{league} 입력 완료")   # 리그마다 변경필요