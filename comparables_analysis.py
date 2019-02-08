# Imports
import pandas as pd
import numpy as np
from heapq import nsmallest
import matplotlib.pyplot as plt

# Pull in data
intrinio_df = pd.read_csv("intrinio_pull_total.csv")
intrinio_df = intrinio_df[['enterprise_value', 'sector', 'ticker']]
quandl_df = pd.read_csv("quandl_pull_total.csv")

# Merge, Reorder, Drop NaNs, Drop Example 
data = quandl_df.merge(intrinio_df, on='ticker')
data = data[['ticker', 'name', 'enterprise_value', 'assets', 'revenue', 'sector']]
data = data.dropna(axis=0, how='any')
data = data[data['enterprise_value'] > 1]
data = data[data['revenue'] > 1]

# Company class
class Company: 
    
    def __init__(self, ticker, name, ev, assets, revenue, sector):
        self.ticker = ticker
        self.name = name
        self.ev = ev
        self.assets = assets
        self.revenue = revenue
        self.sector = sector
    
    def __str__(self):
        return self.name
    
    
    # Find comparable companies based on revenue
    def get_comparables(self, df, n=5):
        if 'sector' not in df.columns.values: 
            return ("Dataframe needs to have a column labled sector")
        if 'revenue' not in df.columns.values: 
            return ("Dataframe needs to have a column labled revenue")
        if n < 1: 
            return ("n needs to be greater than 1")        
       
        # Get subset of this company's sector
        sector_data = df[df['sector'] == self.sector]
        sector_rev = sector_data['revenue']
        
        # Find the closest revenues to it
        comps = nsmallest(n+1, sector_rev, key=lambda x: abs(x-self.revenue))
        
        # Create dataframe, merge, remove the company from its comparables
        comps = pd.DataFrame(comps, columns=['revenue'])
        combo = df.merge(comps, on=['revenue'])
        combo = combo[combo['ticker'] != self.ticker]
        
        # Return that dataframe
        return combo
    
    # Use comparables to get a valuation
    def get_ccv(self, df, n):
        comps = self.get_comparables(df, n)
        ccv = np.mean(comps['enterprise_value'])
        return ccv


# Add CCV estimates to dataframe 
pred_df = pd.read_csv("predictions.csv")
pred_df.head()

# Create dictionary
new_dict = {'name': '',
            'cvv predicted': '123',}

# Create dataframe to be appended to
new_df = pd.DataFrame(new_dict, index=[0])


# Loop over companies, create a Company class, get the 
# comparables estimate 
for i in range(pred_df.shape[0]): 
   
    # Craete the Company object
    curr_company = Company(pred_df['ticker'][i], 
                            pred_df['name'][i], 
                            pred_df['actual ev'][i], 
                            pred_df['assets'][i], 
                            pred_df['revenue'][i], 
                            pred_df['sector'][i])
    
    # Get the name of the company 
    new_dict['name'] = str(curr_company)
    
    # Get the comparables estimate
    new_dict['cvv predicted'] = curr_company.get_ccv(data, 5)

    # Append to the dataframe 
    new_df = new_df.append(new_dict, ignore_index=True)

# Data check
new_df.head()

# Merge the comparables estimates onto the predictions dataframe
all_predictions = pred_df.merge(new_df, on=['name'])
all_predictions.head()

# Get get the predicted enterprise values
lm = all_predictions['lm predicted']
rf = all_predictions['rf predicted']
actual = all_predictions['actual ev']
cvv = all_predictions['cvv predicted']

# Find the absoute error 
lm_error = np.mean(abs(actual-lm)/abs(actual)) * 100
rf_error = np.mean(abs(actual-rf)/abs(actual)) * 100
ccv_error = np.mean(abs(actual-cvv)/abs(actual)) * 100

# Create dataframe for outputting errors
d = {'Model': ['Comparables', 'Regression', 'Random Forest'], 
         'Error': [ccv_error, lm_error, rf_error]}
df = pd.DataFrame(data=d)
df = df[['Model', 'Error']]

# Create plot for visualizing errors
models = ('Comparables', 'Regression', 'Random Forest')
y_pos = np.arange(len(models))
errors = [ccv_error, lm_error, rf_error]

# Get fig and ax
fig, ax = plt.subplots()    
    
# Aesthetics
plt.bar(y_pos, errors, align='center', alpha=0.5)
plt.xticks(y_pos, models)
plt.ylabel('Error (In Percentages)')
plt.title('Enerprise Value Prediction Errors')

# Output dataframe and plot
df
plt.show()
