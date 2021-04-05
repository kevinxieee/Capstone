import numpy as np
import pandas as pd


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

    load_data = pd.read_excel('load_data.xlsx', index_col=0, engine = 'openpyxl')

    # Monthly Bill 
    WMST = 0.003499             ## $/kWh 
    KDC = 0.43

    ## y = bimonthly cost
    ## x = hourly cost


    x = load_data.to_numpy() * (data_6months.to_numpy()+WMST)

    y = []

    for i in range(6): 
        mec = 60*sum(x[:,i])
        mdc = KDC*60*np.amax(load_data.iloc[:,i].to_numpy())
        bill = mec + mdc
        y.append(bill)

    input_var = { "base_m_bill": y , "base_y_bill" : sum(y)}
    

    return input_var

