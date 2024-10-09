import pandas as pd
import streamlit as st
import pandaslib as pl

#load in data from cache
survey = pd.read_csv('cache/survey.csv')
state_table = pd.read_csv('cache/states.csv')
st.dataframe(survey)
st.dataframe(state_table)

#merge survey data with state table
combined = survey.merge(state_table, left_on='state', right_on='state', how='left')


