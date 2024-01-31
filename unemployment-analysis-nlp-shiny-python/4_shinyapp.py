from shiny import App, render, ui, reactive
from shinywidgets import output_widget, reactive_read, register_widget
import pandas as pd 
from pandas_datareader import wb
import requests
import os
import seaborn as sns
from numpy import random
from ipywidgets import interact, interact_manual
import matplotlib.pyplot as plt
import datetime 
from matplotlib.colors import Normalize





data_path = os.getcwd() + '/cleaned_data'







clean_data= pd.read_csv(os.path.join(data_path, 'output_dta.csv'))
sentiment_data = pd.read_csv(os.path.join(data_path, '2022_sentiment_table.csv'))

article_list = os.listdir()

country_list = clean_data['country'].tolist()
country_list = sorted(list(set(country_list))) 
year_list = clean_data['year'].tolist()
year_list = list(set(year_list))
covariate_list = list(clean_data.columns[3:])

sentiment_types = ['Polarity', 'Subjectivity']


harris_logo = "https://anthonyruth.com/wp-content/uploads/2019/11/Screenshot-2019-11-11-18.58.08.png"
wb_logo = "https://1000logos.net/wp-content/uploads/2021/05/The-World-Bank-logo.png"
oecd_logo = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTi8Kv8zVE_KTN8ZgqEtkqZQ3220G19egE0Re833JYXoezkpmLCj91_StuqncHMDLXkdR0&usqp=CAU"

#http://127.0.0.1:8000
app_ui = ui.page_fluid(
    
    ui.row(
       ui.column(4, ui.img(src=oecd_logo, height=100, width =288)),
       ui.column(4, ui.img(src=harris_logo, height=100, width =288)),
       ui.column(4, ui.img(src=wb_logo, height=100, width =288))),
    
    ui.row(
        ui.column(3),
        ui.column(9, ui.h2("Yearly Unemployment effects of OECD countries "))),
   
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_select("countries", "Select an OECD country:", choices = country_list),
            ui.input_slider("year", "Select Year", clean_data['year'].min(), 
                            clean_data['year'].max(), 
                            2008, animate=False, sep = ""),
            ui.input_select("covariate1", "Select first indicator:", choices = covariate_list),
            ui.input_select("covariate2", "Select second indicator:", choices = covariate_list)),
        ui.panel_main(
            ui.output_plot("plot"),
            ui.output_ui('years'))),
    ui.row(
        ui.hr(),
        ui.column(3),
        ui.column(9, ui.h2("Sentiment trend in federal unemployment reports: 2022"))),
        ui.column(12,  ui.input_select("sentimenttype", "Select the Sentiment type:", choices = sentiment_types ),
                  align = 'center'
                  ),
        ui.output_plot('sentiment_plot')
        
    #ui.layout_sidebar(
    #    ui.panel_sidebar(
    #        ui.input_select("sentimenttype", "Select the Sentiment type:", choices = sentiment_types ),
    #        ),
    #    ui.panel_main(
    #        ui.output_plot('sentiment_plot')
    #        )
    #    )
        
    
)

def server(input, output, session):
   
    @output
    @render.plot
    def plot():
        data = clean_data[clean_data['country'] == input.countries()]
        ax = plt.scatter(data[input.covariate1()], data[input.covariate2()])       
      
        data = data[data['year'] == input.year()]
        ax = plt.scatter(data[input.covariate1()], data[input.covariate2()])
        txt1 = str(input.covariate1()) + ':' + str(data[input.covariate1()].iloc[0].round(2)) 
        txt2 =  str(input.covariate2()) + ':' +str(data[input.covariate2()].iloc[0].round(2))
        
        txt = str(input.year()) + '\n' + txt1 + '\n' + txt2
        
        plt.annotate(txt, (data[input.covariate1()] + 0.01, data[input.covariate2()] +0.01))
        plt.xlabel(input.covariate1())
        plt.ylabel(input.covariate2())
        return ax
    
    @output
    @render.plot
    def sentiment_plot():
        ax2 = plt.bar(sentiment_data['Report Date'], sentiment_data[input.sentimenttype()])
        plt.xlabel('Report Date')
        plt.ylabel(input.sentimenttype())
        plt.xticks(rotation = 45)
        return ax2
        
        
        
   # @interact (countries= country_list, variable1= covariate_list, variable2= covariate_list)     
    #def make_plot_for(countries=country_list[0], variable1= covariate_list[0], 
     #                 variable2=covariate_list[0]):     
      #  plot(clean_data, countries, variable1, variable2)
                

        
        
app = App(app_ui, server)

