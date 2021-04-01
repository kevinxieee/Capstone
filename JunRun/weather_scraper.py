## Weather Scraper 
#   Sourced from Weather.com
import requests
from bs4 import BeautifulSoup
import pandas as pd
import csv

def getData():
    file = requests.get("https://weather.com/en-CA/weather/hourbyhour/l/62e0efebee1ac0e8fa9b21fd17d57a6a0001753ab6be8a4874bb78bbb52eda02")

    soup = BeautifulSoup(file.content, "html.parser")

    list = []

    for mess in soup.find_all("div", {"class":"DaypartDetails--DetailSummaryContent--1c28m Disclosure--SummaryDefault--1z_mF"}):

        try:

            time = mess.h2.text
            temp = mess.span.text
    
        except:

            time = None
            temp = None

        list.append([time,temp])

    convert = pd.DataFrame(list)
    convert.columns= [ 'Hour', 'Temperature']
    convert['Temperature'] = convert['Temperature'].map(lambda x: x.rstrip('°'))

    convert.to_csv("weather_data.csv", line_terminator= '\n')
