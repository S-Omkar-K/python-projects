
# Scraping Harris School website:
# https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp
# There is a list named Curriculumn after Program Details, explaining the core classes.
# There are 21 bullet points for this, beginning with "Analytical Politics I" and ending
# just before "Elective Options". Some of those bullet points are intented under others. 
# Using requests and BeautifulSoup, the code collects the text of each of these bullet points so 
# that the top level bullet points, e.g. "Analytical Politics I" are the keys in a 
# dictionary, while the bullet points representing specific classes under them are values
# in a list. The result will be a dictionary indexed by a requirement and get
# back a list of core class options.



import requests
from bs4 import BeautifulSoup

#Method 1 using lxml, no manual matching, automated retrieval
url = 'https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

my_dict = {}

attempt = 0
for lists in soup.find_all('li'):
    is_considerable = False
    for val in lists.find_all('p'):
        if val.get_text().startswith("6 core"):
            is_considerable = True
            attempt += 1
            break

    if is_considerable and attempt == 2:
        for ul in lists.find('ul'):
            for li in lists.find_all('li'):
                index = 0
                key = ''
                for data in li.find_all('p'):
                    result = data.get_text().strip()
                    if index == 0:
                        temp = result
                        key = temp[:len(temp)-1]
                        my_dict[key] = []
                    else:
                        my_dict[key].append(result.replace(u'\xa0', u' '))
                    index += 1

keys_to_delete = []
for key in my_dict.keys():
    if not my_dict[key]:
        keys_to_delete.append(key)

for key in keys_to_delete:
    del my_dict[key]

print(my_dict)

my_dict['Analytical Politics I']
my_dict['Microeconomics Sequence I']

#--------------------------------------------------------------------------------#


##Method 2 using html.parser
#A more efficient way, applicable to all universal websites, no manual matching, automated retrieval.
url = 'https://harris.uchicago.edu/academics/programs-degrees/degrees/master-public-policy-mpp'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
my_dict = {}

for unordered_lists in soup.find_all('ul'):
    for lists in unordered_lists.find_all('li'):
        
        is_considerable = False
        for val in lists.find_all('p'):
            if val.get_text().startswith("6 core"):
                is_considerable = True
                break

        if is_considerable:
          
            for li in lists.find_all('li'):
                index = 0
                key = ''
                for data in li.find_all('p'):
                    if index == 0:
                       key = data.get_text()
                       my_dict[key] = []
                    else:
                       my_dict[key].append(data.get_text())
                    index += 1

keys_to_delete = []
for key in my_dict.keys():
    if not my_dict[key]:
        keys_to_delete.append(key)


for key in keys_to_delete:
    del my_dict[key]

print(my_dict)


my_dict['Analytical Politics I:']
#did not clean ':' and 'or' as it was not mentioned. However, cleaned the in the method 1
my_dict['Microeconomics Sequence I']
#did not clean ':' and 'or' as it was not mentioned. However, cleaned in the method 1







