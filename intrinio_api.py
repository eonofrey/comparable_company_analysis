import time 
import intrinio
import pandas as pd

intrinio.client.username = '0e8670f499ca25b3b2c36027d6525fcd'
intrinio.client.password = 'd327439a8e0fe9075ccb52b63c0dfc3f'

#intrinio.client.username = 'f70a596ff7217ac3f5d413d6309a8663'
#intrinio.client.password = '56b7d2fc92ca76ad2ad679a6b0fd5b62'

#intrinio.client.username = 'b802f91d4a66d954b8b90b1b23c7737b'
#intrinio.client.password = '14121fbd7cfa393232a58377253a63c2'

#intrinio.client.username = 'af43def02dfcd318128885e75c4bebe4'
#intrinio.client.password = '3da53c44e34b190b4b2ccad93ebe6a3a'

#intrinio.client.username = '9c807beaf94e3b86742054d58893c210'
#intrinio.client.password = '15484cd66fee74f0a60f7ef790d15168'

#intrinio.client.username = 'd8357c93a020b240a66933f9394c72df'
#intrinio.client.password = '816fec82465b99ee0346e7b00db1638e'

#intrinio.client.username = '2c168196a5f2befbf1b562523329ef2b'
#intrinio.client.password = '68cc12782d62c14dc719352cc2ce353a'

#intrinio.client.username = 'ca3d54e923e49d827ead1732c643b008'
#intrinio.client.password = '1b140ead6548a1d4af1447e50a12e3d1'

#intrinio.client.username = '8c6e35f1065729769d606312c5cc2215'
#intrinio.client.password = 'aac6cb38355910c7bdc934856f6a4561'

#intrinio.client.username = 'b17bfaf3168c39488351022ec8b91e09'
#intrinio.client.password = '0d409a13aa8a3591d6c2ed89ac8d0cb7'

#intrinio.client.username = '4c496f7a24565178dc7c25fe8de162eb'
#intrinio.client.password = '1788aea42649f1a29e42b175407dcd15'

# Pull in the data obtained from Quandl (revenue, assets, name, ticker)
quandl = pd.read_csv("quandl_pull_total.csv")
quandl.head()
quandl.shape

# Pull in data obtained from the last Intrinio loop
intrinio_df = pd.read_csv("intrinio_pull_total.csv")
intrinio_df.head()
intrinio_df.shape

# Loop over tickers, get their enterprise value and sector
# Create dictionary 
ev_dict = {'enterprise_value': '123',
                'ticker': 'EX',
                'sector': 'tech'}

# Create dataframe to be appended to 
ev_df = pd.DataFrame(ev_dict, index=[0])


# Loop over tickers and get enterprise value and sector
for ticker in quandl['ticker']:
    
    # Skip any tickers that we already have enterprise value and sector for
    if (ticker not in intrinio_df['ticker'].values):
        try:
            # Get data from API
            ev = intrinio.financials(ticker)['enterprisevalue'].values[-1]
            sector = intrinio.companies(ticker)['sector'].values[0]
 
            # Add it to the dictionary 
            ev_dict['enterprise_value'] = ev
            ev_dict['sector'] = sector
            ev_dict['ticker'] = ticker
            
            # Append to the dataframe 
            ev_df = ev_df.append(ev_dict, ignore_index=True)
            print ("got " + ticker)
        except: # Bad Style, should be a particular exception 
            print ("couldn't get " + ticker)

# Data check
ev_df.head()
ev_df.shape
intrinio_df.shape

# Add the data from this loop onto the master dataframe
combo = intrinio_df.append(ev_df)
combo.shape

# Export as a .csv
combo[['enterprise_value', 'sector', 'ticker']].to_csv("intrinio_pull_total.csv")
