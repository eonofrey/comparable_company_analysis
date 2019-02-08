# Imports
import quandl
import pandas as pd
import time 
import intrinio

# API Configurations
intrinio.client.username = '0e8670f499ca25b3b2c36027d6525fcd'
intrinio.client.password = 'd327439a8e0fe9075ccb52b63c0dfc3f'
quandl.ApiConfig.api_key = "1LnvXD6vks1cyTrzKz8b"

# Pull in a list of tickers 
tickers = pd.read_csv("/Users/Eric/Desktop/cis192_proj/tickers.csv", header=None, names = ["ticker", "company_name"])

# Cleaning
tickers['ticker'] = tickers['ticker'].str.replace('WIKI/','')
f = lambda x: x["company_name"].split(r" (")[0]
tickers['company_name'] = tickers.apply(f, axis=1)

# Create dictionary
company_dict = {'name': 'example',
                'ticker': 'EX',
                'revenue': '123',
                'assets': '123',}

# Create dataframe to be appended
company_df = pd.DataFrame(company_dict, index=[0])

# Loop over tickers, grab revenue and assets from Quandl
for name,ticker in list(zip(tickers['company_name'], tickers['ticker']))[2000:3198]: 
    try:
        # Gather data from API
        revenue = quandl.get(("SF0/" + ticker + "_REVENUE_MRY")).values[-1][0] #most recent revenue
        time.sleep(.1)

        assets = quandl.get("SF0/" + ticker + "_ASSETS_MRY").values[-1][0] #total assets
        time.sleep(.1)
        
        # Add data to a dictionary 
        company_dict['name'] = name
        company_dict['ticker'] = ticker
        company_dict['revenue'] = revenue
        company_dict['assets'] = assets

        # Append dicitonary to dataframe 
        company_df = company_df.append(company_dict, ignore_index=True)
        print("got" + ticker)
        
    except: 
        print ("couldn't get " + ticker)
