import numpy as np
import pandas as pd
import time
from scipy.optimize import minimize


data_6months = pd.read_excel("SampleWeatherData.xlsx", index_col=0, engine='openpyxl')
data_6months ['Month 1&2'] = data_6months ['Month 1&2'].apply(lambda x: (2.02887*x + 39.633)/100)
data_6months ['Month 3&4'] = data_6months ['Month 3&4'].apply(lambda x: (0.453122*x + 19.8276)/100)
data_6months ['Month 5&6'] = data_6months ['Month 5&6'].apply(lambda x: (1.13665*x - 11.0085)/100)
data_6months ['Month 7&8'] = data_6months ['Month 7&8'].apply(lambda x: (1.90245*x - 23.2826)/100)
data_6months ['Month 9&10'] = data_6months ['Month 9&10'].apply(lambda x: (1.39145*x - 8.97971)/100)
data_6months ['Month 11&12'] = data_6months ['Month 11&12'].apply(lambda x: (1.72767*x + 21.3536)/100)

load_data = pd.read_excel('load_data.xlsx', index_col=0, engine = 'openpyxl')

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

## x[0:24] = PCEA
## x[24:48] = ESB
## x[48:72] = PCDDR
start_time = time.time()
def constraint1(x):
    for i in range(24):
        if (i == 0):
            x[24] = 0
        else:
            x[24+i] = x[24+i-1] + x[i] - x[48+i-1]
    return x[0:24] + x[24:48] - x[48:72]
    
def constraint2(x):
    for i in range(24):
        if (i == 0):
            x[24] = 0
        else:
            x[24+i] = x[24+i-1] + x[i] - x[48+i-1]
    return ESB - (x[0:24]+ x[24:48] - x[48:72])

def constraint4(x): 
    return 5000 - (abs(x[0:24]) + abs(x[48:72]))

def constraint3(x):
    NC = 0 
    for i in range(24):
        if (i == 0): 
            NC = NC + 0
        else:
            if ((x[24+i] - x[24+i-1]) >= 0):
                NC = NC + (x[24+i] - x[24+i-1])
            else: 
                NC = NC + 0
                
    return KNC - NC/ESB*30

power = ((-PSB, PSB),) * 24
storage = ((0, ESB),) * 24
DDR = ((0,PSB),) * 24

##Objective function
            #       Profits                 
def MEC(x):# - ( KPDDR*30*sum(PCDDR) )                  -       30*sum(load_data+PCEA) x (HOEP+WMST)                -               KDC*30*max(load_data+PCEA) )
    return -( \
        KPDDR*sum(30*(sum(np.array([x[48:72]])))) - \
        sum(30*sum((load_data.iloc[:,month].to_numpy() + np.array([x[0:24]])) * (data_6months.iloc[:,month].to_numpy() + WMST))) - 30*KDC*np.amax(load_data.iloc[:,month].to_numpy() + np.array([x[0:24]])) )


x0 = np.array([np.ones(24), np.ones(24), np.ones(24)])
bounds = (power + storage + DDR)
cons1 = {'type': 'ineq', 'fun': constraint1}
cons2 = {'type': 'ineq', 'fun': constraint2}
cons3 = {'type': 'ineq', 'fun': constraint3}
cons4 = {'type': 'ineq', 'fun': constraint4}
cons = ([cons1, cons2, cons3,cons4])

pcea_solutions = []
esb_solutions = []
ddr_solutions = []

mec = 0 

for month in range(6):
    sol = minimize(MEC, x0, method='SLSQP',
                     bounds=bounds,
                     constraints=cons,
                     options= {'maxiter':150,'disp':True})
    mec = mec + sol.fun
    pcea_solutions.append(sol.x[0:24])
    esb_solutions.append(sol.x[24:48])
    ddr_solutions.append(sol.x[48:72])
      

print(-2*mec)
print("--- %s seconds ---" % (time.time() - start_time))