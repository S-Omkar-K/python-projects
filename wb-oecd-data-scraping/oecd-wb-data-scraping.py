# PPHA 30535
# Spring 2022
# Homework 7

# Sai Omkar Kandukuri

# Sai Omkar Kandukuri
# S-Omkar-K

# Due date: Sunday May 22nd before midnight
# Write your answers in the space between the questions, and commit/push only
# this file to your repo. Note that there can be a difference between giving a
# "minimally" right answer, and a really good answer, so it can pay to put
# thought into your work.

##################

# Question 1: Explore the data portals for the OECD and the World Bank.  Pick
# any three countries, and pick two data series from each of the OECD and the
# World Bank that covers these places over some time period.  It's ok if
# frequency doesn't match up (e.g. one is monthly and one is quarterly), but
# you will need to handle the aggregation.  Load the data into dataframes using
# Pandas data_reader, then merge the data together in long (tidy) format, and
# write it to a csv document that you commit to your repo.


import pandas as pd
import datetime
import pandas_datareader.data as web
from pandas_datareader import wb
from pandas_datareader import oecd
import requests



#indicator = 'NY.GDP.MKTP.CD'
#country = ['US','IN','FR']
#start = datetime.date(year=2000, month=1,  day=1)
#end   = datetime.date(year=2010, month=12, day=31)
#wb_data = wb.download(indicator=indicator, 
 #                country=country, 
#                 start=start, end=end)







##Method 1
indicator = ['NY.GDP.MKTP.CD','EG.ELC.ACCS.ZS']
country = ['US','AU','FR']
start = datetime.date(year=2000, month=1,  day=1)
end   = datetime.date(year=2010, month=12, day=31)
wb_data = wb.download(indicator=indicator, country=country, start=start, end=end)

wb_data.head()
wb_data.reset_index(inplace = True)
wb_data = wb_data.rename(columns = {'NY.GDP.MKTP.CD': 'GDP','EG.ELC.ACCS.ZS':'Perct. Access to Electricity'})
wb_data['country'] = wb_data['country'].astype(str)
wb_data['year'] = wb_data['year'].astype(str)

#OECD data
oecd_data = web.DataReader('HISTPOP', 'oecd', 2000, 2010)
oecd_debt_data = web.DataReader('GOV_DEBT', 'oecd', 2000, 2010)
#Country United States
oecd_data_US = oecd_data["United States"]["Total"]["Total"]
oecd_data_US
oecd_data_US = oecd_data_US.to_frame()
oecd_data_US["country"] = 'United States'
oecd_data_US.reset_index(inplace = True)
#Country France
oecd_data_FR = oecd_data["France"]["Total"]["Total"]
oecd_data_FR
oecd_data_FR = oecd_data_FR.to_frame()
oecd_data_FR["country"] = 'France'
oecd_data_FR.reset_index(inplace = True)
#Country Australia
oecd_data_AU = oecd_data["Australia"]["Total"]["Total"]
oecd_data_AU
oecd_data_AU = oecd_data_AU.to_frame()
oecd_data_AU["country"] = 'Australia'
oecd_data_AU.reset_index(inplace = True)
#Concatenate country data and make it usable
oecd_all = pd.concat([oecd_data_US, oecd_data_AU, oecd_data_FR], axis = 0)
oecd_all['Time'] = oecd_all['Time'].dt.year
oecd_all = oecd_all.rename(columns = {'Time':'year', 'Total':'Population'})
oecd_all['year'] = oecd_all['year'].astype(str)
oecd_all['country'] = oecd_all['country'].astype(str)

data_final = wb_data.merge(oecd_all, on = ['country','year'], how = 'inner')

#OECD debt data for Country France
oecd_debt_data_FR = oecd_debt_data["France"]['Stocks: Outstanding amounts']['Annual']['Million USD']['Total central government debt']
oecd_debt_data_FR = oecd_debt_data_FR.to_frame()
oecd_debt_data_FR.reset_index(inplace = True)
oecd_debt_data_FR['country'] = 'France'
oecd_debt_data_FR.index

#OECD debt data for Country United States
oecd_debt_data_US = oecd_debt_data["United States"]['Stocks: Outstanding amounts']['Annual']['Million USD']['Total central government debt']
oecd_debt_data_US = oecd_debt_data_US.to_frame()
oecd_debt_data_US.reset_index(inplace = True)
oecd_debt_data_US['country'] = 'United States'
oecd_debt_data_US.index

#OECD debt data for Country Australia
oecd_debt_data_AU = oecd_debt_data["Australia"]['Stocks: Outstanding amounts']['Annual']['Million USD']['Total central government debt']
oecd_debt_data_AU = oecd_debt_data_AU.to_frame()
oecd_debt_data_AU.reset_index(inplace = True)
oecd_debt_data_AU['country'] = 'Australia'
oecd_debt_data_AU.index

#Concatenate all three country data
oecd_debt_all = pd.concat([oecd_debt_data_US, oecd_debt_data_AU, oecd_debt_data_FR], axis = 0)

#Renaming the columns and changing types to make it usable
oecd_debt_all['Time period'] = oecd_debt_all['Time period'].dt.year
oecd_debt_all = oecd_debt_all.rename(columns = {'Time period': 'year'})
oecd_debt_all['year'] = oecd_debt_all['year'].astype(str)
data_final = data_final.merge(oecd_debt_all, on = ['country','year'], how = 'inner')


#Modifying it to the desiredlong format
columns_2 = ['GDP', 'Perct. Access to Electricity', 'Population', 'Total central government debt']
columns_1 = ['country', 'year']
data_final = pd.melt(data_final, id_vars = columns_1, value_vars = columns_2, var_name = 'Indicators', value_name = 'Values')

#Providing the 4 different ways of long forms as the format was not specified

#Option 0 : Direct melt to get a long form 
data_final = pd.melt(data_final, id_vars = columns_1, value_vars = columns_2)
data_final.to_csv('C:/Users/saiom/OneDrive/Documents/GitHub/homework-7-S-Omkar-K/data_final_Option0.csv')


#Option 1: Another long format for the data, by setting index that gives another form
#data_final.set_index(['country','Year'], inplace = True)
#data_final.to_csv('C:/Users/saiom/OneDrive/Documents/GitHub/homework-7-S-Omkar-K/data_final_Option1.csv')


#Option 2: Can use the stack function to make the long form it more informative form
#data_final = pd.melt(data_final, id_vars = columns_1, value_vars = columns_2)
#data_final.stack()

#Option 3: We can transform the order by sorting according to year and then applying melt to extract a different form
#data_final2 = pd.melt(data_final2, id_vars = columns_1, value_vars = columns_2)
#data_final = pd.melt(data_final2, id_vars = columns_1, value_vars = columns_2)
#data_final = data_final.sort_values(by=['country', 'Year'])
#data_final.to_csv('C:/Users/saiom/OneDrive/Documents/GitHub/homework-7-S-Omkar-K/data_final_option3.csv')


#Option 4: Combining Index to make a meaningful form 
#data_final = pd.melt(data_final, id_vars = columns_1, value_vars = columns_2, var_name = 'Indicators', value_name = 'Values')
#data_final = data_final.sort_values(by=['country', 'Year'])
#data_final.set_index(['country','Year'], inplace = True)
#data_final.to_csv('C:/Users/saiom/OneDrive/Documents/GitHub/homework-7-S-Omkar-K/data_final_option4.csv')











