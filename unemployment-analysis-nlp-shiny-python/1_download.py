#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
@author: adityaanmol
"""
import pandas as pd 
from pandas_datareader import wb
import requests
import os

work_dir = '/Users/adityaanmol/Documents/GitHub/final-project-unemployment_analysis_ajs'
file = '/data_inputs'
cleaned_data_path = 'cleaned_data/output_dta.csv'
os.chdir(work_dir)

start = 2000
end = 2020

indicators_wb = ['FP.CPI.TOTL.ZG','SL.UEM.TOTL.ZS']
columns_wb = ['Inflation','Unemployment Rate']
wb_col = {indicators_wb[i]: columns_wb[i] for i in range(len(indicators_wb))}


def api_toggle(wb_col, indicators_wb):
    auto = []
    for col in indicators_wb:
        text = 'Do you want automatic retrieval for '+ wb_col[col]+' ? (Y/N) '
        user = input(text)
        auto.append(user)
    return auto

def get_wb_dta(indicators,wb_col, countries, start, end):
    df = pd.DataFrame()
    toggle = api_toggle(wb_col, indicators_wb)
    count = 0
    for indicator in indicators:
        if toggle[count].lower() == 'y':           
            dta =  wb.download(indicator=indicator, \
                               country=countries, start=start, end=end)    
            dta = dta.reset_index()
            dta['country'] = dta['country'].astype('string')
            dta['year'] = dta['year'].apply(pd.to_numeric, errors = 'coerce')
          
        else:
            dta = pd.read_csv(os.path.join(work_dir + file , columns_wb[count]+'_wb.csv'))            
            dta['country'] = dta['country'].astype('string')
            dta['year'] = dta['year'].apply(pd.to_numeric, errors = 'coerce')
          
        if df.empty:
            df = dta
        else:
            df = df.merge(dta,on=['country','year'],how='outer') 
        count += 1
        
    df = df.reset_index()
    df['year'] = df['year'].apply(pd.to_numeric, errors = 'coerce')
    return df 

def merge_dta(df,dta):
    if df.empty:
        df = dta
    else:
        df = df.merge(dta,on=['country','year'],how = 'outer')
    return df

def read_oecd(work_dir, file, csv_name, start, end, cntry_l):
    dta = pd.read_csv(os.path.join(work_dir + file , csv_name))
    edited = dta[['LOCATION','TIME','Value']]
    col_name = csv_name[ :-4]
    edited.rename(columns = {'LOCATION':'country','TIME':'year',\
                             'Value':col_name}, inplace =True)
    edited = edited.loc[(edited['year'] >= start)\
                        & (edited['year'] <= end)]
    edited = edited[edited.country.isin(cntry_l)]
    edited.reset_index(inplace = True)
    edited = edited[['country','year',col_name]]
    return edited

def match_iso(df):       
    remove = [el for el in df.columns if el.startswith('Alpha')]
    df.drop(remove, axis = 1,inplace = True)
    df.drop('country',axis = 1,inplace = True)
    df  = df.rename(columns = {'Name':'country'})
    return df

country_dta = pd.read_csv(os.path.join(work_dir+file,'oecd_country_iso.csv'))
country_2 = list(country_dta['Alpha-2 Code'])
country_3 = list(country_dta['Alpha-3 Code'])

wb_data = get_wb_dta(indicators_wb, wb_col, country_2, start, end)
wb_data.rename(columns = wb_col, inplace = True) 

wb_data = wb_data.drop('index',axis = 1)

non_oecd_x = ['oecd_country_iso.csv', 'Inflation_wb.csv', 'Unemployment Rate_wb.csv']
entries = os.listdir(work_dir+file)
entries = [item for item in entries if (item not in non_oecd_x)]

oecd_main = pd.DataFrame()
for f_name in entries[1:]:
    oecd_dta = read_oecd(work_dir, file, f_name, start, end, country_3)
    oecd_main = merge_dta(oecd_main, oecd_dta)

matched = country_dta.merge(oecd_main, left_on=('Alpha-3 Code'),\
                            right_on= 'country')
matched = match_iso(matched)
output = wb_data.merge(matched, on = ['country','year'],how='outer')

variables = output.columns[2:]

output[variables] = output.groupby(['country'])[variables]\
    .transform(lambda x: x.fillna(x.mean()))

output.to_csv(cleaned_data_path)
    
