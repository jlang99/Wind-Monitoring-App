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
import ctypes, os

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

# --- Color Palette for Weather Conditions ---
# Sunny/Clear Scale (Yellows)
SUNNY = '#FFD700'        # Gold - for clear, sunny days
MOSTLY_SUNNY = '#FAFAD2'  # LightGoldenrodYellow - for mostly sunny conditions
PARTLY_SUNNY = '#EEE8AA'  # PaleGoldenrod - for partly sunny skies

# Cloudy Scale (Greys)
PARTLY_CLOUDY = '#D3D3D3' # LightGray - for partly cloudy
MOSTLY_CLOUDY = '#A9A9A9'  # DarkGray - for mostly cloudy

# Rain/Thunderstorm Scale (Blues/Darker Greys)
SLIGHT_CHANCE_RAIN = '#ADD8E6'    # LightBlue - for a slight chance of rain
CHANCE_RAIN = '#87CEEB'          # SkyBlue - for a chance of rain
RAIN_LIKELY = '#4682B4'    # SteelBlue - for likely rain
THUNDERSTORMS = '#778899'       # LightSlateGray - for thunderstorms
HEAVY_THUNDERSTORMS = '#708090'  # SlateGray - for likely/heavy thunderstorms

# --- Weather to Color Mapping ---
weather_color_dict = {
    # Predominantly Sunny
    "Sunny": SUNNY,
    "Mostly Clear": SUNNY,
    "Mostly Sunny": MOSTLY_SUNNY,
    "Partly Sunny": PARTLY_SUNNY,

    # Predominantly Cloudy
    "Partly Cloudy": PARTLY_CLOUDY,
    "Mostly Cloudy": MOSTLY_CLOUDY,

    # Rain Showers
    "Slight Chance Rain Showers": SLIGHT_CHANCE_RAIN,
    "Chance Rain Showers": CHANCE_RAIN,
    
    # Thunderstorms
    "Slight Chance Showers And Thunderstorms": THUNDERSTORMS,
    "Chance Showers And Thunderstorms": HEAVY_THUNDERSTORMS,
    "Showers And Thunderstorms Likely": HEAVY_THUNDERSTORMS,

    # Transitional Weather (Sunny -> Cloudy/Rainy)
    "Mostly Sunny then Chance Showers And Thunderstorms": PARTLY_SUNNY,
    "Mostly Sunny then Slight Chance Showers And Thunderstorms": PARTLY_CLOUDY,
    "Mostly Sunny then Chance Rain Showers": PARTLY_CLOUDY,
    "Mostly Sunny then Slight Chance Rain Showers": PARTLY_CLOUDY,
    "Partly Sunny then Chance Showers And Thunderstorms": THUNDERSTORMS,
    "Partly Sunny then Slight Chance Showers And Thunderstorms": PARTLY_CLOUDY,

    # Transitional Weather (Cloudy -> Rainy)
    "Partly Cloudy then Slight Chance Showers And Thunderstorms": THUNDERSTORMS,
    "Mostly Cloudy then Slight Chance Rain Showers": MOSTLY_CLOUDY,
    "Mostly Cloudy then Chance Showers And Thunderstorms": HEAVY_THUNDERSTORMS,
    "Mostly Cloudy then Slight Chance Showers And Thunderstorms": THUNDERSTORMS,

    # Transitional Weather (Rainy -> Cloudy)
    "Slight Chance Showers And Thunderstorms then Partly Cloudy": THUNDERSTORMS,
    "Chance Rain Showers then Partly Cloudy": CHANCE_RAIN,
    "Chance Showers And Thunderstorms then Partly Cloudy": HEAVY_THUNDERSTORMS,

    # Transitional Weather (Rainy -> Rainy/Cloudy)
    "Slight Chance Rain Showers then Chance Showers And Thunderstorms": CHANCE_RAIN,
    "Slight Chance Rain Showers then Slight Chance Showers And Thunderstorms": THUNDERSTORMS,
    "Slight Chance Rain Showers then Mostly Cloudy": MOSTLY_CLOUDY,
    "Slight Chance Rain Showers then Partly Cloudy": PARTLY_CLOUDY,
    
    "Showers And Thunderstorms Likely then Chance Showers And Thunderstorms": HEAVY_THUNDERSTORMS,
}

warningspdlower = 25
warningspdupper = 29
gustwarninglow = 30
gustwarningup = 34

stowspd = 30
guststowspd = 35

site_data_dict = {}

def make_windapi_request(office, gridX, gridY):
    url = f"https://api.weather.gov/gridpoints/{office}/{gridX},{gridY}/forecast"
    headers = {
        'Content-Type': 'application/ld+json',
    }
    return requests.get(url, headers=headers) 

def get_wind_speed(site, station, gridx, gridy):
    gust1 = gust2 = gust3 = gust4 = spd1 = spd2 = spd3 = spd4 = None
    weather_data_response = make_windapi_request(station, gridx, gridy)
    if weather_data_response.status_code == 200:
        weather_data = weather_data_response.json()

        #See the output from the API response. 
        #if site == "Cherry":
        #    print(json.dumps(weather_data, indent=4))
        
        periods = weather_data['properties']['periods']

        #Used to gather data for color assignment based on shortForecast sentiment.
        for period in periods:
            forecast = period['shortForecast']
            if forecast not in weather_color_dict:
                messagebox.showwarning(parent=root, title="Weather Color Error", message=f"No matching color available for {forecast}!")
                weather_color_dict[forecast] = 'SystemButtonFace'

        for i, period in enumerate(periods[:4], start=1):
            period_name = f"{period['name']}:"
            if i == 1:
                forecast_now = period['shortForecast']
                if forecast_now in weather_color_dict:
                    weather_color = weather_color_dict[forecast_now]
                else:
                    weather_color = 'SystemButtonFace' #Tkinter Default
                
                with open(f"G:\\Shared drives\\O&M\\NCC Automations\\Daily Automations\\Weather Data\\{site} Weather Forecast.txt", "w") as file:
                    file.write(f"{period_name:<18} {period['detailedForecast']}")
            else:
                with open(f"G:\\Shared drives\\O&M\\NCC Automations\\Daily Automations\\Weather Data\\{site} Weather Forecast.txt", "a") as file:
                    file.write(f"\n{period_name:<18} {period['detailedForecast']}")

            speed_match = re.search(r'(\d+) mph', period['windSpeed'])
            gust_match = re.search(r'gusts as high as (\d+) mph', period['detailedForecast'])
            if speed_match:
                speed = speed_match.group(1)
            else:
                speed = "N/A"
            if gust_match:
                gust = gust_match.group(1)
            else:
                gust = 0

            if i == 1:
                spd1 = speed
                gust1 = gust
            elif i == 2:
                spd2 = speed
                gust2 = gust

            elif i == 3:
                gust3 = gust
                spd3 = speed
            elif i == 4:
                spd4 = speed
                gust4 = gust

    else:
        spd1 = "N/A"
        spd2 = "N/A"
        spd3 = "N/A"
        spd4 = "N/A"
        gust1 = "N/A"
        gust2 = "N/A"
        gust3 = "N/A"
        gust4 = "N/A"
  
    site_data_dict[site] = [spd1, spd2, spd3, spd4, gust1, gust2, gust3, gust4, weather_color]



def update_gui(site, var):
    globals()[f'{var}legend'].config(bg=site_data_dict[site][8])
    if site_data_dict[site][0] != "N/A": #Avoids overwriting a successful data pull with N/A
        globals()[f'{var}curspd'].config(text=site_data_dict[site][0])
        globals()[f'{var}nxtspd'].config(text=site_data_dict[site][1])
        globals()[f'{var}3rdspd'].config(text=site_data_dict[site][2])
        globals()[f'{var}finalspd'].config(text=site_data_dict[site][3])
        globals()[f'{var}gcurspd'].config(text=site_data_dict[site][4])
        globals()[f'{var}gnxtspd'].config(text=site_data_dict[site][5])
        globals()[f'{var}g3rdspd'].config(text=site_data_dict[site][6])
        globals()[f'{var}gfinalspd'].config(text=site_data_dict[site][7])
        if int(site_data_dict[site][0]) >= stowspd:
            bg_color = 'red'
        elif int(site_data_dict[site][4]) >= guststowspd:
            bg_color = 'red'
        elif (warningspdlower <= int(site_data_dict[site][0]) <= warningspdupper) or (gustwarninglow <= int(site_data_dict[site][4]) <= gustwarningup):
            bg_color = 'orange'
        elif (warningspdlower <= int(site_data_dict[site][1])) or (gustwarninglow <= int(site_data_dict[site][5])):
            bg_color = 'orange'
        elif (warningspdlower <= int(site_data_dict[site][2]) <= warningspdupper) or (warningspdlower <= int(site_data_dict[site][3]) <= warningspdupper) or (gustwarninglow <= int(site_data_dict[site][6]) <= gustwarningup) or (gustwarninglow <= int(site_data_dict[site][7]) <= gustwarningup):
            bg_color = 'yellow'
        else:
            bg_color = 'green'

        for label_suffix in ['', 'data', 'lbl', 'lblwind', 'curspd', 'nxtspd', '3rdspd', 'finalspd', 'gcurspd', 'gnxtspd', 'g3rdspd', 'gfinalspd', 'lblgust']:
            globals()[f'{var}{label_suffix}'].config(bg=bg_color)

def get_data_then_update_gui():
    globals()['site_data_dict'] = {}
    for site, var, station, gridx, gridy, localx, localy in sites:
        if gridx and gridy:
            get_wind_speed(site, station, gridx, gridy)

    for site, var, station, gridx, gridy, localx, localy in sites:
        update_gui(site, var)
    update_time = dt.datetime.now() + dt.timedelta(minutes=30)
    update_t = update_time.strftime("%H:%M")
    timenow = dt.datetime.now().strftime("%H:%M")
    globals()['updated'].config(text=f"Updated: {timenow} | Next: {update_t}")
    print("Updating in 30 Minutes...", update_t)
    root.after(1800000, get_data_then_update_gui)

def open_weather_forecast(site):
    os.startfile(f"G:\\Shared drives\\O&M\\NCC Automations\\Daily Automations\\Weather Data\\{site} Weather Forecast.txt")



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
Columns 2, 3 & 4: Represent the Next time block; Afternoon, Night, Morning of the next day if the previous is Night
Data Pulled From:
https://api.weather.gov/""")


dataFrame1 = Frame(root)
dataFrame1.place(x=1720, y=490)

dataFrame2 = Frame(root)
dataFrame2.place(x=1518, y=490)

dataFrame3 = Frame(root)
dataFrame3.place(x=1316, y=490)

legend = LabelFrame(root)
legend.place(x=1630, y=310)

legendtitle = Label(legend, text=f"Legend | Units in Mph\nStow = Wind {stowspd}+ or Gusts {guststowspd} Mph\nWarning = Wind {warningspdlower}+ or Gust {gustwarninglow}+ Mph\nRed = Stow Site\nOrange = Warning\nYellow = Warning, Tomorrow")
legendtitle.pack()
legend1 = Button(legend, text="Learn What Time the Columns Represent", command=legend_notes, bg='light green')
legend1.pack(fill='x')
#TimeStamps
updated = Label(legend, text= "Time Stamps Displayed Here")
updated.pack()
#Update Button
update_butt = Button(legend, text="Update Wind Data Now", command= lambda: get_data_then_update_gui(), bg='light green')
update_butt.pack(fill='x')



spd_wdth = 2
count=0
for site, var, station, gridx, gridy, localx, localy in sites:
    if count < 11:
        parent_frame = dataFrame1
    elif count < 22:
        parent_frame = dataFrame2
    else:
        parent_frame = dataFrame3
    globals()[f'{var}data'] = LabelFrame(parent_frame)
    frame = globals()[f'{var}data']
    frame.pack(anchor=W, fill= 'x')
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=2)

    globals()[f'{var}legend'] = Button(frame, text=site, command= lambda name=site: open_weather_forecast(name))
    globals()[f'{var}legend'].grid(row= 0, column= 0, sticky=W, rowspan=2)
    globals()[f'{var}lblwind'] = Label(frame, text= "Wind: ")
    globals()[f'{var}lblwind'].grid(row= 0, column= 1, sticky=E)
    globals()[f'{var}curspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}curspd'].grid(row= 0, column= 2, sticky=E)
    globals()[f'{var}nxtspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}nxtspd'].grid(row= 0, column= 3, sticky=E)
    globals()[f'{var}3rdspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}3rdspd'].grid(row= 0, column= 4, sticky=E)
    globals()[f'{var}finalspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}finalspd'].grid(row= 0, column= 5, sticky=E)

    globals()[f'{var}lblgust'] = Label(frame, text= "Gust: ")
    globals()[f'{var}lblgust'].grid(row= 1, column= 1, sticky=E)
    globals()[f'{var}gcurspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}gcurspd'].grid(row= 1, column= 2, sticky=E)
    globals()[f'{var}gnxtspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}gnxtspd'].grid(row= 1, column= 3, sticky=E)
    globals()[f'{var}g3rdspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}g3rdspd'].grid(row= 1, column= 4, sticky=E)
    globals()[f'{var}gfinalspd'] = Label(frame, text= "N/A", width=spd_wdth)
    globals()[f'{var}gfinalspd'].grid(row= 1, column= 5, sticky=E)
    count+=1


get_data_then_update_gui()  
root.mainloop()
  
