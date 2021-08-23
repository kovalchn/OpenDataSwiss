#!/usr/bin/env python
# coding: utf-8

# In[1]:


#!/usr/bin/env python
import json
import pprint
import requests     
import pandas as pd 


# In[2]:


# package list of the Swiss open data portal
packages = 'https://ckan.opendata.swiss/api/3/action/package_list'


# In[3]:


# HTTP request
response = requests.get(packages)

#json module to load CKAN's response into a dictionary
response_dict = json.loads(response.content)

# Ccheck the contents of the response
assert response_dict['success'] is True  # make sure if response is OK
result = response_dict['result']         # packages extractions
#pprint.pprint(result)                   


# In[4]:


def get_df_from_dicts(packages): #get pandas df with needed information from the packages
    
    # initialise number of datasets
    datasetsnumber = 0
    
    # get url for package information
    base_url = 'https://opendata.swiss/api/3/action/package_show?id='
    temp = {} # build temporary dictionary 

    for package in packages:
        # url for the package from the packages list
        package_information_url = base_url + package

        # the HTTP request
        package_information = requests.get(package_information_url)

        # json module to load CKAN's response into a dictionary
        package_dict = json.loads(package_information.content)

        # check the contents of the response
        assert package_dict['success'] is True  # again make sure if response is OK
        package_dict = package_dict['result']   # take'result' part from the dictionary
        
        # fill temporary dictionary with needed information 
        temp.setdefault('owner_org', []).append(package_dict.get("owner_org", 0))
        temp.setdefault('metadata_created', []).append(package_dict.get("metadata_created", 0))
        temp.setdefault('metadata_modified', []).append(package_dict.get("metadata_modified", 0))
        temp.setdefault('author', []).append(package_dict.get("author", 0))
        temp.setdefault('name', []).append(package_dict.get("name", 0))
       
    # construct from pandas df from dictionary
    df = pd.DataFrame(temp, 
               columns=['owner_org','metadata_created', 'metadata_modified','author','name']) 
    return df    
   


# In[5]:


df=get_df_from_dicts(result)


# In[6]:


# get extract year from datetime
df['metadata_created'] = pd.to_datetime(df['metadata_created'])


# In[7]:


df['year'] = df['metadata_created'].dt.year


# In[8]:


df.head(3)


# In[25]:


# get df for the year 2020 only
df_2020 = df[df.year == 2020]

# get datasets added to opendata.swiss by different organisations in 2020
ds_2020_authors = df_2020.pivot_table(columns=['author'], aggfunc='size')

# show top 5 organisations that added the largest number of datasets 
print(f"The largest number of datasets uploaded to the opendata.swiss corresponds to the {ds_2020_authors.nlargest(1)}, where {ds_2020_authors.max()} is the number of datasets")
ds_2020_authors.nlargest(5)

