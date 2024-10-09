import pandas as pd
import numpy as np
import streamlit as st
import pandaslib as pl
import os
  
'''
[https://www.askamanager.org/](https://www.askamanager.org/) has a salary survey its members complete. We will use this data to build out a data pipeline.

Survey is here: [https://www.askamanager.org/2021/04/how-much-money-do-you-make-4.html](https://www.askamanager.org/2021/04/how-much-money-do-you-make-4.html) They make the data publically available.

You can view the data here: [https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/edit?resourcekey=&gid=1625408792](https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/edit?resourcekey=&gid=1625408792)

You can download the data with `pd.read_csv` using this version of the URL:
[https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv](https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv)

You will need a US state name to abbreviation lookup table, which you can build here:
[https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv](https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv)

In the extract phase you pull your data from the internet and store it locally for further processing. This way you are not constantly accessing the internet and scraping data more than you need to. This also decouples the transformation logic from the logic that fetches the data. This way if the source data changes we don't need to re-implement the transformations. 

- For each file you extract save it in `.csv` format with a header to the `cache` folder. The basic process is to read the file, add lineage, then write as a `.csv` to the `cache` folder. 
- Extract the states with codes google sheet. Save as `cache/states.csv`
- Extract the survey google sheet, and engineer a `year` column from the `Timestamp` using the `extract_year_mdy` function in `pandaslib.py`. Then save as `cache/survey.csv`
- For each unique year in the surveys: extract the cost of living for that year from the website, engineer a `year` column for that year, then save as `cache/col_{year}.csv` for example for `2024` it would be `cache/col_2024.csv`

After you've completed this part commit your changes to git, but DO NOT PUSH.
'''

# Define the base path
base_path = r"C:\Users\gabri\OneDrive\Documents\ist356\ist356\assignment-05-gabriellucey\code"
cache_dir = os.path.join(base_path, 'cache')

# Ensure the cache directory exists
if not os.path.exists(cache_dir):
    os.makedirs(cache_dir)

# Read in the survey data
url = "https://docs.google.com/spreadsheets/d/1IPS5dBSGtwYVbjsfbaMCYIWnOuRmJcbequohNxCyGVw/export?resourcekey=&gid=1625408792&format=csv"
survey = pd.read_csv(url)

# Extract year from date using the extract_year_mdy function
survey['year'] = survey['Timestamp'].apply(pl.extract_year_mdy)
survey.to_csv(os.path.join(cache_dir, 'survey.csv'), index=False)

# Read in the state table data
url = "https://docs.google.com/spreadsheets/d/14wvnQygIX1eCVo7H5B7a96W1v5VCg6Q9yeRoESF6epw/export?format=csv"
state_table = pd.read_csv(url)
state_table.to_csv(os.path.join(cache_dir, 'states.csv'), index=False)

# Get each unique year in the survey data
years = survey['year'].unique()

# For each year in the survey data, extract the cost of living data
for year in years:
    col_year = pd.read_html(f'https://www.numbeo.com/cost-of-living/rankings.jsp?title={year}&displayColumn=0')
    col_year = col_year[1]
    col_year['year'] = year
    col_year.to_csv(os.path.join(cache_dir, f'col_{year}.csv'), index=False)

# Display dataframes 
st.dataframe(survey)
st.dataframe(state_table)
