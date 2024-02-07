# Scraping Harris School website:
https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp
There is a list named Curriculumn after Program Details, explaining the core classes.

There are 21 bullet points for this, beginning with "Analytical Politics I" and ending
just before "Elective Options". Some of those bullet points are intented under others. 

Using requests and BeautifulSoup, the code collects the text of each of these bullet points so that the top level bullet points, e.g. "Analytical Politics I" are the keys in a dictionary, while the bullet points representing specific classes under them are values
in a list. 

The result will be a dictionary indexed by a requirement and get
back a list of core class options.