#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import geopandas as gpd
import censusdata

from scipy import stats

os.environ["CENSUS_API_KEY"] = "d6a829e3229193acd4e98d0f4ad90540cdfe59d5"


# # Extract SF Census Data from API

# In[17]:


zip_codes = [94401,94402,94403,94497,94404,94063,94062,94061,94064,94065,94117,94121,94122,94188,94404,94123,94403,94164,94146,
94497,94108,94112,94134,94158,94127,94126,94103,94159,94134,94107,94102,94110,94118,94132,94128,94112,94104,94116,
94133,94143,94401,94124,94130,94147,94109,94129,94105,94114,94115,94402,94119,94125,94111,94131,94141,94140, 
             94044, 94002, 94903, 94939, 94015, 94901, 94960, 94066, 94904, 94010, 
              94070, 94947, 94949, 94945, 94080, 94920, 94941, 94965, 94014, 94025, 94925]
zip_codes_str = [str(i) for i in zip_codes]



# In[129]:


def local_census_data(year, zip_code):
    # Specify the state code in the geographic boundary
    zipcode = censusdata.censusgeo([('state', '06'), ('zip code tabulation area', zip_code)])

    # Download the data for the specified variables and geographic boundary
    sfbg_zip = censusdata.download('acs5', year, zipcode,
                                   ['B01003_001E','B08013_001E','B25001_001E','B25002_002E','B25002_003E'],
                                   key='d6a829e3229193acd4e98d0f4ad90540cdfe59d5')
    sfbg_zip = sfbg_zip.reset_index()
    sfbg_zip = sfbg_zip.rename(columns={
        'index': 'Zip Code',
        'B01003_001E': 'Total Population',
        'B08013_001E': 'Aggregate Travel Time to Work',
        'B25001_001E': 'Total Housing',
        'B25002_002E': 'Owner-occupied housing units',
        'B25002_003E': 'Renter-occupied housing units',
    })
    sfbg_zip['Percentage of Rent'] = sfbg_zip['Renter-occupied housing units']/sfbg_zip['Total Housing']
    sfbg_zip['Zip Code'] = sfbg_zip['Zip Code'].astype(str)
    sfbg_zip['Zip Code'] = sfbg_zip['Zip Code'].apply(lambda x: str(x).split(">")[-1].split(":")[1].strip() 
                                                                if isinstance(x, str) else x.tract.split(":")[-1].strip())
    sfbg_zip['Year'] = year
    sfbg_zip = sfbg_zip.sort_values(by = ['Zip Code'], ignore_index = True)
    return sfbg_zip


# # Concat SF 10 year census data

# In[21]:


# Concatenate
sf_all = pd.DataFrame()
start_year = 2011
end_year = 2020

for year in range(2011, 2020):
    for zip_c in zip_codes_str:
        try:
            sf_county = local_census_data(year, zip_c)
            sf_all = pd.concat([sf_all, sf_county], ignore_index=True)
        except Exception:
            pass


# In[34]:


sf_all.to_csv('sf_new_all.csv',index=False)


# In[33]:


sf_all['Average Travel Time to Work per person'] = sf_all['Aggregate Travel Time to Work']/ 
                                                         sf_all['Total Population']


# In[32]:


sf_all = sf_all.drop('Aggregate Travel Time to Work',axis=1)
sf_all = sf_all.dropna()


# In[100]:


duplicates = sf_all.duplicated(subset=['Zip Code', 'Year'])
print(f"Number of duplicate rows: {duplicates.sum()}")
sf_all_drop = sf_all.drop_duplicates(subset=['Zip Code', 'Year'])


# In[79]:


zipcode = list(sf_all_drop['Zip Code'].unique())


# In[80]:


for zip_code in zipcode:
    rows_for_zip_code = sf_all_drop[sf_all_drop['Zip Code'] == zip_code]
    print(f"Number of rows for Zip Code {zip_code}: {len(rows_for_zip_code)}")


# In[53]:


duplicates = sf_all_drop.duplicated(subset=['Zip Code', 'Year'])
print(f"Number of duplicate rows: {duplicates.sum()}")


# In[101]:


sf_all_drop.loc[:, 'Average Travel Time to Work per person'] = sf_all_drop.loc[:, 'Average Travel Time to Work per person'].astype(float)


# In[102]:


sf_all_drop


# # Perform Linear Interpolation on SF

# In[134]:


import pandas as pd
import numpy as np

def create_dataframe():
    df = (pd.DataFrame(index=pd.date_range('2010-01-01', '2019-12-31', freq='3MS'))
          .reset_index()
          .rename(columns={'index': 'y_dt'})
          .assign(key=1)
         )
    return df

def merge_dataframes(df, df_to_merge):
    df_census_tract = df_to_merge.loc[:, ['Zip Code']].drop_duplicates().assign(key=1)
    df = pd.merge(df, df_census_tract, how='outer', on='key').drop(['key'], axis=1)

    assert df_to_merge.shape[0] == df_to_merge.loc[:, ['Zip Code', 'Year']].drop_duplicates().shape[0]

    df_to_merge.loc[:, 'y_dt'] = pd.to_datetime(df_to_merge['Year'], format='%Y')
    df_to_merge = df_to_merge.sort_values('y_dt')

    merged_df = pd.merge(df, df_to_merge, how='left', on=['y_dt', 'Zip Code'])
    merged_df = merged_df.sort_values(['Zip Code', 'y_dt'])
    return merged_df

def interpolate_data(merged_df):
    new_df = merged_df.copy()
    new_df.loc[:, 'new_col'] = np.nan

    for census_tract in merged_df.loc[:, 'Zip Code'].unique():

        merged_df = merged_df.sort_values(['Zip Code', 'y_dt'])

        for col in ['Total Population', 'Total Housing','Owner-occupied housing units','Renter-occupied housing units',
                   'Average Travel Time to Work per person']:

            temp_df = (merged_df.loc[(merged_df.loc[:, 'Zip Code'] == census_tract), [col]]
                        .interpolate(method="spline", order=1, limit_direction="both", downcast="infer")
                        .interpolate(method='bfill')
                        .reset_index(drop=True))

            new_df.loc[(new_df.loc[:, 'Zip Code'] == census_tract), f'Quarterly {col}'] = temp_df.values
    return new_df


# In[135]:


#call the functions

df = create_dataframe()
merged_df = merge_dataframes(df, sf_all_drop)
new_df = interpolate_data(merged_df)


# In[136]:


new_df


# In[143]:


cleaned_df = new_df.loc[:, ['y_dt','Zip Code','Quarterly Total Population','Quarterly Total Housing',
                           'Quarterly Owner-occupied housing units','Quarterly Renter-occupied housing units'
                           ,'Quarterly Average Travel Time to Work per person']]


# In[151]:


#cleaned_df.iloc[:,2:6] = cleaned_df.iloc[:,2:6].astype(int)


# In[141]:


def clean_intepolate_df(new_df):
    new_df = new_df.drop(columns=['new_col','Year'])
    new_df.iloc[:, 2:6] = new_df.iloc[:, 2:6].astype(int)
    new_df.iloc[:, 8:12] = new_df.iloc[:, 8:12].astype(int)
    return new_df


# In[152]:


cleaned_df.to_csv('May_Q_SF_ACS_2011-2019.csv',index=False)


# # Concat four cities ACS data

# In[ ]:


def final_acs():
    cities = ['Q_DALLAS_ACS_2010-2019.csv', 'Q_SF_ACS_2010-2019.csv', 'Q_ATL_ACS_2010-2019.csv', 'Q_BOS_ACS_2010-2019.csv']
    dfs = [pd.read_csv(city, parse_dates=['y_dt']).drop('Unnamed: 0', axis=1) for city in cities]
    final_acs = pd.concat(dfs).reset_index(drop=True)
    return final_acs


# In[ ]:




