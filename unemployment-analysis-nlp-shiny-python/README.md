# Data and Programming for Public Policy II - Python Programming
# PPHA 30538
## Final Project: Unemployment Analysis
#Repo name: final-project-unemployment_analysis_ajs
#Repo location: datasci-harris/final-project-unemployment_analysis_ajs

## Autumn 2022

## Libraries imports
1. Pandas
2. Requests
3. statsmodel.API
4. Seaborn
5. PyPDF2
6. Matplotlib
7. Spacy
8. TextBlob
9. nltk
10. spacytextblob
11. WordCloud
12. Shiny
13. Shinywidgets
14. numpy
15. datetime
16. ipywidgets


## Project Description 

### Research Question 
This research  studies how unemployment rates in OECD 
(Organization for Economic Co-operation and Development) countries are 
affected by indicators such as inflation, average wages, currency valuation,
education, public spending, growth of working age population, and old age 
population dependency.

### Data Used 
The research uses OECD data, extracted from the OECD data portal and the
 World Bank database through API for automatic data retrieval. 
 OECD Data Portal Link : https://stats.oecd.org/ 
 World Bank Data Link: https://data.worldbank.org/indicator 
 Metrics downloaded are as follows:

1. Unemployment Rate 
2. Inflation
3. Average wage
4. Exchange rate
5. Dependency in old age 
6. College enrollment
7. Public expenditures 
8. Working age population percentage

For the OLS regression and model fitting, the research considers 4 countries 
out of the 38 OECD countries, that include Canada, France, United States, and 
Japan.

In the final dataset, the research obtains data of OECD countries from the year 
2000 to 2020.
Due to a large number of missing values, some countries were omitted. 

For the nlp analysis, the research makes use of news releases from federal
reports and bureau of labor statistics. 

The processed data is outputted in the folder named cleaned_data. To do
so the code uses data from the folder - data_inputs. 

### Approach 
The research proceeds by identifying a relevant research question to the 
present times, where we observe high layoffs and possibilities of rising 
unemployment. Then data is extracted from data bases automatically and manually
for each of the variables mentioned earlier. 

After processing the data, there are both static and interactive plots prepared 
and presented using the shiny app to make the data more visually accessible.
For each country there is an option for the user to compare 2 indicators for a
particular year with a trend across years. 

Using NLP, the shiny app allows the user to visualize the polarity and 
subjectivity present in the federal reports released every year. There is 
also a word cloud representing the most frequent used terms in the report, 
added as a image in the files along with the static plots. The code also enables 
the user to place any article or report into the reports folder and visualize 
the sentiment in shiny. (NLP code uses the reports folder for inputs).

### Model Results 
The paper uses ordinary least squares regression to examine the impact of 
inflation on the unemployment rate and the inflation on the unemployment rate.

1. Average wage on unemployment rate:
Using ordinary least squares regression, the paper finds that the average wage is 
negatively correlated with the unemployment rate in 2022, with an estimated 
coefficient of -0.003. This means that a one percentage point increase in the 
average wage results in a 0.3 percentage point decrease in the unemployment 
rate. Therefore, there is no standard deviation since the standard error is 0.
 While this may be interesting, the data does not meet statistical significance.

2. Inflation on unemployment rate:
Based on ordinary least squares, the paper estimates a coefficient of -0.6150 between 
inflation and the unemployment rate in 2022. This means that for every one 
percentage point change in the inflation, unemployment rate drops by 
61.5 percentage points. There was a 0.198 percent margin of error. 
While this may be interesting, the data does not meet statistical significance.

Plots: 
All plots including the static plot, word cloud, sentiment trends are in the 
plots folder. 


### Weaknesses and Difficulty 

1. The variables in study are macroeconomic variables that are affected 
by many other variables, giving way to possible omitted variable bias. 
2. The covariates are macroeconomic variables that are interrelated and thus 
have multicolinearity issues, further multivariable analysis could be useful. 
3. The reports may not represent the complete context and opinions at the time. 



# Disclaimer: the code is designed on mac systems. Some file operations 
may require additional changes based on the Operating System. 
For instance, path separators may not be '/' in all cases. 










