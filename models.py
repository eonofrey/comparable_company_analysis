# Imports 
import pandas as pd
import sklearn
import seaborn as sns
import numpy as np
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

# Shuffle rows 
data = data.sample(frac=1).reset_index(drop=True)

# Data check 
data.head()
data.describe()
data.sort_values(by=['enterprise_value'], ascending=False).head()

# Decorator and plotting functions
def hist_wrapper(func):
    def new_hist(self, name):
        fig, ax = func(self)
        plt.xlabel(name)
        plt.ylabel("Frequency")
        ax.set_facecolor('#F5F5F5')
        plt.title("Distribution of " + name)
        plt.show()
    return new_hist

@hist_wrapper
def plot_hist(series, name="default"):
    fig, ax = plt.subplots()
    sns.kdeplot(series, shade=True)
    return fig, ax
    
# Plots 
# Enterprise Value
plot_hist(data['enterprise_value'], name="Enterprise Value")

# Assets
plot_hist(data['assets'], name="Assets")

# Revenue 
plot_hist(data['revenue'], name="Revenue")

# Plots of logged data
@hist_wrapper
def plot_log_hist(series, name="default"):
    fig, ax = plt.subplots()
    sns.kdeplot(series.apply(np.log), shade=True)
    return fig, ax
    
    
# Enterprise Value
plot_log_hist(data['enterprise_value'], name="Log Enterprise Value")

# Assets
plot_log_hist(data['assets'], name="Log Assets")

# Revenue 
plot_log_hist(data['revenue'], name="Log Revenue")



############# Models #############
