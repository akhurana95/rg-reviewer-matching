
import streamlit as st
import pandas as pd
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


df = pd.DataFrame(
    np.random.randn(10, 5),
    columns=('col %d' % i for i in range(5)))

st.table(df)


uploaded_file = st.file_uploader("Choose a file")
if uploaded_file is not None:
     # To read file as bytes:
     bytes_data = uploaded_file.getvalue()
     st.write(bytes_data)

     # To convert to a string based IO:
     stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
     st.write(stringio)

     # To read file as string:
     string_data = stringio.read()
     st.write(string_data)

     # Can be used wherever a "file-like" object is accepted:
     dataframe = pd.read_csv(uploaded_file)
     st.write(dataframe)

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


# Input bar 1
height = st.number_input("Enter Height")

# Input bar 2
weight = st.number_input("Enter Weight")

# Dropdown input
eyes = st.selectbox("Select Eye Colour", ("Blue", "Brown"))

# If button is pressed
if st.button("Submit"):
    
    
    
    # Output prediction
    st.text(f"This instance is a submission button")
