import streamlit as st
import pandas as pd

# Title of the app
st.title("Backgammon Match Results")

# Instructions for the user
st.write("""
### Welcome!
Please upload a CSV file containing backgammon match results.
""")

# File uploader for CSV files
uploaded_file = st.file_uploader("Choose a CSV file", type="csv")

# If a file is uploaded, read and display it
if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.write("### Match Results Table", df)
