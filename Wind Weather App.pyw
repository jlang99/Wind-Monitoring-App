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

#Site, Var name, Station, Grid Point x, Grid Point Y, X on Map, Y on Map    |       For the Map the higher the number the farther down or Right it is
sites = [('Bishopville II', 'bishopvilleII', 'CAE', 93, 73, 950, 425, TRUE),
        ('Bluebird', 'bluebird', 'GSP', 53, 31, 500, 330, TRUE), 
        ('Bulloch 1A', 'bulloch1a', 'CHS', 19, 52, 650, 700, TRUE), ('Bulloch 1B', 'bulloch1b', 'CHS', 19, 52, 650, 720, TRUE), 
        ('Cardinal', 'cardinal', 'ILM', 37, 60, 1150, 400, TRUE), 
        ('CDIA', 'cdia', 'GSP', 115, 65, 880, 200, FALSE), 
        ('Cherry', 'cherry', 'ILM', 26, 41, 1140, 475, TRUE), 
        ('Conetoe', 'conetoe', 'RAH', 117, 65, 1550, 100, TRUE), 
        ('Cougar', 'cougar', 'RAH', 57, 41, 1300, 200, FALSE), 
        ('Duplin', 'duplin', 'MHX', 12, 31, 1400, 250, FALSE), 
        ('Elk', 'elk', 'RAH', 58, 20, 1250, 280, TRUE), 
        ('Freight Line', 'freightline', 'MHX', 20, 32, 1450, 250, TRUE), 
        ('Gray Fox', 'grayfox', 'ILM', 43, 90, 1285, 290, TRUE),
        ('Harding', 'harding', 'MHX', 22, 53, 1475, 150, TRUE), 
        ('Harrison', 'harrison', 'RAH', 83, 23, 1310, 250, FALSE), 
        ('Hayes', 'hayes', 'RNK', 50, 27, 880, 40, TRUE), 
        ('Hickory', 'hickory', 'MHX', 12, 24, 1400, 290, TRUE), 
        ('Hickson', 'hickson', 'ILM', 17, 81, 1020, 320, TRUE),
        ('Holly Swamp', 'hollyswamp', 'ILM', 44, 82, 1285, 315, TRUE),
        ('Jefferson', 'jefferson', 'ILM', 11, 64, 965, 405, TRUE), 
        ('Marshall', 'marshall', 'ILM', 13, 65, 1020, 420, TRUE),
        ('McLean', 'mclean', 'RAH', 49, 10, 1100, 300, TRUE), 
        ('Lily', 'lily', 'CHS', 30, 84, 800, 650, TRUE),
        ('Longleaf Pine', 'longleafpine', 'GSP', 129, 100, 900, 80, TRUE),
        ('Ogburn', 'ogburn', 'CAE', 85, 93, 960, 330, TRUE), 
        ('PG', 'pg', 'MHX', 9, 40, 1400, 175, TRUE), 
        ('Richmond', 'richmond', 'CAE', 29, 27, 600, 600, TRUE),
        ('Shorthorn', 'shorthorn', 'ILM', 29, 81, 1090, 320, TRUE), 
        ('Sunflower', 'sunflower', 'ILM', 23, 38, 1040, 480, TRUE), 
        ('Tedder', 'tedder', 'ILM', 17, 63, 1020, 400, TRUE),
        ('Thunderhead', 'thunderhead', 'RAH', 33, 51, 1070, 200, TRUE), 
        ('Upson', 'upson', 'FFC', 58, 51, 190, 680, TRUE), 
        ('Van Buren', 'vanburen', 'RAH', 83, 23, 1310, 270, TRUE), 
        ('Violet', 'violet', 'GSP', 133, 74, 900, 170, FALSE), 
        ('Warbler', 'warbler', 'GSP', 90, 66, 750, 200, FALSE), 
        ('Washington', 'washington', 'RNK', 85, 25, 1070, 80, TRUE),
        ('Wayne I', 'waynei', 'RAH', 100, 36, 1400, 150, FALSE), 
        ('Wayne II', 'wayneii', 'RAH', 97, 39, 1390, 125, FALSE), 
        ('Wayne III', 'wayneiii', 'RAH', 105, 41, 1435, 125, FALSE), 
        ('Whitehall', 'whitehall', 'ILM', 18, 51, 1030, 440, TRUE), 
        ('Whitetail', 'whitetail', 'ILM', 35, 69, 1150, 350, TRUE)]

# --- Color Palette for Weather Conditions ---
# Sunny/Clear Scale (Yellows)
SUNNY = '#FFD700'          # Gold - For clear, sunny days
MOSTLY_SUNNY = '#FAFAD2'    # LightGoldenrodYellow - Predominantly sunny
PARTLY_SUNNY = '#EEE8AA'    # PaleGoldenrod - Sun is present but not dominant

# Cloudy/Transitional Scale (Greys/Muted Tones)
MIXED_CONDITIONS = '#D8D8BF' # Pale, muted beige for sun-to-cloud/rain transitions
PARTLY_CLOUDY = '#D3D3D3'    # LightGray - a neutral cloudy state
MOSTLY_CLOUDY = '#A9A9A9'    # DarkGray - Overcast is likely

# Precipitation Scale (Blues/Slates)
SLIGHT_CHANCE_RAIN = '#B0E0E6' # PowderBlue - Low probability of rain
CHANCE_RAIN = '#87CEEB'        # SkyBlue - A definite chance of rain
RAIN_LIKELY = '#4682B4'        # SteelBlue - Rain is probable
THUNDERSTORMS = '#778899'       # LightSlateGray - Storms are possible
HEAVY_THUNDERSTORMS = '#2F4F4F' # DarkSlateGray - Severe storms are likely


def get_weather_color(short_forecast):
    """
    Determines a background color based on keywords in the weather forecast.
    Keywords are checked in order of priority (most severe to least severe).
    If the forecast contains 'then', it only considers the conditions *before* it.
    """
    # Convert forecast to lowercase for case-insensitive matching
    forecast = short_forecast.lower()

    # If 'then' is in the forecast, only consider the part before it
    if ' then ' in forecast:
        primary_forecast = forecast.split(' then ')[0]
    else:
        primary_forecast = forecast

    # This list is ordered by priority. The first keyword found determines the color.
    weather_keywords = [
        # Highest priority: Storms and severe weather
        ("thunderstorms", HEAVY_THUNDERSTORMS),

        # Next priority: High probability of rain
        ("rain likely", RAIN_LIKELY),
        ("heavy rain", RAIN_LIKELY),

        # Next priority: A definite chance of precipitation
        ("chance rain", CHANCE_RAIN),
        ("rain showers", CHANCE_RAIN),
        ("scattered showers", CHANCE_RAIN),

        # Next priority: Low or slight chance of precipitation
        ("slight chance", SLIGHT_CHANCE_RAIN),
        ("isolated showers", SLIGHT_CHANCE_RAIN),
        ("drizzle", SLIGHT_CHANCE_RAIN),
        ("chance light rain", SLIGHT_CHANCE_RAIN),


        # Next priority: Obscured or overcast conditions
        ("fog", PARTLY_CLOUDY),
        ("mostly cloudy", MOSTLY_CLOUDY),
        ("cloudy", MOSTLY_CLOUDY), # General "cloudy" as a fallback

        # Next priority: Mixed sun and clouds
        ("partly sunny", PARTLY_SUNNY),
        ("partly cloudy", PARTLY_CLOUDY), # Catches "partly cloudy" specifically

        # Lowest priority: Predominantly clear
        ("mostly sunny", MOSTLY_SUNNY),
        ("mostly clear", MOSTLY_SUNNY),
        ("sunny", SUNNY),
        ("clear", SUNNY),
    ]

    # Find the first matching keyword in the primary forecast and return its color
    for keyword, color in weather_keywords:
        if keyword in primary_forecast:
            return color

    # If no keywords match, return a neutral default color
    messagebox.showinfo(title="NCC Weather App New Function", message=f"Color not found for {forecast}")
    return MIXED_CONDITIONS

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

def get_wind_speed(site, station, gridx, gridy, var, has_tracker):
    gust1 = gust2 = gust3 = gust4 = spd1 = spd2 = spd3 = spd4 = None
    weather_data_response = make_windapi_request(station, gridx, gridy)
    if weather_data_response.status_code == 200:
        weather_data = weather_data_response.json()

        #See the output from the API response. 
        #if site == "Cherry":
        #    print(json.dumps(weather_data, indent=4))
        
        periods = weather_data['properties']['periods']

        for i, period in enumerate(periods[:4], start=1):
            period_name = f"{period['name']}:"
            if i == 1:
                forecast_now = period['shortForecast']
                weather_color = get_weather_color(forecast_now)
                if has_tracker is FALSE:
                    globals()[f'{var}lbl'].config(bg=weather_color)

                
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



def update_gui(site, var, has_tracker):
    globals()[f'{var}legend'].config(bg=site_data_dict[site][8])
    if has_tracker:
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
    for site, var, station, gridx, gridy, localx, localy, tracking_site in sites:
        if gridx and gridy:
            get_wind_speed(site, station, gridx, gridy, var, tracking_site)

    for site, var, station, gridx, gridy, localx, localy, tracking_site in sites:
        update_gui(site, var, tracking_site)
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
root.title("NCC Weather App")
root.geometry("1920x1080")
root.iconbitmap(r"G:\Shared drives\O&M\NCC Automations\Icons\Wind.ico")

image_map = Image.open(r"G:\Shared drives\O&M\NCC Automations\Icons\NC, SC, GA Map.jpg").resize((1920, 1080))
map_tk = ImageTk.PhotoImage(image_map)

maplbl = Label(root, image=map_tk)
maplbl.place(x=0, y=0, relwidth=1, relheight=1)


#Repeat for Each city, Also check the Lat and Long coords to ensure it's checking the correct city
# Placing label on the map
for site, var, station, gridx, gridy, localx, localy, tracker_site in sites:
    globals()[var] = LabelFrame(root)
    globals()[var].place(x=localx, y=localy)
    globals()[f'{var}lbl'] = Label(globals()[var], text= site)
    globals()[f'{var}lbl'].pack()




dataFrame1 = Frame(root)
dataFrame1.place(x=1716, y=490)

dataFrame2 = Frame(root)
dataFrame2.place(x=1504, y=490)

dataFrame3 = Frame(root)
dataFrame3.place(x=1295, y=490)

nonTFrame = Frame(root)
nonTFrame.place(x=1235, y=490)

legend = LabelFrame(root)
legend.place(x=1640, y=310)

legendtitle = Label(legend, text=f"Legend | Units in Mph\nStow = Wind {stowspd}+ or Gusts {guststowspd} Mph\nWarning = Wind {warningspdlower}+ or Gust {gustwarninglow}+ Mph\nRed = Stow Site\nOrange = Warning\nYellow = Warning, Tomorrow")
legendtitle.pack()
#TimeStamps
updated = Label(legend, text= "Time Stamps Displayed Here")
updated.pack()
#Update Button
update_butt = Button(legend, text="Update Weather Data Now", command= lambda: get_data_then_update_gui(), bg='light green')
update_butt.pack(fill='x')



spd_wdth = 2
count=0
for site, var, station, gridx, gridy, localx, localy, tracker_site in sites:
    if tracker_site:
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

    else:
        globals()[f'{var}legend'] = Button(nonTFrame, text=site, command= lambda name=site: open_weather_forecast(name))
        globals()[f'{var}legend'].pack(anchor=W, fill= 'x')



get_data_then_update_gui()  
root.mainloop()
  
