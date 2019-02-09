# Comparable Company Analysis (Improved) 


#### Background

Comparable company analysis (CCA) is one of the most common valuation techniques in banking. This process attempts to estimate the enterprise value (market cap + debt + minority interest - cash) of a private company using the enterprise values of similar, public companies. Enteprise value is used to assess comany value in situations such as M&A advisory, fairness opinions, IPOs and restructuring.

The simplified steps to comparable company analysis are as follows: 

1. Select similar companies to your target to form your 'peer universe' or 'comparables universe'
2. Calculate the enterprise values for the companies in your comparables universe
3. Choose a ratio for this universe such as EV/Revenue or EV/EBITDA
4. Calculate the mean or median ratio of this universe
5. Multiply the mean or median ratio by the appropriate metric of your target company (Revenue or EBITDA usually) to get the enterprise value for your target company


#### Project Summary 

In this project, I attempt to predict enterprise value in a better way than comparable company analysis. I gather a company's name, stock ticker, assets, revenue, sector, and enterprise value from the Quandl and Intrinio APIs in the quandl_api and  and intrinio_api notebooks. From there, I clean and organize the data and run regression and random forest models in the models notebook in order to try and predict the enterprise value of a company. The models have the following form: 

Enterprise value ~ Assets + Revenue + Sector

After this is done I create the Company class in comparables_analysis.py which creates a Company object for each company in my dataset. I use this class to run a pseudo-comparables-analysis to compare my results from the regression and random forest against. 


#### Motivation
As someone who has conducted comparables analysis, I know the process can be improved. It's time consuming, entirely dependent on assumptions, and uses very few datapoints. The Securities Litigation and Consulting Group published a paper in 2011 in which they try to replace comparables analysis with a regression on only a company's EBITDA or revenue which piqued my interest. I try to further improve on their work by using more companies, more varaibles (assets and sector), and more models (random forest). 

## Project Walkthrough

#### 1. quandl_api.py

In this script I start with a list of tickers I downloaded from the internet. They come with a lot of unnecessary text so I had to clean it up before it was usable. 

<img width="390" alt="screen shot 2019-02-09 at 12 23 13 pm" src="https://user-images.githubusercontent.com/38504767/52523974-8408d080-2c65-11e9-81e0-1e3f9298689b.png"> <img width="200" alt="screen shot 2019-02-09 at 12 26 38 pm" src="https://user-images.githubusercontent.com/38504767/52524010-fd082800-2c65-11e9-9812-b5721353b6c3.png">
 <img width="249" alt="screen shot 2019-02-09 at 12 24 50 pm" src="https://user-images.githubusercontent.com/38504767/52523993-badee680-2c65-11e9-8c42-5b5b82c1a931.png">
 
Once I have this dataframe in the proper form, I loop through the tickers column and make calls to Quandl's API for the revenue and assets of each company. The result is shown below with some familiar companies (and my example row that was needed to start the loop).

<img width="440" alt="screen shot 2019-02-09 at 12 29 42 pm" src="https://user-images.githubusercontent.com/38504767/52524043-7869d980-2c66-11e9-8b5a-c0730cddf0fc.png">


#### 2. intrinio_api.py

For this script, I use Intrinio's API (and many, many keys for that API) to get the enterprise value and sector of each company in dataset. I used multiple API key's because Intrino limits daily requests for each key and 10-minute emails are very easy to create. In a process very similar to the one in quandl_api.py, I loop through the tickers in my dataframe and pull the appropriate data from the API. Below is an example of the final output of this script. 

<img width="269" alt="screen shot 2019-02-09 at 12 42 39 pm" src="https://user-images.githubusercontent.com/38504767/52524173-3cd00f00-2c68-11e9-9573-80db9da6a492.png">


#### 3. intrinio_api.py

<img width="711" alt="screen shot 2019-02-09 at 12 44 32 pm" src="https://user-images.githubusercontent.com/38504767/52524200-7dc82380-2c68-11e9-8226-cf122938f860.png">

Now I have a dataframe that is combined and cleaned (above). The final step before running models on it is to do a small amount of transformation. One of the assumptions of regression is that the independent variables are normally distributed. Plotting enterprise value, assets, and revenue shows that these variables have a heavy right skew. To fix this I log-transform them to get a more Gaussian distribution for each variable.

##### Pre-transformation
<img width="200" alt="screen shot 2019-02-09 at 12 46 11 pm" src="https://user-images.githubusercontent.com/38504767/52524230-cbdd2700-2c68-11e9-823a-b2dade3845a9.png"> <img width="200" alt="screen shot 2019-02-09 at 12 46 20 pm" src="https://user-images.githubusercontent.com/38504767/52524287-4f971380-2c69-11e9-8d32-0eb18c994668.png"> <img width="200" alt="screen shot 2019-02-09 at 12 46 26 pm" src="https://user-images.githubusercontent.com/38504767/52524291-62a9e380-2c69-11e9-8ec2-c86d396fb501.png">


##### Log Transformed 
<img width="200" alt="screen shot 2019-02-09 at 12 46 32 pm" src="https://user-images.githubusercontent.com/38504767/52524299-810fdf00-2c69-11e9-9751-7af3dd50dab0.png"> <img width="200" alt="screen shot 2019-02-09 at 12 46 37 pm" src="https://user-images.githubusercontent.com/38504767/52524305-8e2cce00-2c69-11e9-8921-59c0ce73a324.png"> <img width="200" alt="screen shot 2019-02-09 at 12 46 46 pm" src="https://user-images.githubusercontent.com/38504767/52524314-a56bbb80-2c69-11e9-80a4-2a4ed67d8d58.png">








