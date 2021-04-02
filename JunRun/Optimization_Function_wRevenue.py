import numpy as np
import pandas as pd
import time
from scipy.optimize import minimize

def getData():
    ## Read in csv file from IESO website, ***fill blank entries with 0*** (temp)
    df = pd.read_csv("http://reports.ieso.ca/public/PriceHOEPPredispOR/PUB_PriceHOEPPredispOR_2019.csv").fillna(0)

    df.rename(columns=df.iloc[2], inplace=True)         ## Set headers to the proper ones row 4
    df = df[3:]
    df.reset_index(inplace=True, drop=True)             ## Reset indices to proper values

    #df.dropna(inplace=True)


    ## Convert columns to suitable data types
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.astype({'Hour':int, 'HOEP':float, 'Hour 1 Predispatch': float, 'Hour 2 Predispatch': float, 'Hour 3 Predispatch':float, 'OR 10 Min Sync':float, 'OR 10 Min non-sync':float, 'OR 30 Min':float})

    ## Split the date into year, month, day
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day
    df.drop(['Date'], axis=1, inplace=True)

    ## Rearrange them so they appear at the beginning (not necessary, only intermediate step for you to visualize)
    date = ['Year', 'Month', 'Day']
    df = df[date + [c for c in df if c not in date]]

    ## Create new dataframe for final data values
    data = pd.DataFrame()

    ## Iterate through the months of the year specified from CSV file
    ## and iterate through the hours to get monthly average for that specific hour
    for month in range(1,13):
        average = []
        df_month = df.loc[df['Month'] == month]

        for hour in range(1,25):
            h = df_month.loc[df['Hour'] == hour]
            average.append((h['HOEP'].sum()/h.shape[0])/100)  ## Cents to Dollars
        data['Month ' + str(month)] = average

    ## Set index to proper hours
    data.index = range(1, len(data)+1)
    data.index.name = 'Hour'


    data_6months = pd.DataFrame()
    for i in range(0, 12, 2):
        data_6months[data.columns[i] + ' & ' + data.columns[i+1]] = (data[data.columns[i]] + data[data.columns[i+1]])/2

    load_data = pd.read_excel('load_data.xlsx', index_col=0, engine='openpyxl')

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
    def MEC(x):           #      KPDDR*PCDDR - (PCEA+PDLL)*(HOEP + WMST) - PDF*(GAC+CBR) - KDC*max(PDLL+PCEA)
        return -(\
            #Revenue\
            KPDDR*sum(30*(sum(np.array([x[48:72]])))) - \
            #Costs\
                #MEC\
                sum(30*sum((load_data.iloc[:,month].to_numpy() + np.array([x[0:24]])) * \
                            (data_6months.iloc[:,month].to_numpy() + WMST))) - \
                #MDC\
                #30*KDC*(PDLL + PCEA)\
                30*KDC*np.amax(load_data.iloc[:,month].to_numpy() + np.array([x[0:24]]))\
                )


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

    # y = bimonthly cost

    y = []

    columns = ["Months 1&2", "Months 3&4", "Months 4&5", "Months 7&8", "Months 9&10", "Months 11&12"]

    for month in range(6):
        sol = minimize(MEC, x0, method='SLSQP',\
                        bounds=bounds,\
                        constraints=cons,\
                        options= {'maxiter':150,'disp':True})
        y.append(sol.fun)
        pcea_solutions.append(sol.x[0:24].tolist())
        esb_solutions.append(sol.x[24:48].tolist())
        ddr_solutions.append(sol.x[48:72].tolist())

    input_var = {"columns": columns, "pcea": pcea_solutions, "esb": esb_solutions, "ddr": ddr_solutions,  "ddr_m_bill": y, "ddr_y_bill": sum(y) }

    return(input_var)
