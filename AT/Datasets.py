import pandas as pd
import streamlit as st

def show_list():
    df = pd.read_csv("./datasets/MSC.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
    # df = pd.read_excel(...)  # will work for Excel files
    
    st.title("Test")  # add a title
    st.write(df)  # visualize my dataframe in the Streamlit app