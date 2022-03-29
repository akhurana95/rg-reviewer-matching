
import streamlit as st
import pandas as pd
import numpy as np
import rg_match_helper_functions as rg
from rg_match_main import *
import RothPeranson as rp

# from match.RothPeranson import MatchController
from PIL import Image
image = Image.open('rg_logo.jpg')
st.image(image)

# Title
st.header("RadioGraphics Reviewer Article Matching")


# have the user choose which speciality they are performing the match for
st.header('Step 1: Choose your RG Specialty')

df = pd.DataFrame({
    'first column': ['Informatics', 'Abdominal', 'Neuroradiology', 'Thoracic'],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which speciality would you like to select?',
     df['first column'])

'You selected: ', option


st.header('Step 2: Upload two CSV files (one for articles, one for panelists). Both files should have a column called "coi_dict" to ensure we do not match same institutions')
uploaded_file_articles = st.file_uploader("Upload your Articles CSV")
if uploaded_file_articles is not None: 
    uploaded_file_articles.seek(0)
    article_df = pd.read_csv(uploaded_file_articles)
    st.write(article_df)
uploaded_file_panelists = st.file_uploader("Upload your Panelists CSV")
if uploaded_file_panelists is not None: 
    uploaded_file_panelists.seek(0)
    panelist_df = pd.read_csv(uploaded_file_panelists)
    st.write(panelist_df)
# dataframe = pd.read_csv(uploaded_file_articles)
# st.write(dataframe)


# If button is pressed
if st.button("Match Articles to Panelists"):

    # article_df = pd.read_csv(uploaded_file_articles)
    # panelist_df = pd.read_csv(uploaded_file_panelists)
    matched_df = master_rg_match(option, article_df, panelist_df, number_of_reviews=3)
    
    st.header(f"Articles have been matched with Panelists!")

    st.dataframe(matched_df)

    st.download_button(
     label="Download data as CSV",
     data=matched_df.to_csv(),
     file_name='final_rg_matches_{}.csv'.format(option),
     mime='text/csv',
    )


