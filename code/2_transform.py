import pandas as pd
import streamlit as st
import pandaslib as pl
import os

#load in data from cache
# Define the base path
base_path = r"C:\Users\gabri\OneDrive\Documents\ist356\ist356\assignment-05-gabriellucey\code"
cache_dir = os.path.join(base_path, 'cache')

# Load in data from cache
survey = pd.read_csv(os.path.join(cache_dir, 'survey.csv'))
state_table = pd.read_csv(os.path.join(cache_dir, 'states.csv'))
st.dataframe(survey)
st.dataframe(state_table)

# Get each unique year in the survey data
years = survey['year'].unique()

# For each year in the survey data, extract the cost of living data
dfs=[]
for year in years:
    col_year = pd.read_csv(os.path.join(cache_dir, f'col_{year}.csv'))
    #clean the year column
    col_year['year'] = col_year['year']
    dfs.append(col_year)

# Concatenate the dataframes
col_data = pd.concat(dfs)
st.dataframe(col_data)

# Merge the survey data with the cost of living table

#clean survey data 
survey['What country do you work in?'] = survey['What country do you work in?'].apply(pl.clean_country_usa)

#merge data frames by state with inner join
survey_states_combined = survey.merge(state_table, left_on="If you're in the U.S., what state do you work in?", right_on='State', how='inner')

#generate a column `_full_city` based on this formula so that columns will match
survey_states_combined['_full_city'] = survey_states_combined['What city do you work in?'] + ', ' + survey_states_combined['Abbreviation'] + ', ' + survey_states_combined['What country do you work in?']

st.dataframe(survey_states_combined)

#merge the survey data with the cost of living table
combined = survey_states_combined.merge(col_data, left_on=['year', '_full_city'], right_on=['year', 'City'], how='inner')
st.dataframe(combined)
   
#create cleaned column for annual salary
combined['__annual_salary_cleaned'] = combined["What is your annual salary? (You'll indicate the currency in a later question. If you are part-time or hourly, please enter an annualized equivalent -- what you would earn if you worked the job 40 hours a week, 52 weeks a year.)"].apply(pl.clean_currency)

#generate a column `_annual_salary_adjusted` based on this formula. 
#use 2 decimal places for clarity
combined['_annual_salary_adjusted'] = round((combined['__annual_salary_cleaned'] / combined['Cost of Living Index']) * 100, 2)

st.dataframe(combined)

#Save the engineered dataset to the cache `survey_dataset.csv`
combined.to_csv(os.path.join(cache_dir, 'survey_dataset.csv'), index=False)

#generate reports for salaries based on age categories
report1 = combined.pivot_table(index='_full_city', columns='How old are you?', values='_annual_salary_adjusted', aggfunc='mean')
#save to cache
report1.to_csv(os.path.join(cache_dir, 'annual_salary_adjusted_by_location_and_age.csv'), index=True)
st.dataframe(report1)

#generate reports for salaries based on education categories
report2 = combined.pivot_table(index='_full_city', columns="What is your highest level of education completed?", values='_annual_salary_adjusted', aggfunc='mean')
#save to cache
report2.to_csv(os.path.join(cache_dir, 'annual_salary_adjusted_by_location_and_education.csv'), index=True)
st.dataframe(report2)
