import pandas as pd

#PGIM data

df = pd.read_excel('Effective Rent By ZipCode - RealPage.xlsx')
df = (df.set_index(['Geography Name', 'Geography Type', 'Market Name', 'Unique ID',
           'Metric Type', 'Metric Name', 'Category', 'Niche']).stack().reset_index()
     .rename(columns={'level_8' : 'time_period', 0 : 'e_rent'})
    )

pgim_all = df[df['Market Name'].str.upper().str.contains('SAN FRAN|ATLANTA|BOSTON|DALLAS').fillna(False)]
pgim_all = pgim_all[['Unique ID','time_period','e_rent']]
pgim_all = pgim_all.rename(columns = {'Unique ID': 'Zip Code','time_period':'y_dt'}).reset_index()

quarter_dict = {'Q1': '-01-01', 'Q2': '-04-01', 'Q3': '-07-01', 'Q4': '-10-01'}
pgim_all['y_dt'] = pgim_all['y_dt'].apply(lambda x: x[1:5] + quarter_dict[x[5:]])
pgim_all['y_dt'] = pd.to_datetime(pgim_all['y_dt'])

pgim_all = pgim_all.drop(columns = 'index')

## deflate rent 

# read cpi data
cpi = pd.read_csv('data/cpi.csv')
cpi.drop(columns=['Series ID','Period','Year'],inplace=True)
cpi['y_dt']= pd.to_datetime(cpi['Label'])
cpi.drop(columns=['Label'],inplace=True)
cpi.rename(columns={'Value':'CPI'},inplace=True)

pgim_all = pd.merge(pgim_all,cpi, on = ['y_dt'], how = 'left')

base_quarter = '2000-10-01'

# Calculate CPI index for each quarter
pgim_all['cpi_index'] = pgim_all['CPI'] / pgim_all.loc[pgim_all['y_dt'] == base_quarter, 'CPI'].values[0]

# Calculate deflated rent price for each quarter
pgim_all['deflated e_rent'] = pgim_all['e_rent'] / pgim_all['cpi_index']

pgim_all.to_csv('data/processed_data/pgim_erent_all_deflated.csv',index=False)