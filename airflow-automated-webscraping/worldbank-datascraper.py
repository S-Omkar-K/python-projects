import logging
import os
import sys
import pandas as pd
from datetime import datetime, timedelta
import requests

import airflow
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

'''
Set up logging
'''
# define a Handler which writes INFO messages or higher to the sys.stderr
console = logging.StreamHandler()
console.setLevel(logging.INFO)

# add the handler to the root logger
logging.getLogger('').addHandler(console)



DATA_DIR="/usr/local/airflow/dags/data/"

url1 = 'http://data.un.org/_Docs/SYB/CSV/SYB62_T03_201907_Population%20Growth,%20Fertility%20and%20Mortality%20Indicators.csv'
url2 = 'http://data.un.org/_Docs/SYB/CSV/SYB62_T19_201907_Consumer%20Price%20Indices.csv'

sources = {"pop.csv": url1, "pi.csv":url2}

# Set the default DAG arguments
default_args = {
    'owner': 'SaiOmkarKandukuri',
    'email': ['saiomkark@uchicago.edu'],
    'email_on_failure': False,
    'email_on_retry': False,    
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(1),
    'retries': 1,
    'retry_delay': timedelta(minutes=3),
    'schedule_interval': '@daily',    
}

# Define the DAG object
dag = DAG('DataScraper', default_args=default_args,
          schedule_interval=timedelta(minutes=3))


'''
Define functions
'''

def scrape_data(name,**kwargs):
    url = sources.get(name)
    logging.info("Scraping url: %s" ,url)
    r = requests.get(url, allow_redirects=True)
    open(DATA_DIR + name, 'wb').write(r.content)
    logging.info("Completed writing to file: %s",name)
          

def process_data():
    #create dataframes	
    df1 = pd.read_csv(DATA_DIR + "pop.csv", skiprows=[0], quotechar='"', sep=',',engine='python')
    df2 = pd.read_csv(DATA_DIR + "pi.csv", skiprows=[0], quotechar='"', sep=',',engine='python')
    
    #perform a left join
    df = df1.merge(df2, how="left", on="Region/Country/Area")
    logging.info('Data successfully processed.')
    logging.info(df.head(10))
    df.to_csv(DATA_DIR + "output.csv")
    logging.info('Output written to disk .')

'''
Define tasks
'''
# start_job_task = BashOperator(
#     task_id='StartJob',
#     bash_command='mkdir -p '+ DATA_DIR,    
#     dag=dag)

start_job_task  = DummyOperator(
    task_id='StartJob',
    dag=dag)    


process_data_task = PythonOperator(task_id='ProcessData',
                    python_callable=process_data, dag=dag)


job_complete_task = DummyOperator(
    task_id='CompleteJob',
    dag=dag)    


for name in sources.keys():
    scrape_data_task = PythonOperator(task_id='ScrapeData_'+name,
                    python_callable=scrape_data, op_kwargs={'name':name}, dag=dag)

    # run tasks in sequence
    start_job_task >> scrape_data_task >> process_data_task

process_data_task >> job_complete_task

logging.info('DAG succesfully created.')