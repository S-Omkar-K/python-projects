import pandas as pd
import numpy as np

def load_effective_rent_zip_code():
    df = pd.read_excel( '../data/Effective Rent By ZipCode - RealPage.xlsx')
    return df

def load_existing_units_by_zip_code():
    df = pd.read_excel( '../data/Existing Units By ZipCode - RealPage.xlsx')
    return df    

def load_occupancy_by_zip_code():
    df = pd.read_excel( '../data/Occupancy By ZipCode - RealPage.xlsx')
    return df        

def load_effective_rent_zip_code_and_reshape():
    df = load_effective_rent_zip_code()
    df = (df.set_index(['Geography Name', 'Geography Type', 'Market Name', 'Unique ID',
           'Metric Type', 'Metric Name', 'Category', 'Niche']).stack().reset_index()
     .rename(columns={'level_8' : 'time_period', 0 : 'e_rent'})
    )

    return df

def load_existing_units_by_zip_code_and_reshape():
    df = load_existing_units_by_zip_code()
    df = (df.set_index(['Geography Name', 'Geography Type', 'Market Name', 'Unique ID',
           'Metric Type', 'Metric Name', 'Category', 'Niche']).stack().reset_index()
     .rename(columns={'level_8' : 'time_period', 0 : 'e_units'})
    )

    return df    


def load_occupancy_by_zip_code_and_reshape():
    df = load_occupancy_by_zip_code()
    df = (df.set_index(['Geography Name', 'Geography Type', 'Market Name', 'Unique ID',
           'Metric Type', 'Metric Name', 'Category', 'Niche']).stack().reset_index()
     .rename(columns={'level_8' : 'time_period', 0 : 'occupancy'})
    )

    return df       


def load_sf_acs_data_yearly():
    df = pd.read_csv( '../data/M_SF_ACS_2010-2019.csv') 
    return df


def load_bos_acs_data_yearly():
    df = pd.read_csv( '../data/bos_acs_zipcode_yearly.csv') 
    return df
