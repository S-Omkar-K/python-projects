import pandas as pd
import numpy as np
from datetime import datetime
import statsmodels.api as sm
from sklearn.linear_model import LinearRegression
from dateutil.relativedelta import relativedelta
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
from linearmodels import PanelOLS
from linearmodels import RandomEffects
import statsmodels.api as sm
from statsmodels.iolib.summary2 import summary_col
from linearmodels.panel import compare


#### read data
pgim_all = pd.read_csv('data/processed_data/pgim_erent_all.csv')
pgim_all['y_dt'] = pd.to_datetime(pgim_all['y_dt'])

#we only want data from 2011-2019, but for change we want to perserve values after 18 months for 2019
mask = (pgim_all['y_dt'].dt.year >= 2011) & (pgim_all['y_dt'].dt.year <= 2021)
df_filtered = pgim_all.loc[mask]

rent_df = df_filtered.reset_index(drop = True)


rent_df['y_dt'] = pd.to_datetime(rent_df['y_dt'])

# Get base year values for each zip code
base_year_rent = rent_df.loc[rent_df['y_dt'] == '2012-01-01', ['Zip Code', 'e_rent']].set_index('Zip Code')

# Create a dictionary for easier lookup
base_rent_dict = base_year_rent['e_rent'].to_dict()

# Apply base year values to each row
rent_df['base rent'] = rent_df['Zip Code'].map(base_rent_dict)

# Get future date values by shifting the data by 6 quarters (18 months)
rent_df['future date'] = rent_df.groupby('Zip Code')['y_dt'].shift(-6)
rent_df['future value'] = rent_df.groupby('Zip Code')['e_rent'].shift(-6)

# Calculate rent change
rent_df['rent_change'] = (rent_df['future value'] - rent_df['e_rent']) / rent_df['base rent']

# Filter the output to keep only the desired columns
output_columns = [
    'Zip Code', 'y_dt', 'e_rent', 'future date', 'future value', 'base rent', 'rent_change'
]
result = rent_df[output_columns]

# Display the result
result

new_erent = result[['Zip Code','y_dt','rent_change']]

new_erent.to_csv('data/processed_data/pgim_processed_change.csv')

# Population + Housing data from ACS
acs_all = pd.read_csv('Q_all_ACS_2010-2019.csv')
acs_all['Zip Code'].nunique()


# Convert 'y_dt' column to datetime
acs_all['y_dt'] = pd.to_datetime(acs_all['y_dt'])

# Calculate housing/person
acs_all['Housing/person'] = acs_all['Quarterly Total Housing'] / acs_all['Quarterly Total Population']

# Get base year values for each zip code
base_year_values = acs_all.loc[acs_all['y_dt'] == '2012-01-01', ['Zip Code', 'Quarterly Total Population', 'Quarterly Total Housing']].set_index('Zip Code')

# Create dictionaries for easier lookup
base_population_dict = base_year_values['Quarterly Total Population'].to_dict()
base_housing_dict = base_year_values['Quarterly Total Housing'].to_dict()

# Apply base year values to each row
acs_all['base Population'] = acs_all['Zip Code'].map(base_population_dict)
acs_all['base Housing'] = acs_all['Zip Code'].map(base_housing_dict)

# Get prior date values by shifting the data by 6 quarters (18 months)
acs_all['prior date'] = acs_all.groupby('Zip Code')['y_dt'].shift(6)
acs_all['prior population'] = acs_all.groupby('Zip Code')['Quarterly Total Population'].shift(6)
acs_all['prior housing'] = acs_all.groupby('Zip Code')['Quarterly Total Housing'].shift(6)
acs_all['prior housing/person'] = acs_all.groupby('Zip Code')['Housing/person'].shift(6)

# Calculate changes
acs_all['Population Change (%)'] = (acs_all['Quarterly Total Population'] - acs_all['prior population']) / acs_all['base Population']
acs_all['Housing Change (%)'] = (acs_all['Quarterly Total Housing'] - acs_all['prior housing']) / acs_all['base Housing']
acs_all['Housing/person Change (%)'] = (acs_all['Housing/person'] - acs_all['prior housing/person']) / acs_all['prior housing/person']

# Filter the output to keep only the change columns, y_dt, and Zip Code
output_columns = [
    'y_dt', 'Zip Code', 'Population Change (%)', 'Housing Change (%)', 'Housing/person Change (%)'
]
acs_processed = acs_all[output_columns]

# Display the result
acs_processed


# Merge_data

merge_data = pd.merge(acs_processed,new_erent, on = ['y_dt','Zip Code'], how = 'inner')
merge_data = merge_data.dropna()

features= ['Population Change (%)','Housing Change (%)','Housing/person Change (%)']

X = merge_data[features]
y = merge_data['rent_change']

# pooled ols
X = sm.add_constant(X)
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())


merge_data.rename(columns={'y_dt':'year'},inplace=True)
year = pd.Categorical(merge_data.year)
merge_data = merge_data.set_index(['Zip Code', 'year'])
merge_data['year'] = year

# random effect model
exog_vars = features
exog = sm.add_constant(merge_data[exog_vars])
mod_ran= RandomEffects( merge_data['rent_change'], exog).fit()
print(mod_ran)

# fixed effect models
mod1= PanelOLS(merge_data['rent_change'], exog,entity_effects =False, time_effects = False).fit()
mod2= PanelOLS(merge_data['rent_change'], exog,entity_effects =False, time_effects = True).fit()
mod3= PanelOLS(merge_data['rent_change'], exog,entity_effects =True, time_effects = False).fit()
mod4= PanelOLS(merge_data['rent_change'], exog,entity_effects =True, time_effects = True).fit()

print(mod4)

print(compare({'Pooled OLS': mod1,'Random Effect': mod_ran,
                'Fixed Effect 1': mod2, 'Fixed Effect 2': mod3, 'Fixed Effect 3': mod4}, stars = True))

##### do hausman test to compare re vs fe
import numpy.linalg as la
from scipy import stats

def hausman(fe, re):
    b = fe.params
    B = re.params
    v_b = fe.cov
    v_B = re.cov
    df = b[np.abs(b) < 1e8].size
    chi2 = np.dot((b - B).T, la.inv(v_b -v_B).dot(b - B))
    pval = stats.chi2.sf(chi2, df)
    return chi2, df, pval


hausman_results = hausman(mod_ran, mod4) 
print('chi-Squared: ' + str(hausman_results[0]))
print('degrees of freedom: ' + str(hausman_results[1]))
print('p-Value: '+ str(hausman_results[2]))


