
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
    'first column': ['Abdominal Imaging', 'Breast Imaging', 'Cardiac Imaging', 'Chest Imaging', 
    'Emergency Radiology', 'Gastrointestinal Imaging', 'Genitourinary Imaging', 'Informatics',
    'Multisystem', 'Musculoskeletal', 'Neuroradiology', 'Nuclear Medicine',
    'Pediatric Imaging', 'Physics', 'Quality Improvement', 'Radiation Oncology',
    'Resident and Fellow Education', 'Ultrasound', 'Vascular and Interventional Radiology', "Women's Imaging"]
    })

option = st.selectbox(
    'Which speciality would you like to select?',
     df['first column'])

'You selected: ', option


st.header('Step 2: Upload your Article File')
"The file must have a column labeled 'coi_dict' if we want to ensure no conflict of interest in matching"
uploaded_file_articles = st.file_uploader("Upload your Articles CSV")
if uploaded_file_articles is not None: 
    uploaded_file_articles.seek(0)
    article_df = pd.read_csv(uploaded_file_articles)
    st.write(article_df)

st.header('Step 3: Upload your Reviewer File')
"The file must have a column labeled 'coi_dict' if we want to ensure no conflict of interest in matching"
uploaded_file_panelists = st.file_uploader("Upload your Panelists CSV")
if uploaded_file_panelists is not None: 
    uploaded_file_panelists.seek(0)
    panelist_df = pd.read_csv(uploaded_file_panelists)
    st.write(panelist_df)
# dataframe = pd.read_csv(uploaded_file_articles)
# st.write(dataframe)

st.header('Step 4: Choose how many times an article must be reviewed:')
number_of_reviews = st.slider("How many times should an article be reviewed?", 0, 5)

# If button is pressed
if st.checkbox("Match Articles to Panelists"):

    # article_df = pd.read_csv(uploaded_file_articles)
    # panelist_df = pd.read_csv(uploaded_file_panelists)
    matched_df = master_rg_match(option, article_df, panelist_df, number_of_reviews)
    
    st.header("Articles have been matched with Panelists!")

    #create new version of dataframe
    new_matched_df = {}
    for panelist in panelist_df.panelist:
        test = matched_df.isin([panelist])
        test = test[test.values==True].index.tolist()
        new_matched_df[panelist] = test
    
    # st.code(pd.Series(new_matched_df).to_frame())

    # new_matched_df = pd.DataFrame(new_matched_df)
    st.dataframe(matched_df)
    st.dataframe(pd.Series(new_matched_df).to_frame())

    if st.button("How many articles does each reviewer have to review?"):
        from functools import reduce
        dfs = [matched_df[col].value_counts().reset_index() for col in matched_df.columns]
                # matched_df[1].value_counts().reset_index(),
                # matched_df[2].value_counts().reset_index()]
                
        reviewer_counts = reduce(lambda left,right: pd.merge(left,right,on='index'), dfs)
        reviewer_counts['Sum'] = reviewer_counts[0]+reviewer_counts[1]+reviewer_counts[2]
        st.dataframe(reviewer_counts)

    st.download_button(
     label="Download data as CSV",
     data=matched_df.to_csv(),
     file_name='final_rg_matches_{}.csv'.format(option),
     mime='text/csv',
    )






# st.caption("Here's an example of what your csv file should look like:")

# df = pd.read_csv('sample_informatics_articles.csv')
# df = df[['TITLE','Institution','Classification','coi_dict']].head(5)
# st.table(df)


# st.header('Step 3: Make sure all your panelists have filled out their topic preferences')
# st.subheader('Here are your reviewers that have filled out their topic preferences.')

# df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1GP8k9J2cSPhCmmX7774bqxW7uKeODjc3zw3D2Cai1HQ/export?format=csv&gid=51107142')
# st.write(df1[df1['Which subspeciality are you a panelist for?'] == option]['Reviewer Name'])




# uploaded_file = st.file_uploader("Choose a file")
# if uploaded_file is not None:
# #      # To read file as bytes:
# #      bytes_data = uploaded_file.getvalue()
# #      st.write(bytes_data)

# #      # To convert to a string based IO:
# #      stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
# #      st.write(stringio)

# #      # To read file as string:
# #      string_data = stringio.read()
# #      st.write(string_data)

#      # Can be used wherever a "file-like" object is accepted:
#     st.header('Step 4: Choose your Article Matching Parameters')
#     st.subheader('How many times should an article be reviewed?')
#     st.subheader('Make sure to choose which columns correspond to the following variables')

    
#     dataframe = pd.read_csv(uploaded_file)
#     st.write(dataframe)
    
#     col1, col2, col3 = st.columns(3)
#     with col1:
#         article_column = st.selectbox(
#             'Which column contains the Article Titles?',
#             df.columns)
#     with col2:
#         institution_columm = st.selectbox(
#             'Which column contains the Article Institutions?',
#             df.columns)
#     with col3:
#         category_column = st.selectbox(
#             'Which column contains the Article Categories?',
#             df.columns)


# # # Add a selectbox to the sidebar:
# # add_selectbox = st.sidebar.selectbox(
# #     'How would you like to be contacted?',
# #     ('Email', 'Home phone', 'Mobile phone')
# # )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'How many times should an exhibit be reviewed?',
#     0.0, 10.0, (25.0, 75.0)
# )








# # If button is pressed
# if st.button("Submit"):
    
    
    
#     # Output prediction
#     st.text(f"This instance is a submission button")
    
    
# csv = 'hello'
# st.download_button(
#      label="Download data as CSV",
#      data=csv,
#      file_name='large_df.csv',
#      mime='text/csv',
#  )
