
import streamlit as st
import pandas as pd
import numpy as np
from PIL import Image
image = Image.open('rg_logo.jpg')
st.image(image)

# Title
st.header("RadioGraphics Reviewer Article Matching")


df = pd.DataFrame({
    'first column': ['Informatics', 'Abdominal', 'Neuroradiology', 'Thoracic'],
    'second column': [10, 20, 30, 40]
    })

option = st.selectbox(
    'Which speciality would you like to select?',
     df['first column'])

'You selected: ', option


df = pd.read_csv('RSNAInformaticsExhibits.csv')
df = df[['TITLE','Institution','Classification']].head(5)
st.table(df)


df1 = pd.read_csv('https://docs.google.com/spreadsheets/d/1GP8k9J2cSPhCmmX7774bqxW7uKeODjc3zw3D2Cai1HQ/export?format=csv&gid=51107142')
st.table(df1)




uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
#      # To read file as bytes:
#      bytes_data = uploaded_file.getvalue()
#      st.write(bytes_data)

#      # To convert to a string based IO:
#      stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
#      st.write(stringio)

#      # To read file as string:
#      string_data = stringio.read()
#      st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
    dataframe = pd.read_csv(uploaded_file)
    st.write(dataframe)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        article_column = st.selectbox(
            'Which column contains the Article Titles?',
            df.columns)
    with col2:
        institution_columm = st.selectbox(
            'Which column contains the Article Institutions?',
            df.columns)
    with col3:
        category_column = st.selectbox(
            'Which column contains the Article Categories?',
            df.columns)


# # Add a selectbox to the sidebar:
# add_selectbox = st.sidebar.selectbox(
#     'How would you like to be contacted?',
#     ('Email', 'Home phone', 'Mobile phone')
# )

# # Add a slider to the sidebar:
# add_slider = st.sidebar.slider(
#     'Select a range of values',
#     0.0, 100.0, (25.0, 75.0)
# )


st.header('Step 1: Choose your RG Specialty')
st.subheader('Here are your reviewers that have filled out their topic preferences.')

st.header('Step 2: Choose your Article Matching Parameters')
st.subheader('How many times should an article be reviewed?')

st.header('Step 3: Upload your CSV file containing your exhibit titles and information')
st.subheader('Make sure to choose which columns correspond to the following variables')



# If button is pressed
if st.button("Submit"):
    
    
    
    # Output prediction
    st.text(f"This instance is a submission button")
    
    
csv = 'hello'
st.download_button(
     label="Download data as CSV",
     data=csv,
     file_name='large_df.csv',
     mime='text/csv',
 )
