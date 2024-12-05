from tkinter import *
from tkinter import messagebox

import datetime as dt
import requests
from requests_html import HTMLSession

from urllib.request import urlopen
from bs4 import BeautifulSoup
from icecream import ic
import re
from PIL import ImageTk, Image
import ctypes

counties = [("nc", "surry"), ("nc", "cleveland"), ("nc", "cabarrus"), ("nc", "guilford"), ("nc", "randolph"), ("nc", "scotland"), ("nc", "hoke"), ("nc", "robeson"), ("nc", "sampson"), ("nc", "duplin"), ("nc", "lenoir"), ("nc", "greene"), ("nc", "wayne"), ("nc", "johnston"), ("nc", "edgecombe"), ("sc", "lee"), ("sc", "anderson"), ("sc", "chesterfield"), ("sc", "marlboro"), ("sc", "marion"), ("sc", "darlington"), ("sc", "dillon"), ("sc", "williamsburg"), ("sc", "allendale"), ("ga", "upson"), ("ga", "richmond"), ("ga", "bulloch")]

#ic(html_code)
session = HTMLSession()
wind_speed_dict = {}

def get_wind_speed(state, county):
    url = f"https://wind.willyweather.com/{state}/{county}-county.html"

    page = urlopen(url)
    html_bytes = page.read()
    htmlp = html_bytes.decode('utf-8')
    
    try:
        
        soup = BeautifulSoup(htmlp.html.html, 'html.parser')
        print("Read Me: ", soup)
        return # I added this to skip checking the website for data as the Website has increased security measures and the existing logic no longer works. I am planning to switch to a website that allows API calls. 
        content = soup.find('aside', class_='region-precis', first=True)
        step1 = content.find("dl", first=True)
        info = step1.find("dd", first=True)
        first = info.find("p", first=True)

        if first:
            try:
                second= first.find_next_sibling("p")
                third= second.find_next_sibling("p")
                firsttxt= first.text
                secondtxt = second.text
                thirdtxt = third.text
            except UnboundLocalError:
                firsttxt = '1 Mph'
                secondtxt = '1 Mph'
                thirdtxt = '1 Mph'
            except AttributeError:
                firsttxt = '1 Mph'
                secondtxt = '1 Mph'
                thirdtxt = '1 Mph'
    except AttributeError or UnboundLocalError:
        firsttxt = '1 Mph'
        secondtxt = '1 Mph'
        thirdtxt = '1 Mph'
    try:
        wind_speed1 = re.search(r'(\d+) Mph', firsttxt).group(1)
    except AttributeError or UnboundLocalError:
        wind_speed1 = "1"
    try:
        gust_speed1 = re.search(r'Gusts up to (\d+) Mph', firsttxt).group(1)
    except AttributeError or UnboundLocalError:
        gust_speed1 = "1"
    try:
        wind_speed2 = re.search(r'(\d+) Mph', secondtxt).group(1)
    except AttributeError or UnboundLocalError:
        wind_speed2 = "1"
    try:
        gust_speed2 = re.search(r'Gusts up to (\d+) Mph', secondtxt).group(1)
    except AttributeError or UnboundLocalError:
        gust_speed2 = "1"
    try:
        wind_speed3 = re.search(r'(\d+) Mph', thirdtxt).group(1)
    except AttributeError or UnboundLocalError:
        wind_speed3 = "1"
    try:
        gust_speed3 = re.search(r'Gusts up to (\d+) Mph', thirdtxt).group(1)
    except AttributeError or UnboundLocalError:
        gust_speed3 = "1"


    wind_speed_dict[county] = [wind_speed1, wind_speed2, wind_speed3, gust_speed1, gust_speed2, gust_speed3]



def update_gui():
    ic(wind_speed_dict)


    leelblwind.config(text= "Wind: " + wind_speed_dict['lee'][0] + " | " + wind_speed_dict["lee"][1] + " | " + wind_speed_dict["lee"][2])
    leelblgust.config(text= "Gusts: " + wind_speed_dict['lee'][3] + " | " + wind_speed_dict["lee"][4] + " | " + wind_speed_dict["lee"][5])
    if int(wind_speed_dict["lee"][3]) >= 35 or int(wind_speed_dict["lee"][4]) >= 35:
        lee.config(bg='red')
        leelbl.config(bg='red')
        leelblgust.config(bg='red')
        leelblwind.config(bg='red')
    elif int(wind_speed_dict["lee"][0]) >= 30 or int(wind_speed_dict["lee"][1]) >= 30:
        lee.config(bg='red')
        leelbl.config(bg='red')
        leelblgust.config(bg='red')
        leelblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["lee"][0]) <= 25) or (20 <= int(wind_speed_dict["lee"][1]) <= 25) or (20 <= int(wind_speed_dict["lee"][2]) <= 25):
        lee.config(bg='orange')
        leelbl.config(bg='orange')
        leelblgust.config(bg='orange')
        leelblwind.config(bg='orange')
    else:
        lee.config(bg='green')
        leelbl.config(bg='green')
        leelblgust.config(bg='green')
        leelblwind.config(bg='green')

    andersonlblwind.config(text= "Wind: " + wind_speed_dict['anderson'][0] + " | " + wind_speed_dict["anderson"][1] + " | " + wind_speed_dict["anderson"][2])
    andersonlblgust.config(text= "Gusts: " + wind_speed_dict['anderson'][3] + " | " + wind_speed_dict["anderson"][4] + " | " + wind_speed_dict["anderson"][5])
    if int(wind_speed_dict["anderson"][3]) >= 35 or int(wind_speed_dict["anderson"][4]) >= 35:
        anderson.config(bg='red')
        andersonlbl.config(bg='red')
        andersonlblgust.config(bg='red')
        andersonlblwind.config(bg='red')
    elif int(wind_speed_dict["anderson"][0]) >= 30 or int(wind_speed_dict["anderson"][1]) >= 30:
        anderson.config(bg='red')
        andersonlbl.config(bg='red')
        andersonlblgust.config(bg='red')
        andersonlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["anderson"][0]) <= 25) or (20 <= int(wind_speed_dict["anderson"][1]) <= 25) or (20 <= int(wind_speed_dict["anderson"][2]) <= 25):
        anderson.config(bg='orange')
        andersonlbl.config(bg='orange')
        andersonlblgust.config(bg='orange')
        andersonlblwind.config(bg='orange')
    else:
        anderson.config(bg='green')
        andersonlbl.config(bg='green')
        andersonlblgust.config(bg='green')
        andersonlblwind.config(bg='green')

    bullochlblwind.config(text= "Wind: " + wind_speed_dict['bulloch'][0] + " | " + wind_speed_dict["bulloch"][1] + " | " + wind_speed_dict["bulloch"][2])
    bullochlblgust.config(text= "Gusts: " + wind_speed_dict['bulloch'][4] + " | " + wind_speed_dict["bulloch"][4] + " | " + wind_speed_dict["bulloch"][5])
    if int(wind_speed_dict["bulloch"][3]) >= 35 or int(wind_speed_dict["bulloch"][4]) >= 35:
        bulloch.config(bg='red')
        bullochlbl.config(bg='red')
        bullochlblgust.config(bg='red')
        bullochlblwind.config(bg='red')
    elif int(wind_speed_dict["bulloch"][0]) >= 30 or int(wind_speed_dict["bulloch"][1]) >= 30:
        bulloch.config(bg='red')
        bullochlbl.config(bg='red')
        bullochlblgust.config(bg='red')
        bullochlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["bulloch"][0]) <= 25) or (20 <= int(wind_speed_dict["bulloch"][1]) <= 25) or (20 <= int(wind_speed_dict["bulloch"][2]) <= 25):
        bulloch.config(bg='orange')
        bullochlbl.config(bg='orange')
        bullochlblgust.config(bg='orange')
        bullochlblwind.config(bg='orange')
    else:
        bulloch.config(bg='green')
        bullochlbl.config(bg='green')
        bullochlblgust.config(bg='green')
        bullochlblwind.config(bg='green')

    allendalelblwind.config(text= "Wind: " + wind_speed_dict['allendale'][0] + " | " + wind_speed_dict["allendale"][1] + " | " + wind_speed_dict["allendale"][2])
    allendalelblgust.config(text= "Gusts: " + wind_speed_dict['allendale'][4] + " | " + wind_speed_dict["allendale"][4] + " | " + wind_speed_dict["allendale"][5])
    if int(wind_speed_dict["allendale"][3]) >= 35 or int(wind_speed_dict["allendale"][4]) >= 35:
        allendale.config(bg='red')
        allendalelbl.config(bg='red')
        allendalelblgust.config(bg='red')
        allendalelblwind.config(bg='red')
    elif int(wind_speed_dict["allendale"][0]) >= 30 or int(wind_speed_dict["allendale"][1]) >= 30:
        allendale.config(bg='red')
        allendalelbl.config(bg='red')
        allendalelblgust.config(bg='red')
        allendalelblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["allendale"][0]) <= 25) or (20 <= int(wind_speed_dict["allendale"][1]) <= 25) or (20 <= int(wind_speed_dict["allendale"][2]) <= 25):
        allendale.config(bg='orange')
        allendalelbl.config(bg='orange')
        allendalelblgust.config(bg='orange')
        allendalelblwind.config(bg='orange')
    else:
        allendale.config(bg='green')
        allendalelbl.config(bg='green')
        allendalelblgust.config(bg='green')
        allendalelblwind.config(bg='green')

    williamsburglblwind.config(text= "Wind: " + wind_speed_dict['williamsburg'][0] + " | " + wind_speed_dict["williamsburg"][1] + " | " + wind_speed_dict["williamsburg"][2])
    williamsburglblgust.config(text= "Gusts: " + wind_speed_dict['williamsburg'][4] + " | " + wind_speed_dict["williamsburg"][4] + " | " + wind_speed_dict["williamsburg"][5])
    if int(wind_speed_dict["williamsburg"][3]) >= 35 or int(wind_speed_dict["williamsburg"][4]) >= 35:
        williamsburg.config(bg='red')
        williamsburglbl.config(bg='red')
        williamsburglblgust.config(bg='red')
        williamsburglblwind.config(bg='red')
    elif int(wind_speed_dict["williamsburg"][0]) >= 30 or int(wind_speed_dict["williamsburg"][1]) >= 30:
        williamsburg.config(bg='red')
        williamsburglbl.config(bg='red')
        williamsburglblgust.config(bg='red')
        williamsburglblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["williamsburg"][0]) <= 25) or (20 <= int(wind_speed_dict["williamsburg"][1]) <= 25) or (20 <= int(wind_speed_dict["williamsburg"][2]) <= 25):
        williamsburg.config(bg='orange')
        williamsburglbl.config(bg='orange')
        williamsburglblgust.config(bg='orange')
        williamsburglblwind.config(bg='orange')
    else:
        williamsburg.config(bg='green')
        williamsburglbl.config(bg='green')
        williamsburglblgust.config(bg='green')
        williamsburglblwind.config(bg='green')


    edgecombelblwind.config(text= "Wind: " + wind_speed_dict['edgecombe'][0] + " | " + wind_speed_dict["edgecombe"][1] + " | " + wind_speed_dict["edgecombe"][2])
    edgecombelblgust.config(text= "Gusts: " + wind_speed_dict['edgecombe'][4] + " | " + wind_speed_dict["edgecombe"][4] + " | " + wind_speed_dict["edgecombe"][5])
    if int(wind_speed_dict["edgecombe"][3]) >= 35 or int(wind_speed_dict["edgecombe"][4]) >= 35 or int(wind_speed_dict["edgecombe"][0]) >= 30 or int(wind_speed_dict["edgecombe"][1]) >= 30:
        edgecombe.config(bg='red')
        edgecombelbl.config(bg='red')
        edgecombelblgust.config(bg='red')
        edgecombelblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["edgecombe"][0]) <= 25) or (20 <= int(wind_speed_dict["edgecombe"][1]) <= 25) or (20 <= int(wind_speed_dict["edgecombe"][2]) <= 25):
        edgecombe.config(bg='orange')
        edgecombelbl.config(bg='orange')
        edgecombelblgust.config(bg='orange')
        edgecombelblwind.config(bg='orange')
    else:
        edgecombe.config(bg='green')
        edgecombelbl.config(bg='green')
        edgecombelblgust.config(bg='green')
        edgecombelblwind.config(bg='green')

    richmondlblwind.config(text= "Wind: " + wind_speed_dict['richmond'][0] + " | " + wind_speed_dict["richmond"][1] + " | " + wind_speed_dict["richmond"][2])
    richmondlblgust.config(text= "Gusts: " + wind_speed_dict['richmond'][3] + " | " + wind_speed_dict["richmond"][4] + " | " + wind_speed_dict["richmond"][5])
    if int(wind_speed_dict["richmond"][3]) >= 35 or int(wind_speed_dict["richmond"][4]) >= 35:
        richmond.config(bg='red')
        richmondlbl.config(bg='red')
        richmondlblgust.config(bg='red')
        richmondlblwind.config(bg='red')
    elif int(wind_speed_dict["richmond"][0]) >= 30 or int(wind_speed_dict["richmond"][1]) >= 30:
        richmond.config(bg='red')
        richmondlbl.config(bg='red')
        richmondlblgust.config(bg='red')
        richmondlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["richmond"][0]) <= 25) or (20 <= int(wind_speed_dict["richmond"][1]) <= 25) or (20 <= int(wind_speed_dict["richmond"][2]) <= 25):
        richmond.config(bg='orange')
        richmondlbl.config(bg='orange')
        richmondlblgust.config(bg='orange')
        richmondlblwind.config(bg='orange')
    else:
        richmond.config(bg='green')
        richmondlbl.config(bg='green')
        richmondlblgust.config(bg='green')
        richmondlblwind.config(bg='green')

    upsonlblwind.config(text= "Wind: " + wind_speed_dict['upson'][0] + " | " + wind_speed_dict["upson"][1] + " | " + wind_speed_dict["upson"][2])
    upsonlblgust.config(text= "Gusts: " + wind_speed_dict['upson'][3] + " | " + wind_speed_dict["upson"][4] + " | " + wind_speed_dict["upson"][5])
    if int(wind_speed_dict["upson"][3]) >= 35 or int(wind_speed_dict["upson"][4]) >= 35:
        upson.config(bg='red')
        upsonlbl.config(bg='red')
        upsonlblgust.config(bg='red')
        upsonlblwind.config(bg='red')
    elif int(wind_speed_dict["upson"][0]) >= 30 or int(wind_speed_dict["upson"][1]) >= 30:
        upson.config(bg='red')
        upsonlbl.config(bg='red')
        upsonlblgust.config(bg='red')
        upsonlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["upson"][0]) <= 25) or (20 <= int(wind_speed_dict["upson"][1]) <= 25) or (20 <= int(wind_speed_dict["upson"][2]) <= 25):
        upson.config(bg='orange')
        upsonlbl.config(bg='orange')
        upsonlblgust.config(bg='orange')
        upsonlblwind.config(bg='orange')
    else:
        upson.config(bg='green')
        upsonlbl.config(bg='green')
        upsonlblgust.config(bg='green')
        upsonlblwind.config(bg='green')

    darlingtonlblwind.config(text= "Wind: " + wind_speed_dict['darlington'][0] + " | " + wind_speed_dict["darlington"][1] + " | " + wind_speed_dict["darlington"][2])
    darlingtonlblgust.config(text= "Gusts: " + wind_speed_dict['darlington'][3] + " | " + wind_speed_dict["darlington"][4] + " | " + wind_speed_dict["darlington"][5])
    if int(wind_speed_dict["darlington"][3]) >= 35 or int(wind_speed_dict["darlington"][4]) >= 35:
        darlington.config(bg='red')
        darlingtonlbl.config(bg='red')
        darlingtonlblgust.config(bg='red')
        darlingtonlblwind.config(bg='red')
    elif int(wind_speed_dict["darlington"][0]) >= 30 or int(wind_speed_dict["darlington"][1]) >= 30:
        darlington.config(bg='red')
        darlingtonlbl.config(bg='red')
        darlingtonlblgust.config(bg='red')
        darlingtonlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["darlington"][0]) <= 25) or (20 <= int(wind_speed_dict["darlington"][1]) <= 25) or (20 <= int(wind_speed_dict["darlington"][2]) <= 25):
        darlington.config(bg='orange')
        darlingtonlbl.config(bg='orange')
        darlingtonlblgust.config(bg='orange')
        darlingtonlblwind.config(bg='orange')
    else:
        darlington.config(bg='green')
        darlingtonlbl.config(bg='green')
        darlingtonlblgust.config(bg='green')
        darlingtonlblwind.config(bg='green')

    dillonlblwind.config(text= "Wind: " + wind_speed_dict['dillon'][0] + " | " + wind_speed_dict["dillon"][1] + " | " + wind_speed_dict["dillon"][2])
    dillonlblgust.config(text= "Gusts: " + wind_speed_dict['dillon'][3] + " | " + wind_speed_dict["dillon"][4] + " | " + wind_speed_dict["dillon"][5])
    if int(wind_speed_dict["dillon"][3]) >= 35 or int(wind_speed_dict["dillon"][4]) >= 35:
        dillon.config(bg='red')
        dillonlbl.config(bg='red')
        dillonlblgust.config(bg='red')
        dillonlblwind.config(bg='red')
    elif int(wind_speed_dict["dillon"][0]) >= 30 or int(wind_speed_dict["dillon"][1]) >= 30:
        dillon.config(bg='red')
        dillonlbl.config(bg='red')
        dillonlblgust.config(bg='red')
        dillonlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["dillon"][0]) <= 25) or (20 <= int(wind_speed_dict["dillon"][1]) <= 25) or (20 <= int(wind_speed_dict["dillon"][2]) <= 25):
        dillon.config(bg='orange')
        dillonlbl.config(bg='orange')
        dillonlblgust.config(bg='orange')
        dillonlblwind.config(bg='orange')
    else:
        dillon.config(bg='green')
        dillonlbl.config(bg='green')
        dillonlblgust.config(bg='green')
        dillonlblwind.config(bg='green')

    marionlblwind.config(text= "Wind: " + wind_speed_dict['marion'][0] + " | " + wind_speed_dict["marion"][1] + " | " + wind_speed_dict["marion"][2])
    marionlblgust.config(text= "Gusts: " + wind_speed_dict['marion'][3] + " | " + wind_speed_dict["marion"][4] + " | " + wind_speed_dict["marion"][5])
    if int(wind_speed_dict["marion"][3]) >= 35 or int(wind_speed_dict["marion"][4]) >= 35:
        marion.config(bg='red')
        marionlbl.config(bg='red')
        marionlblgust.config(bg='red')
        marionlblwind.config(bg='red')
    elif int(wind_speed_dict["marion"][0]) >= 30 or int(wind_speed_dict["marion"][1]) >= 30:
        marion.config(bg='red')
        marionlbl.config(bg='red')
        marionlblgust.config(bg='red')
        marionlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["marion"][0]) <= 25) or (20 <= int(wind_speed_dict["marion"][1]) <= 25) or (20 <= int(wind_speed_dict["marion"][2]) <= 25):
        marion.config(bg='orange')
        marionlbl.config(bg='orange')
        marionlblgust.config(bg='orange')
        marionlblwind.config(bg='orange')
    else:
        marion.config(bg='green')
        marionlbl.config(bg='green')
        marionlblgust.config(bg='green')
        marionlblwind.config(bg='green')

    chesterfieldlblwind.config(text= "Wind: " + wind_speed_dict['chesterfield'][0] + " | " + wind_speed_dict["chesterfield"][1] + " | " + wind_speed_dict["chesterfield"][2])
    chesterfieldlblgust.config(text= "Gusts: " + wind_speed_dict['chesterfield'][3] + " | " + wind_speed_dict["chesterfield"][4] + " | " + wind_speed_dict["chesterfield"][5])
    if int(wind_speed_dict["chesterfield"][3]) >= 35 or int(wind_speed_dict["chesterfield"][4]) >= 35:
        chesterfield.config(bg='red')
        chesterfieldlbl.config(bg='red')
        chesterfieldlblgust.config(bg='red')
        chesterfieldlblwind.config(bg='red')
    elif int(wind_speed_dict["chesterfield"][0]) >= 30 or int(wind_speed_dict["chesterfield"][1]) >= 30:
        chesterfield.config(bg='red')
        chesterfieldlbl.config(bg='red')
        chesterfieldlblgust.config(bg='red')
        chesterfieldlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["chesterfield"][0]) <= 25) or (20 <= int(wind_speed_dict["chesterfield"][1]) <= 25) or (20 <= int(wind_speed_dict["chesterfield"][2]) <= 25):
        chesterfield.config(bg='orange')
        chesterfieldlbl.config(bg='orange')
        chesterfieldlblgust.config(bg='orange')
        chesterfieldlblwind.config(bg='orange')
    else:
        chesterfield.config(bg='green')
        chesterfieldlbl.config(bg='green')
        chesterfieldlblgust.config(bg='green')
        chesterfieldlblwind.config(bg='green')

    marlborolblwind.config(text= "Wind: " + wind_speed_dict['marlboro'][0] + " | " + wind_speed_dict["marlboro"][1] + " | " + wind_speed_dict["marlboro"][2])
    marlborolblgust.config(text= "Gusts: " + wind_speed_dict['marlboro'][3] + " | " + wind_speed_dict["marlboro"][4] + " | " + wind_speed_dict["marlboro"][5])
    if int(wind_speed_dict["marlboro"][3]) >= 35 or int(wind_speed_dict["marlboro"][4]) >= 35:
        marlboro.config(bg='red')
        marlborolbl.config(bg='red')
        marlborolblgust.config(bg='red')
        marlborolblwind.config(bg='red')
    elif int(wind_speed_dict["marlboro"][0]) >= 30 or int(wind_speed_dict["marlboro"][1]) >= 30:
        marlboro.config(bg='red')
        marlborolbl.config(bg='red')
        marlborolblgust.config(bg='red')
        marlborolblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["marlboro"][0]) <= 25) or (20 <= int(wind_speed_dict["marlboro"][1]) <= 25) or (20 <= int(wind_speed_dict["marlboro"][2]) <= 25):
        marlboro.config(bg='orange')
        marlborolbl.config(bg='orange')
        marlborolblgust.config(bg='orange')
        marlborolblwind.config(bg='orange')
    else:
        marlboro.config(bg='green')
        marlborolbl.config(bg='green')
        marlborolblgust.config(bg='green')
        marlborolblwind.config(bg='green')


    surrylblwind.config(text= "Wind: " + wind_speed_dict['surry'][0] + " | " + wind_speed_dict["surry"][1] + " | " + wind_speed_dict["surry"][2])
    surrylblgust.config(text= "Gusts: " + wind_speed_dict['surry'][3] + " | " + wind_speed_dict["surry"][4] + " | " + wind_speed_dict["surry"][5])
    if int(wind_speed_dict["surry"][3]) >= 35 or int(wind_speed_dict["surry"][4]) >= 35:
        surry.config(bg='red')
        surrylbl.config(bg='red')
        surrylblgust.config(bg='red')
        surrylblwind.config(bg='red')
    elif int(wind_speed_dict["surry"][0]) >= 30 or int(wind_speed_dict["surry"][1]) >= 30:
        surry.config(bg='red')
        surrylbl.config(bg='red')
        surrylblgust.config(bg='red')
        surrylblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["surry"][0]) <= 25) or (20 <= int(wind_speed_dict["surry"][1]) <= 25) or (20 <= int(wind_speed_dict["surry"][2]) <= 25):
        surry.config(bg='orange')
        surrylbl.config(bg='orange')
        surrylblgust.config(bg='orange')
        surrylblwind.config(bg='orange')
    else:
        surry.config(bg='green')
        surrylbl.config(bg='green')
        surrylblgust.config(bg='green')
        surrylblwind.config(bg='green')

    guilfordlblwind.config(text= "Wind: " + wind_speed_dict['guilford'][0] + " | " + wind_speed_dict["guilford"][1] + " | " + wind_speed_dict["guilford"][2])
    guilfordlblgust.config(text= "Gusts: " + wind_speed_dict['guilford'][3] + " | " + wind_speed_dict["guilford"][4] + " | " + wind_speed_dict["guilford"][5])
    if int(wind_speed_dict["guilford"][3]) >= 35 or int(wind_speed_dict["guilford"][4]) >= 35:
        guilford.config(bg='red')
        guilfordlbl.config(bg='red')
        guilfordlblgust.config(bg='red')
        guilfordlblwind.config(bg='red')
    elif int(wind_speed_dict["guilford"][0]) >= 30 or int(wind_speed_dict["guilford"][1]) >= 30:
        guilford.config(bg='red')
        guilfordlbl.config(bg='red')
        guilfordlblgust.config(bg='red')
        guilfordlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["guilford"][0]) <= 25) or (20 <= int(wind_speed_dict["guilford"][1]) <= 25) or (20 <= int(wind_speed_dict["guilford"][2]) <= 25):
        guilford.config(bg='orange')
        guilfordlbl.config(bg='orange')
        guilfordlblgust.config(bg='orange')
        guilfordlblwind.config(bg='orange')
    else:
        guilford.config(bg='green')
        guilfordlbl.config(bg='green')
        guilfordlblgust.config(bg='green')
        guilfordlblwind.config(bg='green')


    randolphlblwind.config(text= "Wind: " + wind_speed_dict['randolph'][0] + " | " + wind_speed_dict["randolph"][1] + " | " + wind_speed_dict["randolph"][2])
    randolphlblgust.config(text= "Gusts: " + wind_speed_dict['randolph'][3] + " | " + wind_speed_dict["randolph"][4] + " | " + wind_speed_dict["randolph"][5])
    if int(wind_speed_dict["randolph"][3]) >= 35 or int(wind_speed_dict["randolph"][4]) >= 35:
        randolph.config(bg='red')
        randolphlbl.config(bg='red')
        randolphlblgust.config(bg='red')
        randolphlblwind.config(bg='red')
    elif int(wind_speed_dict["randolph"][0]) >= 30 or int(wind_speed_dict["randolph"][1]) >= 30:
        randolph.config(bg='red')
        randolphlbl.config(bg='red')
        randolphlblgust.config(bg='red')
        randolphlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["randolph"][0]) <= 25) or (20 <= int(wind_speed_dict["randolph"][1]) <= 25) or (20 <= int(wind_speed_dict["randolph"][2]) <= 25):
        randolph.config(bg='orange')
        randolphlbl.config(bg='orange')
        randolphlblgust.config(bg='orange')
        randolphlblwind.config(bg='orange')
    else:
        randolph.config(bg='green')
        randolphlbl.config(bg='green')
        randolphlblgust.config(bg='green')
        randolphlblwind.config(bg='green')

    hokelblwind.config(text= "Wind: " + wind_speed_dict['hoke'][0] + " | " + wind_speed_dict["hoke"][1] + " | " + wind_speed_dict["hoke"][2])
    hokelblgust.config(text= "Gusts: " + wind_speed_dict['hoke'][3] + " | " + wind_speed_dict["hoke"][4] + " | " + wind_speed_dict["hoke"][5])
    if int(wind_speed_dict["hoke"][3]) >= 35 or int(wind_speed_dict["hoke"][4]) >= 35:
        hoke.config(bg='red')
        hokelbl.config(bg='red')
        hokelblgust.config(bg='red')
        hokelblwind.config(bg='red')
    elif int(wind_speed_dict["hoke"][0]) >= 30 or int(wind_speed_dict["hoke"][1]) >= 30:
        hoke.config(bg='red')
        hokelbl.config(bg='red')
        hokelblgust.config(bg='red')
        hokelblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["hoke"][0]) <= 25) or (20 <= int(wind_speed_dict["hoke"][1]) <= 25) or (20 <= int(wind_speed_dict["hoke"][2]) <= 25):
        hoke.config(bg='orange')
        hokelbl.config(bg='orange')
        hokelblgust.config(bg='orange')
        hokelblwind.config(bg='orange')
    else:
        hoke.config(bg='green')
        hokelbl.config(bg='green')
        hokelblgust.config(bg='green')
        hokelblwind.config(bg='green')

    robesonlblwind.config(text= "Wind: " + wind_speed_dict['robeson'][0] + " | " + wind_speed_dict["robeson"][1] + " | " + wind_speed_dict["robeson"][2])
    robesonlblgust.config(text= "Gusts: " + wind_speed_dict['robeson'][3] + " | " + wind_speed_dict["robeson"][4] + " | " + wind_speed_dict["robeson"][5])
    if int(wind_speed_dict["robeson"][3]) >= 35 or int(wind_speed_dict["robeson"][4]) >= 35:
        robeson.config(bg='red')
        robesonlbl.config(bg='red')
        robesonlblgust.config(bg='red')
        robesonlblwind.config(bg='red')
    elif int(wind_speed_dict["robeson"][0]) >= 30 or int(wind_speed_dict["robeson"][1]) >= 30:
        robeson.config(bg='red')
        robesonlbl.config(bg='red')
        robesonlblgust.config(bg='red')
        robesonlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["robeson"][0]) <= 25) or (20 <= int(wind_speed_dict["robeson"][1]) <= 25) or (20 <= int(wind_speed_dict["robeson"][2]) <= 25):
        robeson.config(bg='orange')
        robesonlbl.config(bg='orange')
        robesonlblgust.config(bg='orange')
        robesonlblwind.config(bg='orange')
    else:
        robeson.config(bg='green')
        robesonlbl.config(bg='green')
        robesonlblgust.config(bg='green')
        robesonlblwind.config(bg='green')

    scotlandlblwind.config(text= "Wind: " + wind_speed_dict['scotland'][0] + " | " + wind_speed_dict["scotland"][1] + " | " + wind_speed_dict["scotland"][2])
    scotlandlblgust.config(text= "Gusts: " + wind_speed_dict['scotland'][3] + " | " + wind_speed_dict["scotland"][4] + " | " + wind_speed_dict["scotland"][5])
    if int(wind_speed_dict["scotland"][3]) >= 35 or int(wind_speed_dict["scotland"][4]) >= 35:
        scotland.config(bg='red')
        scotlandlbl.config(bg='red')
        scotlandlblgust.config(bg='red')
        scotlandlblwind.config(bg='red')
    elif int(wind_speed_dict["scotland"][0]) >= 30 or int(wind_speed_dict["scotland"][1]) >= 30:
        scotland.config(bg='red')
        scotlandlbl.config(bg='red')
        scotlandlblgust.config(bg='red')
        scotlandlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["scotland"][0]) <= 25) or (20 <= int(wind_speed_dict["scotland"][1]) <= 25) or (20 <= int(wind_speed_dict["scotland"][2]) <= 25):
        scotland.config(bg='orange')
        scotlandlbl.config(bg='orange')
        scotlandlblgust.config(bg='orange')
        scotlandlblwind.config(bg='orange')
    else:
        scotland.config(bg='green')
        scotlandlbl.config(bg='green')
        scotlandlblgust.config(bg='green')
        scotlandlblwind.config(bg='green')

    sampsonlblwind.config(text= "Wind: " + wind_speed_dict['sampson'][0] + " | " + wind_speed_dict["sampson"][1] + " | " + wind_speed_dict["sampson"][2])
    sampsonlblgust.config(text= "Gusts: " + wind_speed_dict['sampson'][3] + " | " + wind_speed_dict["sampson"][4] + " | " + wind_speed_dict["sampson"][5])
    if int(wind_speed_dict["sampson"][3]) >= 35 or int(wind_speed_dict["sampson"][4]) >= 35:
        sampson.config(bg='red')
        sampsonlbl.config(bg='red')
        sampsonlblgust.config(bg='red')
        sampsonlblwind.config(bg='red')
    elif int(wind_speed_dict["sampson"][0]) >= 30 or int(wind_speed_dict["sampson"][1]) >= 30:
        sampson.config(bg='red')
        sampsonlbl.config(bg='red')
        sampsonlblgust.config(bg='red')
        sampsonlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["sampson"][0]) <= 25) or (20 <= int(wind_speed_dict["sampson"][1]) <= 25) or (20 <= int(wind_speed_dict["sampson"][2]) <= 25):
        sampson.config(bg='orange')
        sampsonlbl.config(bg='orange')
        sampsonlblgust.config(bg='orange')
        sampsonlblwind.config(bg='orange')
    else:
        sampson.config(bg='green')
        sampsonlbl.config(bg='green')
        sampsonlblgust.config(bg='green')
        sampsonlblwind.config(bg='green')

    duplinlblwind.config(text= "Wind: " + wind_speed_dict['duplin'][0] + " | " + wind_speed_dict["duplin"][1] + " | " + wind_speed_dict["duplin"][2])
    duplinlblgust.config(text= "Gusts: " + wind_speed_dict['duplin'][3] + " | " + wind_speed_dict["duplin"][4] + " | " + wind_speed_dict["duplin"][5])
    if int(wind_speed_dict["duplin"][3]) >= 35 or int(wind_speed_dict["duplin"][4]) >= 35:
        duplin.config(bg='red')
        duplinlbl.config(bg='red')
        duplinlblgust.config(bg='red')
        duplinlblwind.config(bg='red')
    elif int(wind_speed_dict["duplin"][0]) >= 30 or int(wind_speed_dict["duplin"][1]) >= 30:
        duplin.config(bg='red')
        duplinlbl.config(bg='red')
        duplinlblgust.config(bg='red')
        duplinlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["duplin"][0]) <= 25) or (20 <= int(wind_speed_dict["duplin"][1]) <= 25) or (20 <= int(wind_speed_dict["duplin"][2]) <= 25):
        duplin.config(bg='orange')
        duplinlbl.config(bg='orange')
        duplinlblgust.config(bg='orange')
        duplinlblwind.config(bg='orange')
    else:
        duplin.config(bg='green')
        duplinlbl.config(bg='green')
        duplinlblgust.config(bg='green')
        duplinlblwind.config(bg='green')

    lenoirlblwind.config(text= "Wind: " + wind_speed_dict['lenoir'][0] + " | " + wind_speed_dict["lenoir"][1] + " | " + wind_speed_dict["lenoir"][2])
    lenoirlblgust.config(text= "Gusts: " + wind_speed_dict['lenoir'][3] + " | " + wind_speed_dict["lenoir"][4] + " | " + wind_speed_dict["lenoir"][5])
    if int(wind_speed_dict["lenoir"][3]) >= 35 or int(wind_speed_dict["lenoir"][4]) >= 35:
        lenoir.config(bg='red')
        lenoirlbl.config(bg='red')
        lenoirlblgust.config(bg='red')
        lenoirlblwind.config(bg='red')
    elif int(wind_speed_dict["lenoir"][0]) >= 30 or int(wind_speed_dict["lenoir"][1]) >= 30:
        lenoir.config(bg='red')
        lenoirlbl.config(bg='red')
        lenoirlblgust.config(bg='red')
        lenoirlblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["lenoir"][0]) <= 25) or (20 <= int(wind_speed_dict["lenoir"][1]) <= 25) or (20 <= int(wind_speed_dict["lenoir"][2]) <= 25):
        lenoir.config(bg='orange')
        lenoirlbl.config(bg='orange')
        lenoirlblgust.config(bg='orange')
        lenoirlblwind.config(bg='orange')
    else:
        lenoir.config(bg='green')
        lenoirlbl.config(bg='green')
        lenoirlblgust.config(bg='green')
        lenoirlblwind.config(bg='green')

    waynelblwind.config(text= "Wind: " + wind_speed_dict['wayne'][0] + " | " + wind_speed_dict["wayne"][1] + " | " + wind_speed_dict["wayne"][2])
    waynelblgust.config(text= "Gusts: " + wind_speed_dict['wayne'][3] + " | " + wind_speed_dict["wayne"][4] + " | " + wind_speed_dict["wayne"][5])
    if int(wind_speed_dict["wayne"][3]) >= 35 or int(wind_speed_dict["wayne"][4]) >= 35:
        wayne.config(bg='red')
        waynelbl.config(bg='red')
        waynelblgust.config(bg='red')
        waynelblwind.config(bg='red')
    elif int(wind_speed_dict["wayne"][0]) >= 30 or int(wind_speed_dict["wayne"][1]) >= 30:
        wayne.config(bg='red')
        waynelbl.config(bg='red')
        waynelblgust.config(bg='red')
        waynelblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["wayne"][0]) <= 25) or (20 <= int(wind_speed_dict["wayne"][1]) <= 25) or (20 <= int(wind_speed_dict["wayne"][2]) <= 25):
        wayne.config(bg='orange')
        waynelbl.config(bg='orange')
        waynelblgust.config(bg='orange')
        waynelblwind.config(bg='orange')
    else:
        wayne.config(bg='green')
        waynelbl.config(bg='green')
        waynelblgust.config(bg='green')
        waynelblwind.config(bg='green')
        
    greenelblwind.config(text= "Wind: " + wind_speed_dict['greene'][0] + " | " + wind_speed_dict["greene"][1] + " | " + wind_speed_dict["greene"][2])
    greenelblgust.config(text= "Gusts: " + wind_speed_dict['greene'][3] + " | " + wind_speed_dict["greene"][4] + " | " + wind_speed_dict["greene"][5])
    if int(wind_speed_dict["greene"][3]) >= 35 or int(wind_speed_dict["greene"][4]) >= 35:
        greene.config(bg='red')
        greenelbl.config(bg='red')
        greenelblgust.config(bg='red')
        greenelblwind.config(bg='red')
    elif int(wind_speed_dict["greene"][0]) >= 30 or int(wind_speed_dict["greene"][1]) >= 30:
        greene.config(bg='red')
        greenelbl.config(bg='red')
        greenelblgust.config(bg='red')
        greenelblwind.config(bg='red')
    elif (20 <= int(wind_speed_dict["greene"][0]) <= 25) or (20 <= int(wind_speed_dict["greene"][1]) <= 25) or (20 <= int(wind_speed_dict["greene"][2]) <= 25):
        greene.config(bg='orange')
        greenelbl.config(bg='orange')
        greenelblgust.config(bg='orange')
        greenelblwind.config(bg='orange')
    else:
        greene.config(bg='green')
        greenelbl.config(bg='green')
        greenelblgust.config(bg='green')
        greenelblwind.config(bg='green')


def get_data_then_update_gui():
    for state, county in counties:
        get_wind_speed(state, county)

    update_gui()
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

lee = LabelFrame(root)
lee.place(x=900, y=400)
leelbl = Label(lee, text= "Lee")
leelbl.grid(column=0, row= 0, columnspan= 3)
leelblwind = Label(lee, text= "Wind: ")
leelblwind.grid(column=0, row=1)
leelblgust = Label(lee, text= "Gusts: ")
leelblgust.grid(column= 0, row= 2)

anderson = LabelFrame(root)
anderson.place(x=500, y=300)
andersonlbl = Label(anderson, text= "Anderson")
andersonlbl.grid(column=0, row= 0, columnspan= 3)
andersonlblwind = Label(anderson, text= "Wind: ")
andersonlblwind.grid(column=0, row=1)
andersonlblgust = Label(anderson, text= "Gusts: ")
andersonlblgust.grid(column= 0, row= 2)

bulloch = LabelFrame(root)
bulloch.place(x=700, y=700)
bullochlbl = Label(bulloch, text= "Bulloch")
bullochlbl.grid(column=0, row= 0, columnspan= 3)
bullochlblwind = Label(bulloch, text= "Wind: ")
bullochlblwind.grid(column=0, row=1)
bullochlblgust = Label(bulloch, text= "Gusts: ")
bullochlblgust.grid(column= 0, row= 2)

upson = LabelFrame(root)
upson.place(x=200, y=600)
upsonlbl = Label(upson, text= "Upson")
upsonlbl.grid(column=0, row= 0, columnspan= 3)
upsonlblwind = Label(upson, text= "Wind: ")
upsonlblwind.grid(column=0, row=1)
upsonlblgust = Label(upson, text= "Gusts: ")
upsonlblgust.grid(column= 0, row= 2)

richmond = LabelFrame(root)
richmond.place(x=650, y=580)
richmondlbl = Label(richmond, text= "Richmond")
richmondlbl.grid(column=0, row= 0, columnspan= 3)
richmondlblwind = Label(richmond, text= "Wind: ")
richmondlblwind.grid(column=0, row=1)
richmondlblgust = Label(richmond, text= "Gusts: ")
richmondlblgust.grid(column= 0, row= 2)

allendale = LabelFrame(root)
allendale.place(x=800, y=600)
allendalelbl = Label(allendale, text= "Allendale")
allendalelbl.grid(column=0, row= 0, columnspan= 3)
allendalelblwind = Label(allendale, text= "Wind: ")
allendalelblwind.grid(column=0, row=1)
allendalelblgust = Label(allendale, text= "Gusts: ")
allendalelblgust.grid(column= 0, row= 2)

williamsburg = LabelFrame(root)
williamsburg.place(x=1050, y=480)
williamsburglbl = Label(williamsburg, text= "Williamsburg")
williamsburglbl.grid(column=0, row= 0, columnspan= 3)
williamsburglblwind = Label(williamsburg, text= "Wind: ")
williamsburglblwind.grid(column=0, row=1)
williamsburglblgust = Label(williamsburg, text= "Gusts: ")
williamsburglblgust.grid(column= 0, row= 2)

chesterfield = LabelFrame(root)
chesterfield.place(x=1000, y=300)
chesterfieldlbl = Label(chesterfield, text= "Chesterfield")
chesterfieldlbl.grid(column=0, row= 0, columnspan= 3)
chesterfieldlblwind = Label(chesterfield, text= "Wind: ")
chesterfieldlblwind.grid(column=0, row=1)
chesterfieldlblgust = Label(chesterfield, text= "Gusts: ")
chesterfieldlblgust.grid(column= 0, row= 2)

marlboro = LabelFrame(root)
marlboro.place(x=1100, y=350)
marlborolbl = Label(marlboro, text= "Marlboro")
marlborolbl.grid(column=0, row= 0, columnspan= 3)
marlborolblwind = Label(marlboro, text= "Wind: ")
marlborolblwind.grid(column=0, row=1)
marlborolblgust = Label(marlboro, text= "Gusts: ")
marlborolblgust.grid(column= 0, row= 2)

darlington = LabelFrame(root)
darlington.place(x=1000, y=400)
darlingtonlbl = Label(darlington, text= "Darlington")
darlingtonlbl.grid(column=0, row= 0, columnspan= 3)
darlingtonlblwind = Label(darlington, text= "Wind: ")
darlingtonlblwind.grid(column=0, row=1)
darlingtonlblgust = Label(darlington, text= "Gusts: ")
darlingtonlblgust.grid(column= 0, row= 2)

dillon = LabelFrame(root)
dillon.place(x=1190, y=390)
dillonlbl = Label(dillon, text= "Dillon")
dillonlbl.grid(column=0, row= 0, columnspan= 3)
dillonlblwind = Label(dillon, text= "Wind: ")
dillonlblwind.grid(column=0, row=1)
dillonlblgust = Label(dillon, text= "Gusts: ")
dillonlblgust.grid(column= 0, row= 2)

marion = LabelFrame(root)
marion.place(x=1200, y=460)
marionlbl = Label(marion, text= "Marion")
marionlbl.grid(column=0, row= 0, columnspan= 3)
marionlblwind = Label(marion, text= "Wind: ")
marionlblwind.grid(column=0, row=1)
marionlblgust = Label(marion, text= "Gusts: ")
marionlblgust.grid(column= 0, row= 2)

edgecombe = LabelFrame(root)
edgecombe.place(x=1500, y=50)
edgecombelbl = Label(edgecombe, text= "Edgecombe")
edgecombelbl.grid(column=0, row= 0, columnspan= 3)
edgecombelblwind = Label(edgecombe, text= "Wind: ")
edgecombelblwind.grid(column=0, row=1)
edgecombelblgust = Label(edgecombe, text= "Gusts: ")
edgecombelblgust.grid(column= 0, row= 2)

guilford = LabelFrame(root)
guilford.place(x=1060, y=100)
guilfordlbl = Label(guilford, text= "Guilford")
guilfordlbl.grid(column=0, row= 0, columnspan= 3)
guilfordlblwind = Label(guilford, text= "Wind: ")
guilfordlblwind.grid(column=0, row=1)
guilfordlblgust = Label(guilford, text= "Gusts: ")
guilfordlblgust.grid(column= 0, row= 2)

randolph = LabelFrame(root)
randolph.place(x=1060, y=180)
randolphlbl = Label(randolph, text= "Randolph")
randolphlbl.grid(column=0, row= 0, columnspan= 3)
randolphlblwind = Label(randolph, text= "Wind: ")
randolphlblwind.grid(column=0, row=1)
randolphlblgust = Label(randolph, text= "Gusts: ")
randolphlblgust.grid(column= 0, row= 2)

scotland = LabelFrame(root)
scotland.place(x=1200, y=320)
scotlandlbl = Label(scotland, text= "Scotland")
scotlandlbl.grid(column=0, row= 0, columnspan= 3)
scotlandlblwind = Label(scotland, text= "Wind: ")
scotlandlblwind.grid(column=0, row=1)
scotlandlblgust = Label(scotland, text= "Gusts: ")
scotlandlblgust.grid(column= 0, row= 2)

hoke = LabelFrame(root)
hoke.place(x=1200, y=250)
hokelbl = Label(hoke, text= "Hoke")
hokelbl.grid(column=0, row= 0, columnspan= 3)
hokelblwind = Label(hoke, text= "Wind: ")
hokelblwind.grid(column=0, row=1)
hokelblgust = Label(hoke, text= "Gusts: ")
hokelblgust.grid(column= 0, row= 2)

robeson = LabelFrame(root)
robeson.place(x=1300, y=320)
robesonlbl = Label(robeson, text= "Robeson")
robesonlbl.grid(column=0, row= 0, columnspan= 3)
robesonlblwind = Label(robeson, text= "Wind: ")
robesonlblwind.grid(column=0, row=1)
robesonlblgust = Label(robeson, text= "Gusts: ")
robesonlblgust.grid(column= 0, row= 2)

sampson = LabelFrame(root)
sampson.place(x=1350, y=220)
sampsonlbl = Label(sampson, text= "Sampson")
sampsonlbl.grid(column=0, row= 0, columnspan= 3)
sampsonlblwind = Label(sampson, text= "Wind: ")
sampsonlblwind.grid(column=0, row=1)
sampsonlblgust = Label(sampson, text= "Gusts: ")
sampsonlblgust.grid(column= 0, row= 2)

surry = LabelFrame(root)
surry.place(x=900, y=20)
surrylbl = Label(surry, text= "Surry")
surrylbl.grid(column=0, row= 0, columnspan= 3)
surrylblwind = Label(surry, text= "Wind: ")
surrylblwind.grid(column=0, row=1)
surrylblgust = Label(surry, text= "Gusts: ")
surrylblgust.grid(column= 0, row= 2)

duplin = LabelFrame(root)
duplin.place(x=1450, y=220)
duplinlbl = Label(duplin, text= "Duplin")
duplinlbl.grid(column=0, row= 0, columnspan= 3)
duplinlblwind = Label(duplin, text= "Wind: ")
duplinlblwind.grid(column=0, row=1)
duplinlblgust = Label(duplin, text= "Gusts: ")
duplinlblgust.grid(column= 0, row= 2)

lenoir = LabelFrame(root)
lenoir.place(x=1550, y=250)
lenoirlbl = Label(lenoir, text= "Lenoir")
lenoirlbl.grid(column=0, row= 0, columnspan= 3)
lenoirlblwind = Label(lenoir, text= "Wind: ")
lenoirlblwind.grid(column=0, row=1)
lenoirlblgust = Label(lenoir, text= "Gusts: ")
lenoirlblgust.grid(column= 0, row= 2)

greene = LabelFrame(root)
greene.place(x=1550, y=150)
greenelbl = Label(greene, text= "Greene")
greenelbl.grid(column=0, row= 0, columnspan= 3)
greenelblwind = Label(greene, text= "Wind: ")
greenelblwind.grid(column=0, row=1)
greenelblgust = Label(greene, text= "Gusts: ")
greenelblgust.grid(column= 0, row= 2)

wayne = LabelFrame(root)
wayne.place(x=1450, y=150)
waynelbl = Label(wayne, text= "Wayne")
waynelbl.grid(column=0, row= 0, columnspan= 3)
waynelblwind = Label(wayne, text= "Wind: ")
waynelblwind.grid(column=0, row=1)
waynelblgust = Label(wayne, text= "Gusts: ")
waynelblgust.grid(column= 0, row= 2)


def legend_notes():
    messagebox.showinfo(parent=legend, title= "Legend Notes", message="""Column 1: Represents the Current time block; Morning, Afternoon, Night; of the Current day
Column 2: Represents the Next time block; Afternoon, Night, Morning of the next day if Column 1 is Night
Column 3: Represents the Morning of the next day unless Column 1 is Night, then it is Afternoon of the next Day
Data Pulled From:
https://wind.willyweather.com/""")



legend = LabelFrame(root)
legend.place(x=1600, y=350)
legendtitle = Label(legend, text="Legend | Units in Mph | 1 = No Value Found\nRed = Stow Site | Orange = Stow Almost Required")
legendtitle.pack()
legend1 = Button(legend, text="Learn What Time the Columns Represent", command=legend_notes, bg='light green')
legend1.pack(fill='x')

NCLabel = Label(legend, text="NC", font=("TkDefaultFont", 11, 'bold'))
NCLabel.pack(anchor=W)

#NC
sites_in_surry = Label(legend, text="Surry: Hayes")
sites_in_guilford = Label(legend, text="Guilford: Washington")
sites_in_randolph = Label(legend, text="Randolph: Thunderhead")
sites_in_hoke = Label(legend, text="Hoke: Elk")
sites_in_scotland = Label(legend, text="Scotland: McLean")
sites_in_robeson = Label(legend, text="Robeson: Holly Swamp, Gray Fox")
sites_in_sampson = Label(legend, text="Sampson: Van Buren")
sites_in_duplin = Label(legend, text="Duplin: Hickory")
sites_in_wayne = Label(legend, text="Wayne: PG")
sites_in_edgecombe = Label(legend, text="Edgecombe: Conetoe")
sites_in_greene = Label(legend, text="Greene: Harding")
sites_in_lenoir = Label(legend, text="Lenoir: Freight Line")
sites_in_duplin.pack(anchor=W)
sites_in_edgecombe.pack(anchor=W)
sites_in_greene.pack(anchor=W)
sites_in_guilford.pack(anchor=W)
sites_in_hoke.pack(anchor=W)
sites_in_lenoir.pack(anchor=W)
sites_in_randolph.pack(anchor=W)
sites_in_robeson.pack(anchor=W)
sites_in_sampson.pack(anchor=W)
sites_in_scotland.pack(anchor=W)
sites_in_surry.pack(anchor=W)
sites_in_wayne.pack(anchor=W)

SCLabel = Label(legend, text="SC", font=("TkDefaultFont", 11, 'bold'))
SCLabel.pack(anchor=W)
#SC
sites_in_anderson = Label(legend, text="Anderson: Bluebird")
sites_in_chesterfield = Label(legend, text="Chesterfield: Ogburn, Shorthorn")
sites_in_marlboro = Label(legend, text="Marlboro: Hickson")
sites_in_lee = Label(legend, text="Lee: Bishopville II")
sites_in_allendale = Label(legend, text="Allendale: Lily")
sites_in_williamsburg = Label(legend, text="Williamsburg: Sunflower, Cherry Blossom")
sites_in_marion = Label(legend, text="Marion: Cardinal")
sites_in_dillon = Label(legend, text="Dillon: Whitetail")
sites_in_darlington = Label(legend, text="Darlington: Marshall, Tedder, Jefferson, Whitehall")
sites_in_allendale.pack(anchor=W)
sites_in_anderson.pack(anchor=W)
sites_in_chesterfield.pack(anchor=W)
sites_in_darlington.pack(anchor=W)
sites_in_dillon.pack(anchor=W)
sites_in_lee.pack(anchor=W)
sites_in_marion.pack(anchor=W)
sites_in_marlboro.pack(anchor=W)
sites_in_williamsburg.pack(anchor=W)

GALabel =Label(legend, text="GA", font=("TkDefaultFont", 11, 'bold'))
GALabel.pack(anchor=W)
#GA
sites_in_upson = Label(legend, text="Upson: Upson")
sites_in_richmond = Label(legend, text="Richmond: Richmond")
sites_in_bulloch = Label(legend, text="Bulloch: Bulloch 1A, Bulloch 1B")
sites_in_bulloch.pack(anchor=W)
sites_in_richmond.pack(anchor=W)
sites_in_upson.pack(anchor=W)

#TimeStamps
updated = Label(legend, text= "Time Stamps Displayed Here")
updated.pack()

#Update Button
update_butt = Button(legend, text="Update Wind Data Now", command= lambda: get_data_then_update_gui(), bg='light green')
update_butt.pack(fill="x", expand=True)



get_data_then_update_gui()  
root.mainloop()
  






