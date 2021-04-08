import numpy as np
import pandas as pd


from scipy.optimize import minimize

def getData(yyyy):
    if int(yyyy) == 2018 :
        df = pd.read_csv("http://reports.ieso.ca/public/PriceHOEPPredispOR/PUB_PriceHOEPPredispOR_2018.csv").fillna(0)
    elif int(yyyy) == 2019:
        df = pd.read_csv("http://reports.ieso.ca/public/PriceHOEPPredispOR/PUB_PriceHOEPPredispOR_2019.csv").fillna(0)
    elif int(yyyy) == 2020:
        df = pd.read_csv("http://reports.ieso.ca/public/PriceHOEPPredispOR/PUB_PriceHOEPPredispOR_2020.csv").fillna(0)

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

    hoep_data_6months = pd.DataFrame()

    load_data = pd.read_excel('data/load_data.xlsx', index_col=0, engine="openpyxl")

    for i in range(0, 12, 2):
        hoep_data_6months[data.columns[i] + ' & ' + data.columns[i+1]] = (data[data.columns[i]] + data[data.columns[i+1]])/2

    ## Initialize all constants

    ESB = 10000
    PSB = 5000

    # Monthly Bill 
    WMST = 0.003499             ## $/kWh 
    KDC = 0.43

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
                x[24+i] = x[24+i-1] + x[i]
        return x[0:24] + x[24:48]
        
    def constraint2(x):
        for i in range(24):
            if (i == 0):
                x[24] = 0
            else:
                x[24+i] = x[24+i-1] + x[i]
        return 10000 - (x[0:24]+ x[24:48])

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


    ##Objective
    def MEC(x):           #      (    PDLL             +             PCEA     )          x        HOEP
        return sum(30*sum((load_data.iloc[:,month].to_numpy() + np.array([x[0:24]])) * (hoep_data_6months.iloc[:,month].to_numpy()+WMST))) + 30*KDC*np.amax(load_data.iloc[:,month].to_numpy() + np.array([x[0:24]]))

    x0 = np.ones(48)
    bounds = (power + storage)
    cons1 = {'type': 'ineq', 'fun': constraint1}
    cons2 = {'type': 'ineq', 'fun': constraint2}
    cons3 = {'type': 'ineq', 'fun': constraint3}

    cons = ([cons1, cons2, cons3])

    # y = bimonthly cost

    y = []

    for month in range(6):
        sol = minimize(MEC, x0, method='SLSQP',bounds=bounds,constraints=cons,options= {'maxiter':150,'disp':True})
        y.append(2*sol.fun)

    y_round = [round(num,2) for num in y]

    input_var = { "EA_m_bill": y_round , "EA_y_bill" : round(sum(y),2) }
    

    return input_var

