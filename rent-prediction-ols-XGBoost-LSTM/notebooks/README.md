# Data directory

1. Effective Rent By ZipCode - RealPage.xlsx: PGIM's effective rent data by Zip Code, in the United States.
2. pgim_erent_all_deflated.csv: Processed, effective rent data for four matropolitan cities, deflated by CPI.
3. May_Q_SF_ACS_2011-2019.csv: Processed, quarterly, ACS data from 2011 to 2019 for SF MSA.
4. normalize_sf_x.csv: Processed, quarterly, ACS normalized data from 2011 to 2019 for SF MSA. The variables are normalized and calculated by the percentage change of the past 18 months. The detailed calculation see below.
5. Registered*Business_Locations*-\_San_Francisco.csv: This dataset includes the locations of businesses that pay taxes to the City and County of San Francisco.

# Notebooks directory

This contains notebook that we use for analysis

1. atlanta-data-download
   - The notebook "atlanta-data-download" utilizes the ACS public API to pull Atlanta data year by year spanning from 2010-2019
   - The indicators that are pulled from ACS are:
     - zip
     - Year
     - Total Population
     - Bachelor degree
     - Total Housing
     - Total Occupied housing units
     - Total Vacant housing units
     - Total Owner occupied housing units
     - Total Renter occupied housing units
     - Median Household Income (USD)

- Further all the pulled data is exported to "Y_AT_ACS_2010-2019.csv" file

2. atlanta-data-processing

   - The notebook "atlanta-data-processing" loads the "Y_AT_ACS_2010-2019.csv" file and processes the columns to
     calculate nominal change variables required in the regression models
   - Futher a new file "Y_AT_ACS_2010-2019_Change.csv" is generate with the follwing columns ready to be used in regression models:
     - zip
     - Year
     - Total Population
     - Total Housing
     - Housing per person
     - Total Population Change
     - Total Housing Change
     - Housing per person Change

3. Week 3-5 notebook - ACS.ipynb
   This is a notebook that deals with San Francisco MSA's American Community Survey (ACS) data, including extracting variables using API, cleaning the data, and performing linear interpolation.
4. Week 6-notebook.ipynb
   This is a notebook that mainly deals with normalization and linear modeling for SF. It has PGIM data cleaning & modeling, ACS data cleaning & modeling, and final merge for SF's panel data, with effective rent (y variable) and X features. It also have some visualization.

   - The notebook "atlanta-data-processing" loads the "Y_AT_ACS_2010-2019.csv" file and processes the columns to
     calculate nominal change variables required in the regression models
   - Futher a new file "Y_AT_ACS_2010-2019_Change.csv" is generate with the follwing columns ready to be used in regression models:
     - zip
     - Year
     - Total Population
     - Total Housing
     - Housing per person
     - Total Population Change
     - Total Housing Change
     - Housing per person Change

5. process_acs_data.ipynb
   This notebook is used to conduct ACS data extraction using census API, yearly data interpolation, PGIM data merging, and OLS model building.

6. map-data-visuzaliztion.ipynb
   This notebook visualized actual rent price on choropleth maps for 4 cities filtered by zipcode, year, MSA

7. SF-map-visualization.ipynb
   This notebook visualized actual and predictive rent price on choropleth maps for SF filtered by quarter.
   
8. PCA.ipynb
   This notebook has PCA done on ACS data.

9. PCA_Stats_ML_SF.ipynb
   This notebook has modeling on PCA data for San Fran. OLS, ML, DL and Time Series Models.
10. PCA_Stats_ML_BOS.ipynb
   This notebook has modeling on PCA data for Boston. OLS, ML, DL and Time Series Models.

11. PCA_Stats_ML_DALLAS.ipynb
   This notebook has modeling on PCA data for DALLAS. OLS, ML, DL and Time Series Models.

12. PCA_Stats_ML_ATL.ipynb
   This notebook has modeling on PCA data for Atlanta. OLS, ML, DL and Time Series Models.

13. linear_interpolation_pca_city.ipynb
   Interpolation for PCA data notebook.

