# -*- coding: utf-8 -*-
"""
Created on Fri Nov 11 11:17:27 2022

@author: saiom
"""

import os
import shiny
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
from shiny import App, render, ui, reactive

lline_shp = geopandas.read_file(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\CTA_RailLines\CTA_RailLines.shp')
pdistricts_shp = geopandas.read_file(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\PoliceDistrict\PoliceDistrict.shp')
police_data = pd.read_csv(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\Police_Stations.csv') 
fire_data = pd.read_csv(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\Police_Stations.csv')



om_app = ui.page_fluid(
    ui.h2('Visualization of Police and Fire Stations'),
    ui.input_select(id = 'status',
                    label = 'L Line On/Off', 
                    choices = list(['On', 'Off'])),
    
    ui.output_plot('my_plot')
        
        
        )
    


def server(input, output, session):
    
    @output
    @render.plot()
    def my_plot():
        if input.status() == 'On':
            fig,ax = plt.subplots(figsize = (8,8))
            pdistricts_shp.plot(ax = ax, alpha = 0.5, color = 'white', edgecolor = 'black', label = 'Police Districts')
            for line in lline_shp['LINES'].unique():
                ax = lline_shp[lline_shp['LINES'] == line].plot(ax = ax, color = 'black', alpha = 1, linewidth = 1)
            return ax
            ax.axis('off')
            ax.set_title('Chicago Police Districts with L line')
        elif input.status() == 'Off':
            fig,ax = plt.subplots(figsize = (8,8))
            ax = pdistricts_shp.plot(ax = ax, alpha = 0.5, color = 'white', edgecolor = 'black', label = 'Police Districts')
            return ax

app = App(om_app,server)
            

