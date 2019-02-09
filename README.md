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

<img width="390" alt="screen shot 2019-02-09 at 12 23 13 pm" src="https://user-images.githubusercontent.com/38504767/52523974-8408d080-2c65-11e9-81e0-1e3f9298689b.png"> <img width="249" alt="screen shot 2019-02-09 at 12 24 50 pm" src="https://user-images.githubusercontent.com/38504767/52523993-badee680-2c65-11e9-8c42-5b5b82c1a931.png">


