from tkinter import *
from tkinter import messagebox

import datetime as dt
import requests
from requests_html import HTMLSession
import json
from urllib.request import urlopen
from bs4 import BeautifulSoup
from icecream import ic
import re
from PIL import ImageTk, Image
import ctypes

#Site, Var name, Station, Grid Point x, Grid Point Y, X on Map, Y on Map    |       For the Map the higher the number the farher down or Right it is
sites = [('Bishopville II', 'bishopvilleII', 'CAE', 93, 73, 950, 425),
        ('Bluebird', 'bluebird', 'GSP', 53, 31, 500, 330), 
        ('Bulloch 1A', 'bulloch1a', 'CHS', 19, 52, 650, 700), ('Bulloch 1B', 'bulloch1b', 'CHS', 19, 52, 650, 720), 
        ('Cardinal', 'cardinal', 'ILM', 37, 60, 1150, 400), 
        ('Cherry', 'cherry', 'ILM', 26, 41, 1140, 475), 
        ('Conetoe', 'conetoe', 'RAH', 117, 65, 1550, 100), 
        ('Elk', 'elk', 'RAH', 58, 20, 1250, 280), 
        ('Freight Line', 'freightline', 'MHX', 20, 32, 1450, 250), 
        ('Gray Fox', 'grayfox', 'ILM', 43, 90, 1285, 290),
        ('Harding', 'harding', 'MHX', 22, 53, 1475, 150), 
        ('Hayes', 'hayes', 'RNK', 50, 27, 880, 40), 
        ('Hickory', 'hickory', 'MHX', 12, 24, 1400, 290), 
        ('Hickson', 'hickson', 'ILM', 17, 81, 1020, 320),
        ('Holly Swamp', 'hollyswamp', 'ILM', 44, 82, 1285, 315),
        ('Jefferson', 'jefferson', 'ILM', 11, 64, 965, 405), 
        ('Marshall', 'marshall', 'ILM', 13, 65, 1020, 420),
        ('McLean', 'mclean', 'RAH', 49, 10, 1100, 300), 
        ('Lily', 'lily', 'CHS', 30, 84, 800, 650),
        ('Ogburn', 'ogburn', 'CAE', 85, 93, 960, 330), 
        ('PG', 'pg', 'MHX', 9, 40, 1400, 175), 
        ('Richmond', 'richmond', 'CAE', 29, 27, 600, 600),
        ('Shorthorn', 'shorthorn', 'ILM', 29, 81, 1090, 320), 
        ('Sunflower', 'sunflower', 'ILM', 23, 38, 1040, 480), 
        ('Tedder', 'tedder', 'ILM', 17, 63, 1020, 400),
        ('Thunderhead', 'thunderhead', 'RAH', 33, 51, 1070, 200), 
        ('Upson', 'upson', 'FFC', 58, 51, 190, 680), 
        ('Van Buren', 'vanburen', 'RAH', 83, 23, 1300, 200), 
        ('Washington', 'washington', 'RNK', 85, 25, 1070, 80),
        ('Whitehall', 'whitehall', 'ILM', 18, 51, 1030, 440), 
        ('Whitetail', 'whitetail', 'ILM', 35, 69, 1150, 350)]

counties = [("nc", "surry"), ("nc", "cleveland"), ("nc", "cabarrus"), ("nc", "guilford"), ("nc", "randolph"), ("nc", "scotland"), ("nc", "hoke"), ("nc", "robeson"), ("nc", "sampson"), ("nc", "duplin"), ("nc", "lenoir"), ("nc", "greene"), ("nc", "wayne"), ("nc", "johnston"), ("nc", "edgecombe"), ("sc", "lee"), ("sc", "anderson"), ("sc", "chesterfield"), ("sc", "marlboro"), ("sc", "marion"), ("sc", "darlington"), ("sc", "dillon"), ("sc", "williamsburg"), ("sc", "allendale"), ("ga", "upson"), ("ga", "richmond"), ("ga", "bulloch")]

warningspdlower = 20
warningspdupper = 29

stowspd = 30

wind_speed_dict = {}

def make_windapi_request(office, gridX, gridY):
    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"
    headers = {
        'Content-Type': 'application/ld+json',
    }
    return requests.get(url, headers=headers) 

def get_wind_speed(site, station, gridx, gridy):
    spd1 = spd2 = spd3 = spd4 = None
    weather_data_response = make_windapi_request(station, gridx, gridy)
    if weather_data_response.status_code == 200:
        weather_data = weather_data_response.json()
        periods = weather_data['properties']['periods']

        if site == "Bluebird":
            formatted_weather_data = json.dumps(weather_data, indent=4)
            print(site, ' | ', formatted_weather_data)
        
        for i, period in enumerate(periods[:4], start=1):
            speed = re.search(r'(\d+) mph', period['windSpeed']).group(1)
            if i == 1:
                spd1 = speed
            elif i == 2:
                spd2 = speed
            elif i == 3:
                spd3 = speed
            elif i == 4:
                spd4 = speed

    else:
        spd1 = "N/A"
        spd2 = "N/A"
        spd3 = "N/A"
        spd4 = "N/A"
        
  
    wind_speed_dict[site] = [spd1, spd2, spd3, spd4]



def update_gui(site, var):
        globals()[f'{var}lblwind'].config(text= f"Wind:  {wind_speed_dict[site][0]} | {wind_speed_dict[site][1]} | {wind_speed_dict[site][2]} | {wind_speed_dict[site][3]}")
        if wind_speed_dict[site][0] != "N/A":
            if int(wind_speed_dict[site][0]) >= stowspd or int(wind_speed_dict[site][1]) >= stowspd:
                globals()[f'{var}'].config(bg='red')
                globals()[f'{var}lbl'].config(bg='red')
                globals()[f'{var}lblwind'].config(bg='red')
            elif (warningspdlower <= int(wind_speed_dict[site][0]) <= warningspdupper) or (warningspdlower <= int(wind_speed_dict[site][1]) <= warningspdupper):
                globals()[f'{var}'].config(bg='orange')
                globals()[f'{var}lbl'].config(bg='orange')
                globals()[f'{var}lblwind'].config(bg='orange')
            else:
                globals()[f'{var}'].config(bg='green')
                globals()[f'{var}lbl'].config(bg='green')
                globals()[f'{var}lblwind'].config(bg='green')


def get_data_then_update_gui():
    globals()['wind_speed_dict'] = {}
    for site, var, station, gridx, gridy, localx, localy in sites:
        if gridx and gridy:
            get_wind_speed(site, station, gridx, gridy)

    for site, var, station, gridx, gridy, localx, localy in sites:
        update_gui(site, var)
    update_time = dt.datetime.now() + dt.timedelta(minutes=30)
    update_t = update_time.strftime("%H:%M")
    timenow = dt.datetime.now().strftime("%H:%M")
    updated.config(text=f"Updated: {timenow}, Next: {update_t}")
    print("Updating in 30 Minutes...", update_t)
    root.after(1800000, get_data_then_update_gui)

myappid = 'NCC.Wind.Monitor.GUI'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

root = Tk()
root.title("NCC Wind Monitor")
root.geometry("1920x1080")
root.iconbitmap(r"G:\Shared drives\O&M\NCC Automations\Icons\Wind.ico")

image_map = Image.open(r"G:\Shared drives\O&M\NCC Automations\Icons\NC, SC, GA Map.jpg").resize((1920, 1080))
map_tk = ImageTk.PhotoImage(image_map)

maplbl = Label(root, image=map_tk)
maplbl.place(x=0, y=0, relwidth=1, relheight=1)


#Repeat for Each city, Also check the Lat and Long coords to ensure it's checking the correct city

for site, var, station, gridx, gridy, localx, localy in sites:
    globals()[var] = LabelFrame(root)
    globals()[var].place(x=localx, y=localy)
    globals()[f'{var}lbl'] = Label(globals()[var], text= site)
    globals()[f'{var}lbl'].grid(column=0, row= 0, columnspan= 3)






def legend_notes():
    messagebox.showinfo(parent=legend, title= "Legend Notes", message="""Column 1: Represents the Current time block; Morning, Afternoon, Night; of the Current day
Column 2: Represents the Next time block; Afternoon, Night, Morning of the next day if Column 1 is Night
Column 3: Represents the Morning of the next day unless Column 1 is Night, then it is Afternoon of the next Day
Data Pulled From:
https://wind.willyweather.com/""")



legend = LabelFrame(root)
legend.place(x=1640, y=280)
legendtitle = Label(legend, text="Legend | Units in Mph\nRed = Stow Site | Orange = Stow Almost Required")
legendtitle.grid(column= 0, row= 0, columnspan=2)
legend1 = Button(legend, text="Learn What Time the Columns Represent", command=legend_notes, bg='light green')
legend1.grid(column= 0, row= 1, columnspan=2)

index = 2
for site, var, station, gridx, gridy, localx, localy in sites:
    globals()[f'{var}legend'] = Label(legend, text=site)
    globals()[f'{var}legend'].grid(row= index, column= 0, sticky=W)
    globals()[f'{var}lblwind'] = Label(legend, text= "Wind: ")
    globals()[f'{var}lblwind'].grid(row= index, column= 1, sticky=W)
    index += 1



#TimeStamps
updated = Label(legend, text= "Time Stamps Displayed Here")
updated.grid(row=index+1, column= 0, columnspan=2)

#Update Button
update_butt = Button(legend, text="Update Wind Data Now", command= lambda: get_data_then_update_gui(), bg='light green')
update_butt.grid(row=index+2, column=0, columnspan=2)



get_data_then_update_gui()  
root.mainloop()
  






