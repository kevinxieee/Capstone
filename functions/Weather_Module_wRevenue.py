import numpy as np
import pandas as pd
from scipy.optimize import minimize
from datetime import datetime
import time
from functions import weather_scraper

def getData():
    # run weather_scraper.py to fetch new weather data
    # weather_scraper.getData()

    ## Read in csv file "weather_data.csv"
    weather_data = pd.read_csv("data/weather_data.csv")

    # Grab the current month & hour
    currentMonth = datetime.now().month
    currentHour = datetime.now().hour
    hours = weather_data.iloc[:,1].tolist()

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
    load_data = pd.read_excel('data/load_data.xlsx', index_col=0, engine = 'openpyxl')

    # Create loading schedule based on current time of day and month
    load_sched = np.arange(48)

    for i in range(len(temp)):
        load_sched[i] = load_data.iloc[ weather_data.iloc[i,1] , currentMonthGroup]

    ## Initialize all constants

    ESB = 10000
    PSB = 5000

    # Revenue
    KPDDR = 1200.264/8720       ## $856.436 /kW year

    # Monthly Bill 
    WMST = 0.003499             ## $/kWh 
    KDC = 0.43

    # Asset Costs
    KPB = 40
    PS = 5000 
    KEB = 500
    ES = 10000

    # Cycle Constraint
    KNC = 67

    ## x[0:48] = PCEA
    ## x[48:96] = ESB
    ## x[96:144] = PCDDR

    def constraint1(x):
        for i in range(48):
            if (i == 0):
                x[48] = 0
            else:
                x[48+i] = x[48+i-1] + x[i] - x[96+i-1]
        return x[0:48] + x[48:96] - x[96:144]
        
    def constraint2(x):
        for i in range(48):
            if (i == 0):
                x[48] = 0
            else:
                x[48+i] = x[48+i-1] + x[i] - x[96+i-1]
        return ESB - (x[0:48] + x[48:96] - x[96:144])

    def constraint3(x): 
        return 5000 - (abs(x[0:48]) + abs(x[96:144]))


    power = ((-PSB, PSB),) * 48
    storage = ((0, ESB),) * 48
    DDR = ((0,PSB),) * 48

    ##Objective function                
    def MEC(x):
        return -( sum(  sum(KPDDR*np.array([x[96:144]])) - sum( (load_sched + np.array([x[0:48]])) * (np.array(hoep_data)+WMST) ) ) )

    x0 = np.ones(144)
    bounds = (power + storage + DDR)
    cons1 = {'type': 'ineq', 'fun': constraint1}
    cons2 = {'type': 'ineq', 'fun': constraint2}
    cons3 = {'type': 'ineq', 'fun': constraint3}
    cons = ([cons1, cons2, cons3])

    pcea_solutions = []
    esb_solutions = []
    ddr_solutions = []



    sol = minimize(MEC, x0, method='SLSQP', \
                        bounds=bounds, \
                        constraints=cons, \
                        options= {'maxiter':150,'disp':True})
    pcea_solutions.append(sol.x[0:48].tolist())
    esb_solutions.append(sol.x[48:96].tolist())
    ddr_solutions.append(sol.x[96:144].tolist())

    input_var = {"Hour": hours, "pcea": pcea_solutions, "esb": esb_solutions, "ddr": ddr_solutions,  "ddr_w_bill": sol.fun}

    return input_var




