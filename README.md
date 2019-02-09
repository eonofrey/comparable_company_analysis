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

The data on over 1,400 companies that incldues their tickers, name, enterprise value, assets, revenue, and sector. I split the data into training and test samples, and train linear regression and random foreset models on the training data. I use these models to predict the enterprise value of the companies in the test sample. Below is a screenshot of what my predictions dataframe looks like. 

<img width="650" alt="screen shot 2019-02-09 at 12 55 31 pm" src="https://user-images.githubusercontent.com/38504767/52524401-8b7ea880-2c6a-11e9-8245-dc78b5ac7192.png">


#### 4. comparables_analysis.py

Finally we arrive at the comparables analysis. In this script I first make a Company class that houses all of the data I've gathered for each company. I also create methods for it called get_comparables() and get_ccv(). get_comparables() will find the 5 closest companies in terms of revenue to the target company within it's sector. get_ccv() averages the enerprise value of these companies to give it's comparable company valuation. I realize this method has limits to it and the actual process of comparable company analysis is more nuanced than this, but this is my rough approximation. I use these methods to obtain the comparable company valuation for each company in my predictions dataframe in order to get a baseline to compare my models against. Below is the final dataframe with all of the data and predicitons in it.

<img width="650" alt="screen shot 2019-02-09 at 1 06 31 pm" src="https://user-images.githubusercontent.com/38504767/52524497-8e2dcd80-2c6b-11e9-9383-e8461dd23089.png">

## Results 

I am extremely happy with the results I've obtained. The comparable company valuation had a mean absolute error of 1175.3%, the regression had a mean absolute error of 62.0%, and the random forest had a mean absolute error of 71.5%. I was expecting the random forest to pick up interaction effects between sector and assets/revenue, but it turns out that a simple regression outperformed it. These results are in-line with a research paper published by the Securities Litigation and Consulting Group in which they ran a regression on only revenue for a company in an attempt to beat the comparable copmany valuation and got a mean absolute error of 31.7% for regression and 11,641.8% for comparable company analysis.

<img width="200" alt="screen shot 2019-02-09 at 1 08 26 pm" src="https://user-images.githubusercontent.com/38504767/52524524-d816b380-2c6b-11e9-81fe-d411773de220.png">       <img width="500" alt="screen shot 2019-02-09 at 1 09 12 pm" src="https://user-images.githubusercontent.com/38504767/52524533-eb298380-2c6b-11e9-8ac8-0dc7be1a0eab.png">





