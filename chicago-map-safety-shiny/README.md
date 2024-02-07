# Creating a choropleth using geopandas and Chicago data, inside an interactive Shiny app. 


To do this, use the City of Chicago [Data Portal](https://data.cityofchicago.org/).

  1. Download the [CTA "L" shapefile](https://data.cityofchicago.org/Transportation/CTA-L-Rail-Lines-Shapefile/53r7-y88m).
  2. Download any other one [shapefile](https://data.cityofchicago.org/browse?tags=shapefiles) of some Chicago division (wards, neighborhoods, etc).  Keep this shapefile relatively small, e.g. police districts, not building footprints.
  3. Download two [datasets](https://data.cityofchicago.org/browse?limitTo=datasets) that can be plotted on your shapefile.  For example, if choosen wards at step two, then data from step three should either be at the ward level, or individual points that could be plotted independent of divisions.
  
Then a single plot of the shapefile from above is created, with controls that allow to do the following:

  - Toggle the "L" lines shapefile from step 1 off and on.
  - Switch between the two datasets from step 3 to change how the choropleth is colored.
  

