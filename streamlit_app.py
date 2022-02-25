
import streamlit as st
import pandas as pd

# Title
st.header("Streamlit Machine Learning App")

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
