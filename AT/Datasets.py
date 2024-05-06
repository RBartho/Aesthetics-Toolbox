import pandas as pd
import streamlit as st

def show_list():
    
    st.markdown('<p class="font2">Aesthetics Toolbox</p>', unsafe_allow_html=True)
    st.markdown('<p class="font0">Datasets</p>', unsafe_allow_html=True)

    df = pd.read_csv("./datasets/MSC.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
    # df = pd.read_excel(...)  # will work for Excel files
    
    st.title("Test")  # add a title
    st.write(df)  # visualize my dataframe in the Streamlit app