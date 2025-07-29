# Searching football player in five League from FotMob

from tkinter import *
from tkinter.ttk import *   #combobox
import tkinter.messagebox as msgbox
import pymysql
import io
from urllib.request import urlopen          # url open
from PIL import Image as PILImage, ImageTk  # image 크기 변경

win_search=Tk()
win_search.title("player search")
win_search.geometry("1700x600+0+200")
win_search.resizable(False,False)
win_search.option_add("*Font","Courier 12")

frame_select = Frame(win_search,width=470,height=600)
frame_select.pack_propagate(FALSE)   # 프레임 크기 고정
frame_select["relief"]="raised"
frame_select.pack(side=LEFT)

frame_list = Frame(win_search,width=1230,height=550)
frame_list.pack_propagate(FALSE) 
frame_list.pack(side=LEFT)

ent_name = Entry(frame_select,width=42)
def clear(event):
    if ent_name.get() == "Name":
        ent_name.delete(0,len(ent_name.get()))

ent_name.insert(0,"Name")
ent_name.config(justify=CENTER)
ent_name.bind("<Button-1>",clear)       # 어떤 입력이 들어 왔을때 이러한 기능을 실행한다
ent_name.place(x=25,y=320)

def refresh():
    global nation_list
    cbox_league.set("Select League") 
    cbox_club.set("Select Club") ; club_list.clear() ; cbox_club.config(values=club_list)

    nation_list.clear()
    cur,conn = None,None
    conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
    cur = conn.cursor()

    sql_n_g = 'select distinct country from gk_player ;'        ; cur.execute(sql_n_g)
    result_n = cur.fetchall()
    for result in result_n:
        nation_list.append(result[0])
    sql_n_ng = 'select distinct country from none_gk_player ;'  ; cur.execute(sql_n_ng)
    result_n = cur.fetchall()
    for result in result_n:
        nation_list.append(result[0])
    conn.close()
    nation_list=sorted(list(set(nation_list)))

    cbox_nation.set("Select Nation")      ; cbox_nation.config(values=nation_list)
    cbox_position.set("Select Position")  ; ent_name.delete(0,len(ent_name.get()))  ; ent_name.insert(0,"Name")

    win_search.update()    

btn_refresh = Button(frame_select)    # 새로고침 버튼
btn_refresh.config(text="↺",width=4,command=refresh)
btn_refresh.place(x=420,y=30)

global nation_list
league_list,club_list,nation_list = [],[],[]

cur,conn = None,None

conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
cur = conn.cursor()

sql_l = "select distinct league from gk_player order by league;" ; cur.execute(sql_l)
result_l = cur.fetchall()
for result in result_l:
    league_list.append(result[0])

position_list = ["Keepers","Defenders","Midfielders","Forwards"]

sql_n_g = 'select distinct country from gk_player ;'             ; cur.execute(sql_n_g)
result_n = cur.fetchall()
for result in result_n:
    nation_list.append(result[0])

sql_n_ng = 'select distinct country from none_gk_player ;'       ; cur.execute(sql_n_ng)
result_n = cur.fetchall()
for result in result_n:
    nation_list.append(result[0])

conn.close()
nation_list = sorted(list(set(nation_list)))

cbox_league = Combobox(frame_select)
cbox_league.set("Select League") 
cbox_league.config(justify=CENTER,state="readonly",values=league_list)
cbox_league.place(x=15,y=80)

cbox_club = Combobox(frame_select)
cbox_club.set("Select Club")
cbox_club.config(justify=CENTER,state="readonly",values=club_list)
cbox_club.place(x=235,y=80)

cbox_position = Combobox(frame_select)
cbox_position.config(width=40)
cbox_position.set("Select Position")
cbox_position.config(justify=CENTER,state="readonly",values=position_list)
cbox_position.place(x=25,y=160)

cbox_nation = Combobox(frame_select)
cbox_nation.config(width=40)
cbox_nation.set("Select Nation")
cbox_nation.config(justify=CENTER,state="readonly",values=nation_list)
cbox_nation.place(x=25,y=240)

# 포지션 약자 변환
def trans_posit(x):
    if x == 'Keeper':
        return 'GK'
    elif x == 'Center-back':
        return 'CB'
    elif x == 'Left-back':
        return 'LB'
    elif x == 'Right-back':
        return 'RB'
    elif x == 'Central Midfielder':
        return 'CM'
    elif x == 'Attacking Midfielder':
        return 'AM'
    elif x == 'Defensive Midfielder':
        return "DM"
    elif x== "Right Winger":
        return 'RW'
    elif x == "Striker":
        return 'ST'
    elif x == 'Left Winger':
        return "LW"
    elif x == "Right Midfielder":
        return "RM"
    elif x == "Left Midfielder":
        return "LM"
    elif x == "Left Wing-Back":
        return "LWB"
    elif x == "Right Wing-Back":
        return "RWB"
    elif x == "defender":
        return "DF"
    elif x == "midfielder":
        return "MF"
    elif x == "forward":
        return "FW"

def no_msg():
    msgbox.showinfo("Notice","There are no applicable players.\nSelect another condition.")

def insert_listbox(sql):
    cur,conn = None,None
    conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
    cur = conn.cursor()

    cur.execute(sql)    # 매개변수로 sql을 받아 실행
    result_player = cur.fetchall()
    for result in result_player:
        if result[4] == None:   # number가 None인 경우 리스트박스 칸 수가 맞지 않는다
            number = "--"
        else:
            number = result[4]
        result_list = " {:<15.15}    {:<26.26}    {:<5}    {:<21.21}    {:<4}    {:<25}".format(f'{result[0]}∙',f'∙{result[1]}∙',f'∙{trans_posit(result[2])}∙',f'∙{result[3]}∙',f'∙{number}∙',f'∙{result[5]}∙')
        lbox_list.insert(END,result_list)
    conn.close()

def select(event=None):
    global nation_list
    lbox_list.delete(0,END)     # 리스트 박스 전체 삭제     

    # League O, Club X      / List X  -> 리그 선택시 해당리그의 클럽,국가들로 combobox 변경
    if cbox_league.get() != "Select League" and cbox_club.get() == "Select Club" and cbox_nation.get() == "Select Nation":
        # club 설정
        club_list.clear()
        cur,conn = None,None

        conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
        cur = conn.cursor()

        sql_l = f'select distinct club from gk_player where league = "{cbox_league.get()}" order by club ;'  ; cur.execute(sql_l)
        result_l = cur.fetchall()
        for result in result_l:
            club_list.append(result[0])
        cbox_club.config(values=club_list)

        # nation 설정
        nation_list.clear()
        sql_n_1 = f'select distinct country from gk_player where league = "{cbox_league.get()}";'            ; cur.execute(sql_n_1)
        result_n_1 = cur.fetchall()
        for result in result_n_1:
            nation_list.append(result[0])            
        sql_n_2 = f'select distinct country from none_gk_player where league = "{cbox_league.get()}" ;'      ; cur.execute(sql_n_2)
        result_n_2 = cur.fetchall()
        for result in result_n_2:
            nation_list.append(result[0])

        nation_list = sorted(list(set(nation_list)))
        cbox_nation.config(values=nation_list)
        cbox_nation.set("Select Nation")
        conn.close()
    
    elif cbox_club.get() != "Select Club" and cbox_nation.get() == "Select Nation":
        nation_list.clear()
        cur,conn = None,None

        conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
        cur = conn.cursor()

        sql_n_1 = f'select distinct country from gk_player where club = "{cbox_club.get()}";'        ; cur.execute(sql_n_1)
        result_n_1 = cur.fetchall()
        for result in result_n_1:
            nation_list.append(result[0])            
        sql_n_2 = f'select distinct country from none_gk_player where club = "{cbox_club.get()}" ;'  ; cur.execute(sql_n_2)
        result_n_2 = cur.fetchall()
        for result in result_n_2:
            nation_list.append(result[0])

        nation_list = sorted(list(set(nation_list)))
        cbox_nation.config(values=nation_list)
        cbox_nation.set("Select Nation")

        conn.close()

     #  Name    / Entry 우선
    if ent_name.get() != "Name":
        sql_l = f'select league,club,position_p,country,number,name from gk_player where name like"%{ent_name.get()}%" ;'  
        insert_listbox(sql_l)
      
        sql_l = f'select league,club,position_p,country,number,name from none_gk_player where name like"%{ent_name.get()}%" ;' 
        insert_listbox(sql_l)

    # (0) League O, Club X, Position X, Nation X     / List O
    elif cbox_league.get() !="Select League" and cbox_club.get() == "Select Club" and cbox_position.get() == "Select Position" and cbox_nation.get() == "Select Nation":
        sql_l = f'select league,club,position_p,country,number,name from gk_player where league = "{cbox_league.get()}" ;' 
        insert_listbox(sql_l)

        sql_l = f'select league,club,position_p,country,number,name from none_gk_player where league = "{cbox_league.get()}" ;' 
        insert_listbox(sql_l)
       
    # (1) League X, Club X, Position X, Nation O    
    elif cbox_league.get() == "Select League" and cbox_club.get() =="Select Club" and cbox_position.get() == "Select Position" and cbox_nation.get() != "Select Nation":
        
        sql_l = f'select league,club,position_p,country,number,name from gk_player where country = "{cbox_nation.get()}" ;' 
        insert_listbox(sql_l)

        sql_l = f'select league,club,position_p,country,number,name from none_gk_player where country = "{cbox_nation.get()}" ;' 
        insert_listbox(sql_l)

    # (2) League X, Club X, Position O, Nation O
    elif cbox_league.get()=="Select League" and cbox_position.get() !="Select Position" and cbox_nation.get() !="Select Nation":
        if cbox_position.get() == "Keepers":
            sql_l = f"select league,club,position_p,country,number,name from gk_player where country = '{cbox_nation.get()}';" 
           
        elif cbox_position.get() == "Defenders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where country = '{cbox_nation.get()}' and (position_p='Center-back' or position_p='Left-back' or position_p ='Right-back' or position_p='Left Wing-Back' or position_p='Right Wing-Back' or position_p='defender');"

        elif cbox_position.get() == "Midfielders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where country = '{cbox_nation.get()}' and (position_p='Central Midfielder' or position_p='Attacking Midfielder' or position_p ='Defensive Midfielder' or position_p='Right Midfielder' or position_p='Left Midfielder' or position_p='midfielder');" 
        
        elif cbox_position.get() == "Forwards":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where country = '{cbox_nation.get()}' and (position_p='Right Winger' or position_p='Striker' or position_p ='Left Winger' or position_p='forward');" 

        insert_listbox(sql_l)

    # (3) League O, Club X, Position O, Nation X
    elif cbox_league.get() != "Select League" and cbox_club.get() == "Select Club" and cbox_position.get() != "Select Position" and cbox_nation.get() == "Select Nation":
        if cbox_position.get() == "Keepers":
            sql_l = f"select league,club,position_p,country,number,name from gk_player where league = '{cbox_league.get()}';" 
           
        elif cbox_position.get() == "Defenders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where league = '{cbox_league.get()}' and (position_p='Center-back' or position_p='Left-back' or position_p ='Right-back' or position_p='Left Wing-Back' or position_p='Right Wing-Back' or position_p='defender');" 

        elif cbox_position.get() == "Midfielders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where league = '{cbox_league.get()}' and (position_p='Central Midfielder' or position_p='Attacking Midfielder' or position_p ='Defensive Midfielder' or position_p='Right Midfielder' or position_p='Left Midfielder' or position_p='midfielder');" 
        
        elif cbox_position.get() == "Forwards":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where league = '{cbox_league.get()}' and (position_p='Right Winger' or position_p='Striker' or position_p ='Left Winger' or position_p='forward');" 

        insert_listbox(sql_l)

    # (4) League O, Club X, Position X, Nation O  
    elif cbox_league.get() != "Select League" and cbox_club.get() == "Select Club" and cbox_position.get() == "Select Position" and cbox_nation.get() != "Select Nation":

        sql_l = f'select league,club,position_p,country,number,name from gk_player where league = "{cbox_league.get()}" and country = "{cbox_nation.get()}" ;'
        insert_listbox(sql_l)

        sql_l = f'select league,club,position_p,country,number,name from none_gk_player where league= "{cbox_league.get()}" and country = "{cbox_nation.get()}" ;' 
        insert_listbox(sql_l)

    # (5) League O, Club X, Position O, Nation O   
    elif cbox_league.get() != "Select League" and  cbox_club.get() == "Select Club" and cbox_nation.get() != "Select Nation" and cbox_position.get() != "Select Position":
        
        if cbox_position.get() == "Keepers":
            sql_l = f"select league,club,position_p,country,number,name from gk_player where league = '{cbox_league.get()}' and country = '{cbox_nation.get()}';" 
           
        elif cbox_position.get() == "Defenders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where league = '{cbox_league.get()}' and country = '{cbox_nation.get()}' and (position_p='Center-back' or position_p='Left-back' or position_p ='Right-back' or position_p='Left Wing-Back' or position_p='Right Wing-Back' or position_p='defender');" 

        elif cbox_position.get() == "Midfielders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where league = '{cbox_league.get()}' and country = '{cbox_nation.get()}' and (position_p='Central Midfielder' or position_p='Attacking Midfielder' or position_p ='Defensive Midfielder' or position_p='Right Midfielder' or position_p='Left Midfielder' or position_p='midfielder');"
        
        elif cbox_position.get() == "Forwards":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where league = '{cbox_league.get()}' and country = '{cbox_nation.get()}' and (position_p='Right Winger' or position_p='Striker' or position_p ='Left Winger' or position_p='forward');" 

        insert_listbox(sql_l)

    # (6) League O, Club O, Position X, Nation X    
    elif cbox_club.get() != "Select Club" and cbox_nation.get()=="Select Nation" and cbox_position.get()=="Select Position" and cbox_nation.get()=="Select Nation":
        sql_l = f'select league,club,position_p,country,number,name from gk_player where club = "{cbox_club.get()}";' 
        insert_listbox(sql_l)
        
        sql_l = f'select league,club,position_p,country,number,name from none_gk_player where club = "{cbox_club.get()}";' 
        insert_listbox(sql_l)
         
    # (7) League O, Club O, Position O, Nation X
    elif cbox_club.get() != "Select Club" and cbox_position.get() != "Select Position" and cbox_nation.get() == "Select Nation":          
        if cbox_position.get() == "Keepers":
            sql_l = f"select league,club,position_p,country,number,name from gk_player where club = '{cbox_club.get()}';" 
           
        elif cbox_position.get() == "Defenders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where club = '{cbox_club.get()}' and (position_p='Center-back' or position_p='Left-back' or position_p ='Right-back' or position_p='Left Wing-Back' or position_p='Right Wing-Back' or position_p='defender');"

        elif cbox_position.get() == "Midfielders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where club = '{cbox_club.get()}' and (position_p='Central Midfielder' or position_p='Attacking Midfielder' or position_p ='Defensive Midfielder' or position_p='Right Midfielder' or position_p='Left Midfielder' or position_p='midfielder');" 
        
        elif cbox_position.get() == "Forwards":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where club = '{cbox_club.get()}' and (position_p='Right Winger' or position_p='Striker' or position_p ='Left Winger' or position_p='forward');" 

        insert_listbox(sql_l)

    # (8) League O, Club O, Position X, Nation O 
    elif cbox_club.get() != "Select Club" and cbox_position.get() == "Select Position" and cbox_nation.get() != "Select Nation":      
        sql_l = f'select league,club,position_p,country,number,name from gk_player where club = "{cbox_club.get()}" and country = "{cbox_nation.get()}";' 
        insert_listbox(sql_l)

        sql_l = f'select league,club,position_p,country,number,name from none_gk_player where club = "{cbox_club.get()}" and country = "{cbox_nation.get()}";' 
        insert_listbox(sql_l)

    # (9) League O, Club O, Position O, Nation O
    elif cbox_club.get() != "Select Club" and cbox_position.get() != "Select Position" and cbox_nation.get() != "Select Nation":
        if cbox_position.get() == "Keepers":
            sql_l = f"select league,club,position_p,country,number,name from gk_player where club = '{cbox_club.get()}' and country ='{cbox_nation.get()}';" 
           
        elif cbox_position.get() == "Defenders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where club = '{cbox_club.get()}' and country = '{cbox_nation.get()}' and (position_p='Center-back' or position_p='Left-back' or position_p ='Right-back' or position_p='Left Wing-Back' or position_p='Right Wing-Back' or position_p='defender');"

        elif cbox_position.get() == "Midfielders":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where club = '{cbox_club.get()}' and country = '{cbox_nation.get()}' and (position_p='Central Midfielder' or position_p='Attacking Midfielder' or position_p ='Defensive Midfielder' or position_p='Right Midfielder' or position_p='Left Midfielder' or position_p='midfielder');" 
        
        elif cbox_position.get() == "Forwards":
            sql_l = f"select league,club,position_p,country,number,name from none_gk_player where club = '{cbox_club.get()}' and country = '{cbox_nation.get()}' and (position_p='Right Winger' or position_p='Striker' or position_p ='Left Winger' or position_p='forward');" 

        insert_listbox(sql_l)
    
    win_search.update()   

    if lbox_list.size() == 0:
        no_msg()    
        
btn_select = Button(frame_select,width=20)
btn_select.config(text="Select",command=select)
btn_select.place(x=280,y=500)

btn_select.bind("<Return>",select)   
win_search.bind("<Return>",select)

lab_list = Label(frame_list)
list_name = " {:<15}     {:<25}   {:<10} {:<20}    {:<10}   {:<25}".format('League','Club','Position','Country','Number','Name')
lab_list.config(text=list_name,justify=LEFT,width=120)
lab_list.place(x=0,y=0)

lbox_list = Listbox(frame_list)
lbox_list.config(width=120,height=25,font="courier 12")
lbox_list.place(x=0,y=30)

scroll_list = Scrollbar(frame_list,command=lbox_list.yview,orient=VERTICAL)
lbox_list.config(yscrollcommand=scroll_list.set)
scroll_list.place(in_=lbox_list,relx=1.0,relheight=1.0,bordermode='outside')

def euro_to_won(value):
    v_won=float(value)*1511.22
    if v_won > 100000000:
        v_won=round(v_won/100000000,1)
        v_won=str(v_won)+'억'    
    elif v_won < 100000000:
        v_won=round(v_won/10000,1)
        v_won=str(v_won)+'만'     
    return v_won

def alter_unit(value):
    if int(value) > 1000000:
        return '€ '+ str(float(value)/1000000)+' M'
    elif int(value) <= 1000000:
        return '€ '+ str(float(value)/1000)+' K' 

win_d_cnt = 0   # detail 창이 열려 있을 때는 다른 detail 창이 열리지 않는다

def detail():
    global win_d_cnt
    if win_d_cnt == 0:
        if lbox_list.size() != 0:
            win_detail=Toplevel()
            win_detail.title("Player Detail")
            win_detail.geometry("350x400+450+250")
            win_detail.option_add("*Font","Arial 11")
            win_detail.resizable(False,False)

            win_d_cnt = 1
            
            frame_player = Frame(win_detail,width=350,height=100)
            frame_player["relief"]="solid"
            frame_player.place(x=0,y=0)

            frame_detail = Frame(win_detail,width=350,height=300)
            frame_detail.place(x=0,y=100)

            cur,conn = None,None
            conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
            cur = conn.cursor()

            idx_player = lbox_list.curselection()
            cur_player = lbox_list.get(idx_player)    # 선택된 선수
            cur_player = cur_player.split("∙")
            cur_club = cur_player[2]  ; cur_name = cur_player[10]

            sql_cur_1 = f'select * from gk_player where club="{cur_club}" and name="{cur_name}";'        ; cur.execute(sql_cur_1)
            result_cur_1 = cur.fetchone()
            sql_cur_2 = f'select * from none_gk_player where club="{cur_club}" and name="{cur_name}";'   ; cur.execute(sql_cur_2)
            result_cur_2 = cur.fetchone()

            if result_cur_1 == None:        # Gk가 아니면
                league = result_cur_2[1]; club = result_cur_2[2]; name = result_cur_2[3]; number = result_cur_2[4]; height = int(result_cur_2[5]); country = result_cur_2[6] ; position = result_cur_2[7]
                age = int(result_cur_2[8]); p_foot = result_cur_2[9]; p_value = result_cur_2[10]; matches = int(result_cur_2[11]); minutes = result_cur_2[12]; goals = result_cur_2[13]
                assists = result_cur_2[14]; started = result_cur_2[15]; rating = result_cur_2[16] ; url_p = result_cur_2[17]
                
                lab_match_d = Label(frame_detail)   ; lab_match_d.config(text=f" Matches          :  {matches}")      ; lab_match_d.place(x=0,y=200)
                lab_started_d = Label(frame_detail) ; lab_started_d.config(text=f"Started   :  {started}")            ; lab_started_d.place(x=200,y=200)
                lab_goal_d = Label(frame_detail)    ; lab_goal_d.config(text=f" Goals              :  {goals}")       ; lab_goal_d.place(x=0,y=225)
                lab_assist_d = Label(frame_detail)  ; lab_assist_d.config(text=f"Assists   :  {assists}")             ; lab_assist_d.place(x=200,y=225)

                
            elif result_cur_2 == None:      # Gk이면
                league = result_cur_1[1]; club = result_cur_1[2]; name = result_cur_1[3]; number = result_cur_1[4]; height = result_cur_1[5]; country = result_cur_1[6]; position=result_cur_1[7]
                age = result_cur_1[8]; p_foot = result_cur_1[9]; p_value = result_cur_1[10]; c_sheets = result_cur_1[11]; saved_penal = result_cur_1[12]; g_conceded = result_cur_1[13]
                matches = result_cur_1[14] ; minutes = result_cur_1[15] ; rating = result_cur_1[16]; url_p = result_cur_1[17]

                lab_match_d = Label(frame_detail)    ; lab_match_d.config(text=f" Matches               :  {matches}")  ; lab_match_d.place(x=0,y=200)
                lab_c_sheets_d = Label(frame_detail) ; lab_c_sheets_d.config(text=f"Clean Sheets     :  {c_sheets}")    ; lab_c_sheets_d.place(x=200,y=200)
                
                lab_conceded_d = Label(frame_detail) ; lab_conceded_d.config(text=f" Goal Conceded   :  {g_conceded}")  ; lab_conceded_d.place(x=0,y=225)
                lab_saved_d = Label(frame_detail)    ; lab_saved_d.config(text=f"Saved Penalties :  {saved_penal}")     ; lab_saved_d.place(x=200,y=225)
                
            birth = 2025-1-age
            
            url = f"https://images.fotmob.com/image_resources/playerimages/{url_p}.png"
            global photo
            photo=None
            with urlopen(url) as response:
                image_data=response.read()
            image = PILImage.open(io.BytesIO(image_data))
            resized_image = image.resize((90,90),PILImage.LANCZOS)
            photo = ImageTk.PhotoImage(resized_image)

            lab_name_d = Label(frame_player) ; lab_name_d.config(text=f" >> {name}",font="Arial 15",justify="center")        ; lab_name_d.place(x=0,y=10)
            lab_league_d = Label(frame_player) ; lab_league_d.config(text=f" {league}",font="Arial 13")                      ; lab_league_d.place(x=0,y=40)
            lab_club_d = Label(frame_player) ; lab_club_d.config(text=f" {club}", font= "Arial 13")                          ; lab_club_d.place(x=0,y=65)
            lab_image_d = Label(frame_player)  ; lab_image_d.config(image=photo) ;  lab_image_d.place(x=250,y=5)

            lab_number_d = Label(frame_detail)   ; lab_number_d.config(text=f" Number          :  {number}")                 ; lab_number_d.place(x=0,y=0)
            lab_position_d = Label(frame_detail) ; lab_position_d.config(text=f" Position          :  {position}")           ; lab_position_d.place(x=0,y=25)
            lab_height_d = Label(frame_detail)   ; lab_height_d.config(text=f" Height             :  {height} cm")           ; lab_height_d.place(x=0,y=50)
            lab_age_d = Label(frame_detail)      ; lab_age_d.config(text=f" Age                 :  {age} years  ({birth})")  ; lab_age_d.place(x=0,y=75)
            lab_country_d = Label(frame_detail)  ; lab_country_d.config(text=f" Country           :  {country}")             ; lab_country_d.place(x=0,y=100)
            lab_prefered_d = Label(frame_detail) ; lab_prefered_d.config(text=f" Prefered foot   :  {p_foot}")               ; lab_prefered_d.place(x=0,y=125)
            lab_value_d = Label(frame_detail)    ; lab_value_d.config(text=f" Market Value   :   {alter_unit(p_value)}  ({euro_to_won(p_value)})")  ; lab_value_d.place(x=0,y=150)
            lab_minute_d = Label(frame_detail)   ; lab_minute_d.config(text=f" Minutes           :  {minutes} min")          ; lab_minute_d.place(x=0,y=175)
            lab_rating_d = Label(frame_detail)   ; lab_rating_d.config(text=f"Rating    :  {rating}")                        ; lab_rating_d.place(x=200,y=175)

            conn.close()
            
            def on_close():
                global win_d_cnt
                win_d_cnt = 0
                win_detail.destroy()
            
            win_detail.protocol("WM_DELETE_WINDOW",on_close)

def compare_num(c1,c2):
    global l_color
    if c1 == None:
        return "↑"
    elif c2 == None:
        return "↓"
    elif c1 < c2:
        l_color="red"
        return "↑"
    elif c1 > c2:
        l_color="blue"
        return "↓"
    elif c1 == c2:
        return "-"
    
def reverse_num(c2):
    if c2 == "↑":
        return "↓"
    elif c2 == "↓":
        return "↑"
    elif c2 == "-":
        return "-"

def compare_color(arrow):
    if arrow == "↑":
        return "red"
    elif arrow == "↓":
        return "blue"

win_c_cnt=0

def compare():
    global win_c_cnt
    if win_c_cnt == 0:
        if lbox_list.size() != 0:
            win_compare = Toplevel()
            win_compare.title("Players Compare")
            win_compare.geometry("750x600+450+250")
            win_compare.resizable(False,False)
            win_compare.option_add("*Font","Arial 15")

            win_c_cnt = 1

            frame_player = Frame(win_compare,width=750,height=100)
            frame_player["relief"] = "solid"
            frame_player.place(x=0,y=0)

            frame_detail = Frame(win_compare,width=750,height=450)
            frame_detail.place(x=0,y=100)

            frame_btn = Frame(win_compare,width=750,height=50)
            frame_btn["relief"] = "solid"
            frame_btn.place(x=0,y=550)

            lab_height = Label(frame_detail); lab_height.config(text="Height",width=15,anchor="center")            ; lab_height.place(x=280,y=30)
            lab_age = Label(frame_detail); lab_age.config(text="Age",width=15,anchor="center")                     ; lab_age.place(x=280,y=60)
            lab_country = Label(frame_detail); lab_country.config(text="Country",width=15,anchor="center")         ; lab_country.place(x=280,y=90)
            lab_prefered = Label(frame_detail); lab_prefered.config(text="Prefered foot",width=15,anchor="center") ; lab_prefered.place(x=280,y=120)
            lab_value = Label(frame_detail); lab_value.config(text="Market values",width=15,anchor="center")       ; lab_value.place(x=280,y=150)
            lab_minute = Label(frame_detail); lab_minute.config(text="Minutes",width=15,anchor="center")           ; lab_minute.place(x=280,y=180)
            lab_match = Label(frame_detail); lab_match.config(text="Matches",width=15,anchor="center")             ; lab_match.place(x=280,y=210)
            lab_rating = Label(frame_detail) ; lab_rating.config(text="Rating",width=15,anchor="center")           ; lab_rating.place(x=280,y=330)

            cur,conn = None,None
            conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
            cur = conn.cursor()
            
            idx_player = lbox_list.curselection()
            cur_player = lbox_list.get(idx_player)    # 선택된 선수
            cur_player = cur_player.split("∙")
            cur_club = cur_player[2]  ; cur_name=cur_player[10] ; cur_posit=cur_player[4]
            global height_c1,age_c1,p_value_c1,matches_c1,minutes_c1,rating_c1,c_sheets_c1,saved_p_c1,g_conceded_c1,goals_c1,assists_c1,started_c1
        
            if cur_posit == "GK":
                lab_c_sheets = Label(frame_detail) ; lab_c_sheets.config(text="Clean sheets",width=15,anchor="center")      ; lab_c_sheets.place(x=280,y=240)
                lab_saved = Label(frame_detail)    ; lab_saved.config(text="Saved penalties",width=15,anchor="center")      ; lab_saved.place(x=280,y=270)
                lab_conceded = Label(frame_detail) ; lab_conceded.config(text="Goals conceded",width=15,anchor="center")    ; lab_conceded.place(x=280,y=300)

                sql_cur = f'select * from gk_player where club="{cur_club}" and name="{cur_name}";'     ; cur.execute(sql_cur)
                result_cur = cur.fetchone()   
                c_sheets_c1 = result_cur[11] ; saved_p_c1 = result_cur[12] ; g_conceded_c1 = result_cur[13] ; matches_c1 = result_cur[14] ; minutes_c1 = result_cur[15]

                lab_c_sheets_c = Label(frame_detail)     ; lab_c_sheets_c.config(text=f" {c_sheets_c1}",width=20,anchor="center")       ; lab_c_sheets_c.place(x=0,y=240)
                lab_saved_c = Label(frame_detail)        ; lab_saved_c.config(text=f" {saved_p_c1}",width=20,anchor="center")           ; lab_saved_c.place(x=0,y=270)
                lab_conceded_c = Label(frame_detail)     ; lab_conceded_c.config(text=f" {g_conceded_c1}",width=20,anchor="center")     ; lab_conceded_c.place(x=0,y=300)

            else:
                lab_started = Label(frame_detail)  ; lab_started.config(text="Started")   ; lab_started.place(x=330,y=240)
                lab_goal = Label(frame_detail)     ; lab_goal.config(text="Goals")        ; lab_goal.place(x=330,y=270)
                lab_assist = Label(frame_detail)   ; lab_assist.config(text="Assists")    ; lab_assist.place(x=330,y=300)

                sql_cur = f'select * from none_gk_player where club="{cur_club}" and name="{cur_name}";'   ; cur.execute(sql_cur)           
                result_cur = cur.fetchone()
                goals_c1 = result_cur[13] ; assists_c1=result_cur[14] ; started_c1=result_cur[15] ; matches_c1=result_cur[11] ; minutes_c1=result_cur[12]

                lab_started_c = Label(frame_detail)    ; lab_started_c.config(text=f" {started_c1}",width=20,anchor="center") ; lab_started_c.place(x=0,y=240)
                lab_goal_c = Label(frame_detail)       ; lab_goal_c.config(text=f" {goals_c1}",width=20,anchor="center")      ; lab_goal_c.place(x=0,y=270)
                lab_assist_c = Label(frame_detail)     ; lab_assist_c.config(text=f" {assists_c1}",width=20,anchor="center")  ; lab_assist_c.place(x=0,y=300)

            league = result_cur[1]; club = result_cur[2]; name = result_cur[3]; number = result_cur[4]; height_c1 = result_cur[5]; country = result_cur[6]; position = result_cur[7]
            age_c1 = result_cur[8]; p_foot = result_cur[9]; p_value_c1 = result_cur[10]; rating_c1 = result_cur[16]

            lab1 = Label(frame_player) ; lab1.config(text=f">> {name}",font="Arial 15") ; lab1.place(x=0,y=10)
            lab2 = Label(frame_player) ; lab2.config(text=f" {league}",font="Arial 13") ; lab2.place(x=0,y=40)
            lab3 = Label(frame_player) ; lab3.config(text=f" {club}", font= "Arial 13") ; lab3.place(x=0,y=65)
        
            lab_num_posit_c =Label(frame_detail)  ; lab_num_posit_c.config(text=f" {number}  {position}",width=21,anchor="center")  ; lab_num_posit_c.place(x=0,y=0)
            lab_height_c = Label(frame_detail)    ; lab_height_c.config(text=f" {height_c1}",width=20,anchor="center")              ; lab_height_c.place(x=0,y=30)
            lab_age_c = Label(frame_detail)       ; lab_age_c.config(text=f" {age_c1}",width=20,anchor="center")                    ; lab_age_c.place(x=0,y=60)
            lab_country_c = Label(frame_detail)   ; lab_country_c.config(text=f" {country}",width=20,anchor="center")               ; lab_country_c.place(x=0,y=90)
            lab_prefered_c = Label(frame_detail)  ; lab_prefered_c.config(text=f" {p_foot}",width=20,anchor="center")               ; lab_prefered_c.place(x=0,y=120)
            lab_value_c = Label(frame_detail)     ; lab_value_c.config(text=f" {alter_unit(p_value_c1)}",width=20,anchor="center")  ; lab_value_c.place(x=0,y=150)
            lab_minute_c = Label(frame_detail)    ; lab_minute_c.config(text=f" {minutes_c1}",width=20,anchor="center")             ; lab_minute_c.place(x=0,y=180)
            lab_match_c = Label(frame_detail)     ; lab_match_c.config(text=f" {matches_c1}",width=20,anchor="center")              ; lab_match_c.place(x=0,y=210)
            lab_rating_c = Label(frame_detail)    ; lab_rating_c.config(text=f" {rating_c1}",width=20,anchor="center")              ; lab_rating_c.place(x=0,y=330)

            conn.close()

            def add():
                cur,conn = None,None
                conn = pymysql.connect(host='127.0.0.1',user='root',password='0000',db='player',charset='utf8')
                cur = conn.cursor()

                idx_player_2 = lbox_list.curselection()
                cur_player_2 = lbox_list.get(idx_player_2)    # 선택된 선수
                cur_player_2 = cur_player_2.split("∙")
                cur_club_2 = cur_player_2[2]  ; cur_name_2=cur_player_2[10] ; cur_posit_a=cur_player_2[4]

                if (cur_posit == "GK" and cur_posit_a == "GK") or (cur_posit != "GK" and cur_posit_a != "GK"):    # GK는 GK끼리만 비교
                    if cur_name != cur_name_2:  # 비교 대상과 다른 선수만 비교
                        global lab_name_a,lab_league_a,lab_club_a,lab_num_posit_a,lab_height_a,lab_age_a,lab_country_a,lab_prefered_a,lab_value_a,lab_minute_a,lab_match_a,lab_rating_a,lab_c_sheets_a,lab_conceded_a,lab_saved_a,lab_goal_a,lab_assist_a,lab_started_a
                        if cur_posit_a =="GK":    # Gk만
                            sql_cur_2 = f'select * from gk_player where club="{cur_club_2}" and name="{cur_name_2}";'   ; cur.execute(sql_cur_2)
                            result_cur_2 = cur.fetchone()
                            c_sheets_c2 = result_cur_2[11] ; saved_p_c2 = result_cur_2[12] ; g_conceded_c2 = result_cur_2[13] ; matches_c2 = result_cur_2[14]; minutes_c2 = result_cur_2[15]

                            lab_c_sheets_a = Label(frame_detail)     ; lab_c_sheets_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(c_sheets_c1,c_sheets_c2),"",c_sheets_c2),width=27,anchor="center",foreground=compare_color(compare_num(c_sheets_c1,c_sheets_c2)))            ; lab_c_sheets_a.place(x=440,y=240)
                            lab_saved_a = Label(frame_detail)        ; lab_saved_a.config(text=f" {saved_p_c2}",width=27,anchor="center")  ; lab_saved_a.place(x=460,y=270)
                            lab_conceded_a = Label(frame_detail)     ; lab_conceded_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(g_conceded_c1,g_conceded_c2),"",g_conceded_c2),width=27,anchor="center",foreground=compare_color(compare_num(g_conceded_c1,g_conceded_c2)))  ; lab_conceded_a.place(x=440,y=300)
                
                        else:                   # None_GK
                            sql_cur_2 = f'select * from none_gk_player where club="{cur_club_2}" and name="{cur_name_2}";'   ; cur.execute(sql_cur_2)
                            result_cur_2 = cur.fetchone()

                            goals_c2 = result_cur_2[13] ; assists_c2 = result_cur_2[14] ; started_c2 = result_cur_2[15] ; matches_c2 = result_cur_2[11]; minutes_c2 = result_cur_2[12]

                            lab_started_a = Label(frame_detail)    ; lab_started_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(started_c1,started_c2),"",started_c2),width=27,anchor="center",foreground=compare_color(compare_num(started_c1,started_c2))) ; lab_started_a.place(x=440,y=240)
                            lab_goal_a = Label(frame_detail)       ; lab_goal_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(goals_c1,goals_c2),"",goals_c2),width=27,anchor="center",foreground=compare_color(compare_num(goals_c1,goals_c2)))              ; lab_goal_a.place(x=440,y=270)
                            lab_assist_a = Label(frame_detail)     ; lab_assist_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(assists_c1,assists_c2),"",assists_c2),width=27,anchor="center",foreground=compare_color(compare_num(assists_c1,assists_c2)))  ; lab_assist_a.place(x=440,y=300)
                        # All  
                        league = result_cur_2[1]; club = result_cur_2[2]; name=result_cur_2[3]; number = result_cur_2[4]; height_c2 = result_cur_2[5] ; country = result_cur_2[6]; position = result_cur_2[7]
                        age_c2 = result_cur_2[8]; p_foot = result_cur_2[9]; p_value_c2 = result_cur_2[10] ; rating_c2 = result_cur_2[16]
                        
                        lab_name_a = Label(frame_player)   ; lab_name_a.config(text=f"{name} <<",font="Arial 15",width=27,anchor="e")    ; lab_name_a.place(x=450,y=10)
                        lab_league_a = Label(frame_player) ; lab_league_a.config(text=f"{league}  ",font="Arial 13",width=33,anchor="e") ; lab_league_a.place(x=450,y=40)
                        lab_club_a = Label(frame_player)   ; lab_club_a.config(text=f"{club}  ", font= "Arial 13",width=33,anchor="e")   ; lab_club_a.place(x=450,y=65)
                                                                        
                        lab_num_posit_a = Label(frame_detail) ; lab_num_posit_a.config(text=f"{number}  {position}",width=30,anchor="center") ;lab_num_posit_a.place(x=450,y=0)
                        lab_height_a = Label(frame_detail)    ; lab_height_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(height_c1,height_c2),"",height_c2),width=27,anchor="center",foreground=compare_color(compare_num(height_c1,height_c2)))                   ; lab_height_a.place(x=440,y=30)
                        lab_age_a = Label(frame_detail)       ; lab_age_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(age_c1,age_c2),"",age_c2),width=27,anchor="center",foreground=compare_color(compare_num(age_c1,age_c2)))                                     ; lab_age_a.place(x=440,y=60)
                        lab_country_a = Label(frame_detail)   ; lab_country_a.config(text=f" {country}",width=27,anchor="center")               ; lab_country_a.place(x=450,y=90)
                        lab_prefered_a = Label(frame_detail)  ; lab_prefered_a.config(text=f" {p_foot}",width=27,anchor="center")               ; lab_prefered_a.place(x=450,y=120)
                        lab_value_a = Label(frame_detail)     ; lab_value_a.config(text="{:^2}{:<1}{:<3}".format(compare_num(p_value_c1,p_value_c2),"",alter_unit(p_value_c2)),width=27,anchor="center",foreground=compare_color(compare_num(p_value_c1,p_value_c2)))   ;  lab_value_a.place(x=440,y=150)
                        lab_minute_a = Label(frame_detail)    ; lab_minute_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(minutes_c1,minutes_c2),"",minutes_c2),width=27,anchor="center",foreground=compare_color(compare_num(minutes_c1,minutes_c2)))              ; lab_minute_a.place(x=440,y=180)
                        lab_match_a = Label(frame_detail)     ; lab_match_a.config(text="{:^2}{:<5}{:<3}".format(compare_num(matches_c1,matches_c2),"",matches_c2),width=27,anchor="center",foreground=compare_color(compare_num(matches_c1,matches_c2)))               ; lab_match_a.place(x=440,y=210)
                        lab_rating_a = Label(frame_detail)    ; lab_rating_a.config(text="{:^2}{:<4}{:<3}".format(compare_num(rating_c1,rating_c2),"",rating_c2),width=27,anchor="center",foreground=compare_color(compare_num(rating_c1,rating_c2)))                   ; lab_rating_a.place(x=440,y=330)

                        win_compare.update()
                        conn.close()        
                    
                    else:
                        no_msg()   

                else:
                    no_msg()
                
            def delete():
                lab_name_a.destroy() ; lab_league_a.destroy() ; lab_club_a.destroy() ; lab_num_posit_a.destroy(); lab_height_a.destroy() ; lab_age_a.destroy() ; lab_country_a.destroy()
                lab_prefered_a.destroy() ; lab_value_a.destroy() ; lab_minute_a.destroy() ; lab_match_a.destroy() ; lab_rating_a.destroy() 
                if position == "Keeper":
                    lab_c_sheets_a.destroy() ; lab_conceded_a.destroy() ; lab_saved_a.destroy() 
                else:
                    lab_goal_a.destroy() ; lab_assist_a.destroy() ; lab_started_a.destroy()

            btn_add = Button(frame_btn)
            btn_add.config(text="Add",command=add)
            btn_add.place(x=650,y=10)

            btn_delete = Button(frame_btn)
            btn_delete.config(text="Delete",command=delete)
            btn_delete.place(x=550,y=10)

            def on_close():
                global win_c_cnt
                win_c_cnt = 0
                win_compare.destroy()
            
            win_compare.protocol("WM_DELETE_WINDOW",on_close)

btn_detail = Button(frame_list)
btn_detail.config(text="Detail",command=detail)
btn_detail.place(x=920,y=520)

btn_compare = Button(frame_list)
btn_compare.config(text='Compare',command=compare)
btn_compare.place(x=1040,y=520)

win_search.mainloop()