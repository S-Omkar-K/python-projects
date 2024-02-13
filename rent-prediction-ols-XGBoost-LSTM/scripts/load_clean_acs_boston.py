import pandas as pd
import os
import matplotlib.pyplot as plt 
import seaborn as sns
import plotly.express as px
import geopandas as gpd
import censusdata
import numpy as np

# Set your Census API key as an environment variable
os.environ["CENSUS_API_KEY"] = "d6a829e3229193acd4e98d0f4ad90540cdfe59d5"
counties = {'25':['005','009','017','021','023','025'], '33': ['017','015'], '09':['015'],
            '44': ['001','003','005','007', '009']
}
states = {'MA':'25','NH':'33','CT':'09','RI':'44'}

county_zip = pd.read_excel('data/county_zip_bos.xlsx',converters={'zip': str,'county':str})
county_zip['county_'] = county_zip['county'].apply(lambda x: str(x)[2:])
county_zip['State_'] = county_zip.apply(lambda x: states[x['State']], axis=1)

counties_bos = ['25005','25009','25017','25021','25023','25025','33017','33015','09015','44001','44003','44005','44007', '44009']

zip = county_zip[county_zip['county'].isin(counties_bos)]
zipcodes = zip.zip.unique()
zip_df = zip.drop_duplicates(subset=['zip'])

def local_census_data(year,state,zipcode):
    zipcode = censusdata.censusgeo([('state', state), ('zip code tabulation area', zipcode)])
    bos_county = censusdata.download('acs5', year, zipcode,
                               ['B01003_001E','B06009_005E','B06009_006E','B25001_001E','B25002_002E','B25002_003E',
                                'B19013_001E'],key='d6a829e3229193acd4e98d0f4ad90540cdfe59d5')
    bos_county = bos_county.reset_index()
    bos_county = bos_county.rename(columns={
        'index': 'zip',
        'B01003_001E': 'Total Population',
        'B06009_005E': 'Bachelor degree',
        'B06009_006E': 'Graduate or Professional Degree',
        'B25001_001E': 'Total Housing',
        'B25002_002E': 'Owner-occupied housing units',
        'B25002_003E': 'Renter-occupied housing units',
        'B19013_001E': 'Median Household Income (USD)'
    })
    bos_county ['Bachelor degree'] = bos_county['Bachelor degree']+bos_county['Graduate or Professional Degree']
    bos_county['Percentage of Rent'] = bos_county['Renter-occupied housing units']/bos_county['Total Housing']
    bos_county['zip'] = bos_county['zip'].astype(str)
    bos_county['zip'] = bos_county['zip'].apply(lambda x: str(x).split(">")[-1].split(":")[1].strip() 
                                                                if isinstance(x, str) else x.tract.split(":")[-1].strip())
    bos_county['Year'] = year
    #bos_county['State'] = states[state]
    bos_county = bos_county.sort_values(by = ['zip'], ignore_index = True)
    return bos_county

# Concatenate
bos_all = pd.DataFrame()
for year in range(2011, 2020):
    for zip_c in zipcodes:
        state = str(zip_df[zip_df.zip==zip_c]['State_'].values[0])
        try:
            bos_county = local_census_data(year,state, zip_c)
            bos_all = pd.concat([bos_all, bos_county], ignore_index=True)
        except Exception:
            pass


bos_all= bos_all[bos_all['Median Household Income (USD)']>=0]

bos_all.to_csv('data/processed_data/bos_all.csv')