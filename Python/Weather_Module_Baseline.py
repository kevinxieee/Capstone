import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime

# run weather_scraper.py to fetch new weather data
import weather_scraper

## Read in csv file "weather_data.csv"
weather_data = pd.read_csv("weather_data.csv")

# Grab the current month & hour
currentMonth = datetime.now().month
currentHour = datetime.now().hour

# Determine which month group the current month is [0,5]
currentMonthGroup = currentMonth // 2

hoep_data = []
temp = weather_data.iloc[:,2]

# Change hour string to number from 0-23
for i in range(len(temp)): 
    weather_data.iloc[i,1] = (currentHour + i) % 24

# Convert temperature data to HOEP data
if (currentMonthGroup == 0) :
    hoep_data = temp.apply(lambda x: (2.02887*x + 39.633)/100)
elif (currentMonthGroup == 1):
    hoep_data = temp.apply(lambda x: (0.453122*x + 19.8276)/100)
elif (currentMonthGroup == 2):
    hoep_data = temp.apply(lambda x: (1.13665*x - 11.0085)/100)
elif (currentMonthGroup == 3):
    hoep_data = temp.apply(lambda x: (1.90245*x - 23.2826)/100)
elif (currentMonthGroup == 4): 
    hoep_data = temp.apply(lambda x: (1.39145*x - 8.97971)/100)
else:
    hoep_data = temp.apply(lambda x: (1.72767*x + 21.3536)/100)

# Load in the load_data
load_data = pd.read_excel('load_data.xlsx', index_col=0, engine = 'openpyxl')

# Create loading schedule based on current time of day and month
load_sched = np.arange(48)

for i in range(len(temp)):
    load_sched[i] = load_data.iloc[ weather_data.iloc[i,1] , currentMonthGroup]

# Initiate Constants
WMST = 0.003499             ## $/kWh 
KDC = 0.43

# Calculate costs

costs = np.multiply(load_sched, hoep_data+WMST)

print(sum(costs))

df_sol = pd.concat([weather_data.iloc[:,1], pd.DataFrame(costs) ], axis =1)
df_sol.columns = ['Hour', 'Hourly Cost']

df_sol.to_csv("Weather_Base.csv")
