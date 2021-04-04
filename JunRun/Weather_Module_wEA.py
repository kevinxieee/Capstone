import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime
import time
import weather_scraper

def getData():
    # # run weather_scraper.py to fetch new weather data
    # weather_scraper.getData()

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

    WMST = 0.003499 

    ## x[0:48] = PCEA
    ## x[48:96] = ESB

    start_time = time.time()

    # Constraints to ensure that ESB falls within limits
    def constraint1(x):
        for i in range(48):
            if (i == 0):
                x[48] = 0
            else:
                x[48+i] = x[48+i-1] + x[i]
        return x[0:48] + x[48:96]
        
    def constraint2(x):
        for i in range(48):
            if (i == 0):
                x[48] = 0
            else:
                x[48+i] = x[48+i-1] + x[i]
        return 10000 - (x[0:48]+ x[48:96])
    

    power = ((-5000, 5000),) * 48
    storage = ((0, 10000),) * 48

    #Objective
    def MEC(x):           #      (    PDLL             +             PCEA     )          x        HOEP
        return sum(sum( (load_sched + np.array([x[0:48]])) * (np.array(hoep_data)+WMST) ))

    x0 = np.array([np.ones(48), np.ones(48)])

    bounds = (power + storage)
    cons1 = {'type': 'ineq', 'fun': constraint1}
    cons2 = {'type': 'ineq', 'fun': constraint2}

    cons = ([cons1, cons2])

    sol = minimize(MEC, x0, method='SLSQP',bounds=bounds,constraints=cons,options= {'maxiter':150,'disp':True})

    input_var = {"EA_w_bill": sol.fun}

    return input_var
