#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  2 18:27:23 2022

@author: adityaanmol
"""
import os
import pandas as pd 
import statsmodels.api as sm
import seaborn as sns

file = '/cleaned_data'
data_path = os.getcwd()+file
figures_path = os.getcwd() + '/plots'



output_dta = pd.read_csv(os.path.join(data_path ,'output_dta.csv'))
variables = output_dta.columns[2:]

study_countries = ['Canada','France','United States', 'Japan']
var_study = ['Unemployment Rate','avg_wage','Inflation','working_age']
    
for cnt in study_countries:
    c_data = output_dta[output_dta.country.isin([cnt])]
    var_study = ['Unemployment Rate','avg_wage','Inflation','working_age']
    ax = sns.pairplot(data = c_data[var_study])
    ax.fig.suptitle('Plot Matrix for '+ ' '.join(var_study) + ' in ' + cnt, \
                    y=1.02)
    ax.savefig(os.path.join(figures_path, cnt+'_matrix_plot'+'.png'))



#base ols 
x = c_data['Inflation'].tolist()
y = c_data['Unemployment Rate'].tolist()

x = sm.add_constant(x)
result = sm.OLS(y, x).fit()

print(result.summary())

                            