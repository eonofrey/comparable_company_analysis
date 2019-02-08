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
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
from sklearn import preprocessing

# Log transform 
data[['enterprise_value', 'assets', 'revenue']] = data[['enterprise_value', 'assets', 'revenue']].apply(np.log)

# Get dummy variables
dummies = pd.get_dummies(data['sector'])
encoded_data = data[['enterprise_value', 'assets', 'revenue']].join(dummies)

# Split into explanatory and response 
X_data = encoded_data.iloc[:,1:].values
y_data = encoded_data['enterprise_value'].values

# Split into training and testing
X_train, X_test, y_train, y_test = train_test_split(X_data, y_data, test_size=0.25, random_state=619)
X_train.shape, X_test.shape
y_train.shape, y_test.shape

# Fit Linear Model
lm = linear_model.LinearRegression()
lm.fit(X_train, y_train)

# Fit Random Forest
rf = RandomForestRegressor(max_depth=3, random_state=619)
rf.fit(X_train, y_train)

# Make predictions 
lm_predictions = lm.predict(X_test) 
rf_predictions = rf.predict(X_test)

# Exponentiate
exp_lm_predictions = np.exp(lm_predictions)
exp_rf_predictions = np.exp(rf_predictions)
exp_actual = np.exp(y_test)

# Predictions 
test = pd.DataFrame(X_test, columns=['assets', 'revenue', 'Basic Materials', 
                                    'Congolomerates', 'Consumer Goods', 'Financial', 'Healthcare',
                                    'Industrial Goods', 'Services', 'Technology', 'Utilities'])

# Get the predicitons from the regression and the random forest and real ev's
lm_pred = pd.DataFrame(exp_lm_predictions, columns = ['lm predicted'])
rf_pred = pd.DataFrame(exp_rf_predictions, columns = ['rf predicted'])
actual = pd.DataFrame(exp_actual, columns=['actual ev'])

# Join all together, add the names and tickers back in
pred_df = test.join(lm_pred).join(rf_pred).join(actual)
pred_df = pred_df.merge(data[['assets', 'revenue','ticker', 'name', 'sector']], on= ['assets', 'revenue'])

# Exponentiate the logged values
pred_df['assets'] = np.exp(test['assets'])
pred_df['revenue'] = np.exp(test['revenue'])

# Reorder
pred_df = pred_df[['name', 'ticker', 'assets', 'revenue', 'sector', 'lm predicted', 'rf predicted', 'actual ev']]

# Drop NaN's
pred_df = pred_df.dropna(axis=0, how='any')

# Data sanity check
pred_df.head()
pred_df.shape

# Ouptput to .csv
pred_df.to_csv("predictions.csv", index=False)
