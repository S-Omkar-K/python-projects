
import os
import shiny
import pandas as pd
import matplotlib.pyplot as plt
import geopandas
from shiny import App, render, ui, reactive
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.colors import Normalize


lline_shp = geopandas.read_file(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\CTA_RailLines\CTA_RailLines.shp')
pdistricts_shp = geopandas.read_file(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\PoliceDistrict\PoliceDistrict.shp')
police_data = pd.read_csv(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\Police_Stations.csv') 
safety_data = pd.read_csv(r'C:\Users\saiom\OneDrive\Documents\GitHub\homework-4-S-Omkar-K\Police_Sentiment_Scores_1.csv')

def get_col(l):
    if 'Blue' in l:
        return 'b'
    elif 'Red' in l:
        return 'r'
    elif 'Purple' in l:
        return 'purple'
    elif 'Brown' in l:
        return 'brown'
    elif 'Yellow' in l:
        return 'yellow'
    elif 'Green' in l:
        return 'green'
    elif 'Pink' in l:
        return 'pink'
    elif 'Orange' in l:
        return 'orange'
    
color_dict = {l:get_col(l) for l in lline_shp['LINES'].unique()}

#Lline preprocessing
lline_shp = lline_shp.set_crs('EPSG:3435')

#Police data preprocessing
police_data_geod = geopandas.GeoDataFrame(police_data, geometry=geopandas.points_from_xy(police_data['X COORDINATE'], 
                                                                                        police_data['Y COORDINATE']))
police_data_geod = police_data_geod.set_crs('EPSG:3435')
police_data_geod = police_data_geod[police_data_geod['DISTRICT'] != 'Headquarters']


#Safety data preprocessing
safety_data = safety_data.groupby(['DISTRICT']).mean()
safety_data = safety_data.reset_index()
safety_data['DISTRICT'] = safety_data['DISTRICT'].astype(int)
safety_data = safety_data.rename(columns = {'DISTRICT': 'DIST_NUM'})


#Merging the police data containing geo data with safety data
pdistricts_shp['DIST_NUM'] = pdistricts_shp['DIST_NUM'].astype(int)
pdistricts_shp  = pdistricts_shp.join(safety_data['SAFETY'], on = ['DIST_NUM'], how = "inner")


#Building ui for the page
app_ui = ui.page_fluid(
    
    ui.row(ui.column(12, ui.h1('Visualization of Ltrain, Police Stations and Safety Sentiment scores'),
                     ui.hr(), 
                     align='center')),
    
    ui.row(ui.column(12,  ui.input_switch (id = 'status',
                     label = 'Display L Train Map Yes/No', 
                     value = False ),
                     align = 'center',

                     ),
           ui.column(12,  ui.input_select(id = 'Indicator',
                            label = 'Indicator', 
                            choices = list(['None', 'Police Stations', 'Sentiment Scores: Safety'])),
                     ui.hr(),
                     align = 'center',
                     )           
           ),

    
    
    ui.output_plot('my_plot'),
    
)


#Initiating and deploying plots
def server(input, output, session):
    @output
    @render.plot()
    def my_plot():
        
        fig,ax = plt.subplots(figsize = (12,12))
        pdistricts_shp.plot(ax = ax, alpha = 0.5, color = 'white', edgecolor = 'black', label = 'Police Districts')
        ax.axis('off')

        if input.status():
            for line in lline_shp['LINES'].unique():
                c = color_dict[line]
                ax = lline_shp[lline_shp['LINES'] == line].plot(ax = ax, color = c, alpha = 1, linewidth = 1)
                ax.axis('off')
                
            if input.Indicator() == 'Police Stations':
                ax = police_data_geod.plot(ax = ax, alpha = 0.5, color = 'blue')
                ax.axis('off')
                ax.set_title('Chicago Districts with L train map and Police Stations')

            
            elif input.Indicator() == 'Sentiment Scores: Safety':
                divider = make_axes_locatable(ax)
                cax = divider.append_axes('right', size='5%', pad=0.1)
                norm = Normalize(vmin = min(pdistricts_shp['SAFETY']), vmax = max(pdistricts_shp['SAFETY']))
                ax = pdistricts_shp.plot(ax = ax, column = 'SAFETY', cax = cax,  norm = norm, lw = 1, legend = True)
                ax.axis('off')
                ax.set_title('Chicago Districts with L train map and Safety survey scores')

                

        else:
            ax = pdistricts_shp.plot(ax = ax, alpha = 0.5, color = 'white', edgecolor = 'black', label = 'Police Districts')
            ax.axis('off')
            if input.Indicator() == 'Police Stations':
                ax = police_data_geod.plot(ax = ax, alpha = 0.5, color = 'blue')
                ax.axis('off')
                ax.set_title('Chicago Districts with Police Stations')
            elif input.Indicator() == 'Sentiment Scores: Safety':
                divider = make_axes_locatable(ax)
                cax = divider.append_axes('right', size='5%', pad=0.1)
                norm = Normalize(vmin = min(pdistricts_shp['SAFETY']), vmax = max(pdistricts_shp['SAFETY']))
                ax = pdistricts_shp.plot(ax = ax, column = 'SAFETY', cax = cax,  norm = norm, lw = 1, legend = True)
                ax.axis('off')
                ax.set_title('Chicago Districts with Safety scores ')

            
        



app = App(app_ui, server)


