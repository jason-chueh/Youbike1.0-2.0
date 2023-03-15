import tkinter as tk
from tkinter import *
from tkinter import ttk
import tkinter.font as tkFont
from PIL import ImageTk, Image


page = Tk()
page.geometry("800x449+367+205")

start = str()
end = str()
class MainPage(tk.Frame):
    def __init__(self):
        tk.Frame.__init__(self)
        self.grid()
        self.Cover_Pic = ImageTk.PhotoImage(file="椰林3.png")
        self.menu_image = tk.Label(self, image=self.Cover_Pic, compound=tk.CENTER)
        self.menu_image.grid(row=0, column=0, columnspan=10, rowspan=10)
        self.createWidgets()
    def createWidgets(self):
        f2 = tkFont.Font(size=28, family='Microsoft JhengHei')
        self.btnNum1 = tk.Button(self, text="開始旅途",command=self.start, height=1, width=12, font=f2)
        self.btnNum1.place(x=260, y=100)
        self.btnNum2 = tk.Button(self, text="離開", command=self.quit,height=1, width=12, font=f2)
        self.btnNum2.place(x=260, y=330)
    def quit(self):
        self.master.destroy()

    def start(self):
        r = Toplevel()  
        r.title("輸入路徑")
        canvas = Canvas(r, height=449, width=800)
        canvas.pack()
        my_image = PhotoImage(file='椰林3.png', master=page)
        canvas.create_image(0, 0, anchor=NW, image=my_image)
        
        f = tkFont.Font(size=20,family='Microsoft JhengHei')
        
        labelstart = tk.Label(r,text = "輸入所在地",font=f)
        labelstart.pack()
        labelstart.place(x=179 ,y=130,height=50)
        labelpurpose = tk.Label(r,text = "輸入目的地",font=f)
        labelpurpose.pack()
        labelpurpose.place(x=179 ,y=350,height=50)
        
        startString = tk.StringVar()
        purposeString = tk.StringVar()
        entry_start = tk.Entry(r,textvariable=startString,font=f)
        entry_start.pack()
        entry_start.place(x=321,y=130,width=300,height=50)
        entry_purpose = tk.Entry(r,textvariable=purposeString,font=f)
        entry_purpose.pack()
        entry_purpose.place(x=321,y=350,width=300,height=50)
        
        btn = tk.Button(r,text='GO',height=1,width=6,font=f,command=self.quit)
        btn.place(x=700,y=390)
        
        ws = r.winfo_screenwidth()
        hs = r.winfo_screenheight()
        x = (ws / 2) - (800 / 2)
        y = (hs / 2) - (449 / 2)
        r.geometry('%dx%d+%d+%d' % (800, 449, x, y))
        r.mainloop()
        start_place = startString.get()
        purpose_place = purposeString.get()
        global start
        global end
        start = start_place
        end = purpose_place

        
page = MainPage()
page.master.title("歡迎光臨")
page.mainloop()

'''
Youbike1.0 Web Crawler
'''
# 除錯
import requests.packages.urllib3
requests.packages.urllib3.disable_warnings()

# 載入package
import requests
from bs4 import BeautifulSoup
from time import sleep
import pandas as pd
import googlemaps
from datetime import datetime
import re

# Web API Crawler
district_1 = []    # 區域
name_1 = []        # 租賃站點
available_1 = []   # 可借車輛數
empty_1 = []       # 剩餘車位數
lat_lst1 = []      # 緯度
lng_lst1 = []      # 經度

url = 'https://apis.youbike.com.tw/api/front/station/all?lang=tw&type=1'
doc = requests.get(url, verify = False)
data_lst1 = doc.json()   # 擷取到一個 list 裡面包含了所有測站的資料，每個測站都自成一個 dict

for lst in data_lst1['retVal']:
    if (lst['district_tw'] == '大安區') or (lst['district_tw'] == '中正區'):
        district_1.append(lst['district_tw'])
        name_1.append(lst['name_tw'])
        available_1.append(lst['available_spaces'])
        empty_1.append(lst['empty_spaces'])
        lat_lst1.append(lst['lat'])
        lng_lst1.append(lst['lng'])
    else:
        pass

# youbike1.0經緯度資訊
loc_lst1 = []   # 經緯度位置資訊
for i in range(len(lat_lst1)):
    lat = lat_lst1[i]
    lng = lng_lst1[i]
    loc = lat + ',' + lng
    name = name_1[i]
    loc_lst1.append([loc, name])    

# youbike1.0站點資訊    
record_lst1 = []
for i in range(len(name_1)):
    record_lst1.append([district_1[i], name_1[i], available_1[i], empty_1[i]])

df1 = pd.DataFrame(record_lst1, columns = ['區域', '租賃站點', '可借車輛數', '剩餘車位數'])
# print_recordlist(df1)





# Web API Crawler
district_2 = []    # 區域
name_2 = []        # 租賃站點
available_2 = []   # 可借車輛數
empty_2 = []       # 剩餘車位數
lat_lst2 = []      # 緯度
lng_lst2 = []      # 經度


url = 'https://apis.youbike.com.tw/api/front/station/all?lang=tw&type=2'
doc = requests.get(url, verify = False)
data_lst2 = doc.json()   # 擷取到一個 list 裡面包含了所有測站的資料，每個測站都自成一個 dict

for lst in data_lst2['retVal']:
    if (lst['district_tw'] == '大安區') or (lst['district_tw'] == '中正區') or (lst['district_tw'] == '臺大專區'):
        district_2.append(lst['district_tw'])
        name_2.append(lst['name_tw'])
        available_2.append(lst['available_spaces'])
        empty_2.append(lst['empty_spaces'])
        lat_lst2.append(lst['lat'])
        lng_lst2.append(lst['lng'])
    else:
        pass

# youbike2.0經緯度資訊
loc_lst2 = []   # 經緯度位置資訊
for i in range(len(lat_lst2)):
    lat = lat_lst2[i]
    lng = lng_lst2[i]
    loc = lat + ',' + lng
    name = name_2[i]
    loc_lst2.append([loc, name])    

record_lst2 = []
for i in range(len(name_2)):
    record_lst2.append([district_2[i], name_2[i], available_2[i], empty_2[i]])

df2 = pd.DataFrame(record_lst2, columns = ['區域', '租賃站點', '可借車輛數', '剩餘車位數'])
# print_recordlist(df2)



# 輸入目標起始點與終點

# 獲得金鑰
gmaps = googlemaps.Client(key = 'AIzaSyArxx6RNh9gS-MNL8xrrEw2RtThp1fRtpA')

class Youbike_Crawler:
    def __init__(self, point):
        self.loc_point = point
    
    # 路徑規劃：輸出兩點距離
    def route_plan(self, origin, destination, mode):   
        now = datetime.now()
        direction = gmaps.directions(origin = origin, destination = destination, mode = mode, alternatives = True, avoid = None,
                   language = 'zh-TW', departure_time = now, arrival_time = None, optimize_waypoints = True, transit_mode = None,
                   transit_routing_preference = None, traffic_model = None)
        distance = direction[0]['legs'][0]['distance']['text']   # 兩點間總距離
    
        return distance

    def top_choice(self):
        # 比較共享腳踏車站地點與目標地點位置距離遠近(1.0)
        distance_lst1 = []
        for station in loc_lst1:
            loc = station[0]
            name = station[1]
            distance1 = self.route_plan(origin = self.loc_point, destination = loc, mode = 'walking')
            distance_lst1.append([name, distance1, loc])

        # 依距離排序(1.0)
        distance_lst1 = sorted(distance_lst1, key = lambda d : d[1], reverse = False)
        top_stations_1 = []
        for i in range(0,2):
            name = distance_lst1[i][0]
            loc = distance_lst1[i][2]
            top_stations_1.append((name, loc))
    
        # 比較共享腳踏車站地點與目標地點位置距離遠近(2.0)
        distance_lst2 = []
        for station in loc_lst2:
            loc = station[0]
            name = station[1]
            distance2 = self.route_plan(origin = self.loc_point, destination = loc, mode = 'walking')
            distance_lst2.append([name, distance2, loc])

        # 依距離排序(2.0)
        distance_lst2 = sorted(distance_lst2, key = lambda d : d[1], reverse = False)
        top_stations_2 = []
        for i in range(0,3):
            name = distance_lst2[i][0]
            loc = distance_lst2[i][2]
            top_stations_2.append((name, loc))
        
        return top_stations_1, top_stations_2

start_point = Youbike_Crawler(point = start)
start_choice = start_point.top_choice()
end_point = Youbike_Crawler(point = end)
end_choice = end_point.top_choice()
"""
print(start_choice[0]) #  起點1.0站(2) [('基隆長興路口', '25.017054,121.544352'), ('捷運公館站(2號出口)', '25.01476,121.534538')]
print(start_choice[1]) #  起點2.0站(3)
print(end_choice[0])   #  終點1.0站(2)
print(end_choice[1])   #  終點2.0站(3)
"""

def borrowable1(station):
 for i in range (0,len(record_lst1)):
        if  station == record_lst1[i][1] and record_lst1[i][2] > 0:
            return True         
        elif station == record_lst1[i][1] and record_lst1[i][2] == 0:
            return False
        else:
            continue

def returnable1(station):
    for i in range (0,len(record_lst1)):
        if  station == record_lst1[i][1] and record_lst1[i][3] > 0:
            return True         
        elif station == record_lst1[i][1] and record_lst1[i][3] == 0:
            return False
        else:
            continue

def borrowable2(station):
    for i in range (0,len(record_lst2)):
        if  station == record_lst2[i][1] and record_lst2[i][2] > 0:
            return True         
        elif station == record_lst2[i][1] and record_lst2[i][2] == 0:
            return False
        else:
            continue

def returnable2(station):
    for i in range (0,len(record_lst2)):
        if  station == record_lst2[i][1] and record_lst2[i][3] > 0:
            return True         
        elif station == record_lst2[i][1] and record_lst2[i][3] == 0:
            return False
        else:
            continue

# 把start_choice裡面的1.0 list、2.0 list都拿出來檢查站點有沒有剩餘車輛，並把剩餘車輛>= 1的append到start_choice2
# end_choice也一樣，有剩餘停車位的append到end_choice2

start_choice2 = []
end_choice2 = []
ubike1_start_list = []
ubike2_start_list = []
ubike1_end_list = []
ubike2_end_list = []
for i in range(len(start_choice[0])):
    if borrowable1(start_choice[0][i][0]) == True:
        ubike1_start_list.append(start_choice[0][i])
    else:
        pass
for i in range(len(start_choice[1])):
    if borrowable2(start_choice[1][i][0]) == True:
        ubike2_start_list.append(start_choice[1][i])
    else:
        pass
start_choice2.append(ubike1_start_list)
start_choice2.append(ubike2_start_list)
for i in range(len(end_choice[0])):
    if returnable1(end_choice[0][i][0]) == True:
        ubike1_end_list.append(end_choice[0][i])
    else:
        pass
for i in range(len(end_choice[1])):
    if returnable2(end_choice[1][i][0]) == True:
        ubike2_end_list.append(end_choice[1][i])
    else:
        pass
end_choice2.append(ubike1_end_list)
end_choice2.append(ubike2_end_list)


def minutes(time_str):
    time_str.strip(' ')         # 頭尾去空格
    hour = time_str.count('小時')
    if hour == 0:
        time_list = time_str.split(' ')   # split完應該是['num','分鐘']
        time_minutes = int(time_list[0])
    else:
        time_list = time_str.split(' ')   # split完應該會變成['num','小時','num','分鐘']
        time_minutes = 60*int(time_list[0]) + int(time_list[2])
    return time_minutes

def km(distance_string):
    distance_string.strip(' ')         # 頭尾去空格
    kilometer = distance_string.count('公里')
    if kilometer == 0:
        distance_list = distance_string.split(' ')   # split完應該是['num','公尺']
        distance_km = int(distance_list[0]) * 0.001
    else:
        distance_list = distance_string.split(' ')   # split完應該會變成['num','公里']
        distance_km = float(distance_list[0])
    return distance_km


def route_plan2(origin, destination, mode):   
    now = datetime.now()
    direction = gmaps.directions(origin = origin, destination = destination, mode = mode, alternatives = True, avoid = None,
               language = 'zh-TW', departure_time = now, arrival_time = None, optimize_waypoints = True, transit_mode = None,
               transit_routing_preference = None, traffic_model = None)
    distance = direction[0]['legs'][0]['distance']['text']   # 兩點間總距離
    duration = direction[0]['legs'][0]['duration']['text']   # 兩點間預計交通時間
    steps = direction[0]['legs'][0]['steps']
    step_by_step = ''   
    for i in range(len(steps)):
        step = steps[i]['html_instructions']
        step = re.sub(r'\<[^\>]*\>',"",step)
        step_by_step += (step + ' → ')
    step_by_step = step_by_step[:-3]   # 所有路徑指示
    step_by_step = step_by_step.strip()
    
    return distance, duration, step_by_step       # 距離,時間,步驟



def ubike1_to_1(start_choice2, end_choice2):
	suggest_list = []
	for i in range(len(start_choice2[0])):       # start_choice2[0]是所有1.0站點，[0][i]是1.0個別站點list，[0][i][1]是座標
		for j in range(len(end_choice2[0])):
			a = route_plan2(start, start_choice2[0][i][1], 'walking')         # route_plan抓出來的會是[距離,時間,路徑]
			b = route_plan2(start_choice2[0][i][1], end_choice2[0][j][1], 'bicycling')
			c = route_plan2(end_choice2[0][j][1], end, 'walking')
			t1 = minutes(a[1])
			t2 = minutes(b[1])
			t3 = minutes(c[1])
			d1 = km(a[0])
			d2 = km(b[0])
			d3 = km(c[0])
			add_time = t1 + t2 + t3
			add_step_by_step = a[2]+' →'+'Youbike1.0'+str(start_choice2[0][i][0])+' →'+b[2]+' →'+'Youbike1.0'+ str(end_choice2[0][j][0])+' →'+c[2]
			add_distance = round(d1 + d2 + d3, 2)
			suggest_list.append([add_time, add_step_by_step, add_distance, start_choice2[0][i][0], end_choice2[0][j][0], 'Youbike1.0 to 1.0'])
	return suggest_list         # [時間,步驟,距離,]
	

def ubike2_to_2(start_choice2, end_choice2):
	suggest_list = []
	for i in range(len(start_choice2[1])):       # start_choice2[1]是所有2.0站點，[1][i]是2.0個別站點list，[1][i][1]是座標
		for j in range(len(end_choice2[1])):
			a = route_plan2(start, start_choice2[1][i][1], 'walking')         # route_plan抓出來的會是[距離,時間,路徑]
			b = route_plan2(start_choice2[1][i][1], end_choice2[1][j][1], 'bicycling')
			c = route_plan2(end_choice2[1][j][1], end, 'walking')
			t1 = minutes(a[1])
			t2 = minutes(b[1])
			t3 = minutes(c[1])
			d1 = km(a[0])
			d2 = km(b[0])
			d3 = km(c[0])
			add_time = t1 + t2 + t3
			add_step_by_step = a[2]+' →'+'Youbike2.0'+str(start_choice2[1][i][0])+' →'+b[2]+' →'+'Youbike2.0'+ str(end_choice2[1][j][0])+' →'+c[2]
			add_distance = round(d1 + d2 + d3, 2)
			suggest_list.append([add_time, add_step_by_step, add_distance, start_choice2[1][i][0], end_choice2[1][j][0], 'Youbike2.0 to 2.0'])
	return suggest_list         # [時間,步驟,距離,]
	
midway_list = [[["捷運公館站(2號出口)",'25.01476,121.534538'],["捷運公館站(2號出口)", '25.01385,121.53549'],["捷運公館站(1號出口)", '25.015069,121.533828']], 
			   [["辛亥新生路口",'25.022413,121.53456'],["辛亥新生路口東南側", '25.02218,121.53474'],["臺大新體育館東南側", '25.02112,121.53407']],
               [["辛亥路二段(臺大外語學院外)",'25.02101,121.54153'], ["臺大法人語言訓練中心前",'25.02104,121.54081'],["臺大社科院西側" , '25.02053,121.54145']],
               [["台灣科技大學",'25.0131,121.539723'], ["臺灣科技大學側門",'25.01295,121.53973'],["臺大教研館北側", '25.01337,121.53909']],
               [["基隆長興路口",'25.017054,121.544352'],["基隆長興路口東側", '25.01727,121.54471'],["臺大男六舍前", '25.01729,121.54531']],
               [["捷運科技大樓站",'25.025896,121.543293'], ["和平復興路口西北側", '25.02543,121.54332'], ["捷運科技大樓站",'25.02429,121.54328']]]
	

def midway_timeCost (start, end, midway):
    route_1 = route_plan2(start, midway, 'bicycling')
    route_2 = route_plan2(midway, end, 'bicycling')
    time_1, time_2 = minutes(route_1[1]), minutes(route_2[1])
    total_time = time_1 + time_2
    return total_time
# 中繼站List    
def optimal_midway_ubike1_start(start, end):    # 出發者一定是騎1.0，在中繼站還1.0借2.0
    name_time_list = []
    for i in range(6):
        midway_list_def = []
        if returnable1(midway_list[i][0][0]) == True:
            if borrowable2(midway_list[i][1][0]) == True:     # 判斷youbike2.0有沒有車可借，midway_list裡的第一個ubike2.0站點名稱:[i][1][0]
                current_time = midway_timeCost(start, end, midway_list[i][0][1])     # 時間要放到1.0中繼站的經緯度[i][0][1]
                midway_list_def.append(current_time)
                midway_list_def.append(midway_list[i][0])
                midway_list_def.append(midway_list[i][1])
            elif borrowable2(midway_list[i][2][0]) == True:
                current_time = midway_timeCost(start, end, midway_list[i][0][1])     # 時間要放到1.0中繼站的經緯度[i][0][1]
                midway_list_def.append(current_time)
                midway_list_def.append(midway_list[i][0])
                midway_list_def.append(midway_list[i][2])
            else:
                continue
        else:
            continue
        name_time_list.append(midway_list_def)

    return sorted(name_time_list)    # list裡的元素:[時間,[1.0站站名,座標],[2.0站名,座標]]
optimal_midway_list1 = optimal_midway_ubike1_start(start, end)
optimal_midway_list2 = optimal_midway_list1[0]

def optimal_midway_ubike2_start(start, end):       # 出發者一定是騎2.0，在中繼站還2.0借1.0
    name_time_list = []
    for i in range(6):
        midway_list_def = []
        if borrowable1(midway_list[i][0][0]) == True:
            if returnable2(midway_list[i][1][0]) == True:     # 判斷youbike2.0有沒有車可借，midway_list裡的第一個ubike2.0站點名稱:[i][1][0]
                current_time = midway_timeCost(start, end, midway_list[i][0][1])     # 時間要放到1.0中繼站的經緯度[i][0][1]
                midway_list_def.append(current_time)
                midway_list_def.append(midway_list[i][0])
                midway_list_def.append(midway_list[i][1])
            elif returnable2(midway_list[i][2][0]) == True:
                current_time = midway_timeCost(start, end, midway_list[i][0][1])     # 時間要放到1.0中繼站的經緯度[i][0][1]
                midway_list_def.append(current_time)
                midway_list_def.append(midway_list[i][0])
                midway_list_def.append(midway_list[i][2])
            else:
                continue
        else:
            continue
        name_time_list.append(midway_list_def)

    return sorted(name_time_list)    # list裡的元素:[時間,[1.0站站名,座標],[2.0站名,座標]]
optimal_midway_list3 = optimal_midway_ubike2_start(start, end)
optimal_midway_list4 = optimal_midway_list3[0]
	

def midway_situation_1to2(list): #  [time, [name, coordinate], [name, coordinate]]
	if len(start_choice2[0]) > 0:
		suggest_list = []
		a = route_plan2(start, start_choice2[0][0][1], 'walking')         # route_plan抓出來的會是[距離,時間,路徑]
		b = route_plan2(start_choice2[0][0][1], list[1][1], 'bicycling')
		c = route_plan2(list[1][1], end_choice2[1][0][1], 'bicycling')
		d = route_plan2(end_choice2[1][0][1], end, 'walking')
		t1 = minutes(a[1])
		t2 = minutes(b[1])
		t3 = minutes(c[1])
		t4 = minutes(d[1])
		d1 = km(a[0])
		d2 = km(b[0])
		d3 = km(c[0])
		d4 = km(d[0])
		add_time = t1 + t2 + t3 + t4
		add_step_by_step = a[2]+' →'+'Youbike1.0'+str(start_choice2[0][0][0])+' →'+b[2]+' →'+'Youbike1.0'+ str(list[1][0])+' →'+c[2]+' →'+ 'Youbike2.0'+ str(end_choice2[1][0][0]) + d[2]
		add_distance = round(d1 + d2 + d3 + d4, 2)
		suggest_list.append([add_time, add_step_by_step, add_distance, start_choice2[0][0][0], end_choice2[1][0][0], '需要換車Youbike1.0 to 2.0'])
	else:
		suggest_list = [[100000, '', 100000, '', '', '']]	
	return suggest_list
    
def midway_situation_2to1(list): #  [time, [name, coordinate], [name, coordinate]]
	if len(start_choice2[1]) > 0:
		suggest_list = []
		a = route_plan2(start, start_choice2[1][0][1], 'walking')         # route_plan抓出來的會是[距離,時間,路徑]
		b = route_plan2(start_choice2[1][0][1], list[2][1], 'bicycling')
		c = route_plan2(list[1][1], end_choice2[0][0][1], 'bicycling')
		d = route_plan2(end_choice2[0][0][1], end, 'walking')
		t1 = minutes(a[1])
		t2 = minutes(b[1])
		t3 = minutes(c[1])
		t4 = minutes(d[1])
		d1 = km(a[0])
		d2 = km(b[0])
		d3 = km(c[0])
		d4 = km(d[0])
		add_time = t1 + t2 + t3 + t4
		add_step_by_step = a[2]+' →'+'Youbike2.0'+str(start_choice2[1][0][0])+' →'+b[2]+' →'+'Youbike2.0'+ str(list[2][0])+' →'+c[2]+' →'+ 'Youbike1.0'+ str(end_choice2[0][0][0]) + d[2]
		add_distance = round(d1 + d2 + d3 + d4, 2)
		suggest_list.append([add_time, add_step_by_step, add_distance, start_choice2[1][0][0], end_choice2[0
		][0][0], '需要換車Youbike2.0 to 1.0'])
	else:
		suggest_list = [[100000, '', 100000, '', '', '']]
	return suggest_list
	


a = [20, ["捷運公館站(2號出口)",'25.01476,121.534538'], ["捷運公館站(2號出口)", '25.01385,121.53549']]

midway1 = (midway_situation_1to2(optimal_midway_list2))	
midway2 = (midway_situation_2to1(optimal_midway_list4))

len_l_start = len(start_choice2[0])
len_2_start = len(start_choice2[1])
len_1_end = len(end_choice2[0])
len_2_end = len(end_choice2[1])

#  print(len_l_start, len_2_start) 2,3

final_list = []

if len_l_start * len_1_end != 0:
	cur_path = ubike1_to_1(start_choice2, end_choice2)
	final_list.append(cur_path)
if len_2_start * len_2_end != 0:
	final_list.append(ubike2_to_2(start_choice2, end_choice2))
final_list.append(midway1)
final_list.append(midway2)
'''
print(final_list[0])
print(final_list[1])
print(final_list[2])
print(final_list[3])
'''
final = final_list[0] + final_list[1] + final_list[2] + final_list[3]
answer_list = sorted(final, key = lambda f : f[0], reverse = False)
	
#  print(answer_list, len(answer_list))
path_list = []
for i in range(2):
	path_list.append(answer_list[i])
def youbike1_depart(a):        # ubike1.0抓剩餘車輛
    for i in range(len(record_lst1)):
        if a == record_lst1[i][1]:
            b = record_lst1[i][2]
            return b
def youbike1_destinate(a):        # ubike1.0抓剩餘車位
    for i in range(len(record_lst1)):
        if a == record_lst1[i][1]:
            b = record_lst1[i][3]
            return b
def youbike2_depart(a):        # ubike2.0抓剩餘車輛
    for i in range(len(record_lst2)):
        if a == record_lst2[i][1]:
            b = record_lst2[i][2]
            return b
def youbike2_destinate(a):        # ubike2.0抓剩餘車位
    for i in range(len(record_lst1)):
        if a == record_lst2[i][1]:
            b = record_lst2[i][3]
            return b

for i in range(len(path_list)):
    if path_list[i][5] == 'Youbike1.0 to 1.0':
        depart_bicycle_1 = youbike1_depart(path_list[i][3])
        path_list[i].append(depart_bicycle_1)
        destinate_bicycle_1 = youbike1_destinate(path_list[i][4])
        path_list[i].append(destinate_bicycle_1)
    elif path_list[i][5] == 'Youbike2.0 to 2.0':
        depart_bicycle_2 = youbike2_depart(path_list[i][3])
        path_list[i].append(depart_bicycle_2)
        destinate_bicycle_2 = youbike2_destinate(path_list[i][4])
        path_list[i].append(destinate_bicycle_2)
    elif path_list[i][5] == '需要換車Youbike2.0 to 1.0':
        depart_bicycle_2 = youbike2_depart(path_list[i][3])
        path_list[i].append(depart_bicycle_2)
        destinate_bicycle_1 = youbike1_destinate(path_list[i][4])
        path_list[i].append(destinate_bicycle_1)
    elif path_list[i][5] == '需要換車Youbike1.0 to 2.0':
        depart_bicycle_1 = youbike1_depart(path_list[i][3])
        path_list[i].append(depart_bicycle_1)
        destinate_bicycle_2 = youbike2_destinate(path_list[i][4])
        path_list[i].append(destinate_bicycle_2)

answer = path_list

time1 = answer[0][0]
route1 = answer[0][1]
dis1 = answer[0][2]
start1 = answer[0][3]
purpose1 = answer[0][4]
method_ride1 = answer[0][5]
num_bike1 = answer[0][6]
num_empty1 = answer[0][7]
        
timedisans1 = "PATH1, " + "時間: " + str(time1) + "分鐘, " + "距離: " +  str(dis1) + "km" + " ,騎乘方法:" + str(method_ride1)
data1 = "起點: " + str(start1) + " ;尚餘車數:" + str(num_bike1) +  " ;終點:" + str(purpose1) + " ;尚餘車位:" + str(num_empty1) 
time2 = answer[1][0]
route2 = answer[1][1]
dis2 = answer[1][2]
start2 = answer[1][3]
purpose2 = answer[1][4]
method_ride2 = answer[1][5]
num_bike2 = answer[1][6]
num_empty2 = answer[1][7]
timedisans2 = "PATH2, " + "時間: " + str(time2) + "分鐘, " + "距離: " +  str(dis2) + "km" + " ,騎乘方法:" + str(method_ride2) 
data2 = "起點: " + str(start2) + " ;尚餘車數:" + str(num_bike2) +  " ;終點:" + str(purpose2) + " ;尚餘車位:" + str(num_empty2) 

if answer != []:
    page1 = Tk()
    page1.geometry("1500x800+0+0")

    class MainPage1(tk.Frame):
        def __init__(self):
            tk.Frame.__init__(self)
            self.grid()
            self.Cover_Pic = ImageTk.PhotoImage(file="椰林4.png")
            self.menu_image = tk.Label(self, image=self.Cover_Pic, compound=tk.CENTER)
            self.menu_image.grid(row=0, column=0, columnspan=10, rowspan=10)
            self.createWidgets()
        def createWidgets(self):
            f2 = tkFont.Font(size=16, family='Microsoft JhengHei')
            self.label1 = tk.Label(self ,text = timedisans1,height = 1, width = 55, font = f2, anchor = 'w')
            self.label1.place(x=50, y=130)
            self.label2 = tk.Label(self ,text = route1,height = 6, width = 100, font = f2, wraplength = 1300, justify = 'left', anchor = 'w')
            self.label2.place(x=50, y=230)
            self.label3 = tk.Label(self ,text = data1,height = 1, width = 75, font = f2, anchor = 'w')
            self.label3.place(x=50, y=180)
            self.label4 = tk.Label(self ,text = timedisans2,height = 1, width = 55, font = f2, anchor = 'w')
            self.label4.place(x=50, y=480)
            self.label5 = tk.Label(self ,text = route2,height = 6, width = 100, font = f2, wraplength = 1300, justify = 'left', anchor = 'w')
            self.label5.place(x=50, y=580)
            self.label6 = tk.Label(self ,text = data2,height = 1, width = 75, font = f2, anchor = 'w')
            self.label6.place(x=50, y=530)

    page1 = MainPage1()
    page1.master.title("最佳路徑!")
    page1.mainloop()
else:
    pass
