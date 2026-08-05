import streamlit as st
from AT import AT_misc
import pandas as pd
from pathlib import Path

AT_misc.build_heading(head  = 'DODA: Database of Datasets for Aesthetics',
                      notes = 'DODA is a curated database of image datasets used in empirical and computational aesthetics research. \
                                Each entry summarizes key properties of a dataset so that researchers can quickly search, compare, and \
                                select suitable datasets. A preprint describing DODA is available here: \
                                <a href="https://arxiv.org/abs/2608.00089" target="_blank">link to preprint</a>.',
                      DODA  = True)
               
csv_file = Path(__file__).parent / "DODA.csv"

df = pd.read_csv(csv_file, encoding="latin1")
df = df.dropna(how="all")

st.sidebar.header("🔎 Filter Options")

# # Categorical filters
# for col in df.select_dtypes(include=["object", "category"]).columns:
#     unique_vals = df[col].dropna().unique()
#     selected_vals = st.sidebar.multiselect(f"Filter by {col}", options=unique_vals, default=unique_vals)
#     df = df[df[col].isin(selected_vals)]


## Year
col = "Year"
min_val = int(df[col].min())
max_val = int(df[col].max())
if min_val != max_val:
    selected_range = st.sidebar.slider(
        f"Filter by {col}",
        min_value = min_val,
        max_value = max_val,
        value=(min_val, max_val)
    )
    df = df[df[col].between(*selected_range)]

## Number of images
col = "Size in Images"
st.sidebar.markdown(f"Filter by {col}")
numeric = pd.to_numeric(df[col], errors="coerce")
if numeric.notna().any():
    min_val = int(numeric.min())
    max_val = int(numeric.max())
    col1, col2 = st.sidebar.columns([0.3,0.7])
    user_min = col1.number_input("Min", value=min_val, min_value=min_val, max_value=max_val)
    user_max = col2.number_input("Max", value=max_val, min_value=min_val, max_value=max_val)
    if user_min <= user_max:
        df = df[numeric.between(user_min, user_max) | numeric.isna()]
    else:
        st.sidebar.warning("⚠️ Min should be less than or equal to Max")

## Number of Annotators
col = "Number of Annotators/ Participants/ Captions"
st.sidebar.markdown(f"Filter by {col}")
numeric = pd.to_numeric(df[col], errors="coerce")
if numeric.notna().any():
    min_val = int(numeric.min())
    max_val = int(numeric.max())
    col1, col2 = st.sidebar.columns([0.3,0.7])
    user_min = col1.number_input("Min", value=min_val, min_value=min_val, max_value=max_val, key="annotators_min")
    user_max = col2.number_input("Max", value=max_val, min_value=min_val, max_value=max_val, key="annotators_max")
    if user_min <= user_max:
        df = df[numeric.between(user_min, user_max) | numeric.isna() ]
    else:
        st.sidebar.warning("⚠️ Min should be less than or equal to Max")


## Votes per image
col = "Minimum Votes/Clicks per image"
st.sidebar.markdown(f"Filter by {col}")
numeric = pd.to_numeric(df[col], errors="coerce")
if numeric.notna().any():
    min_val = int(numeric.min())
    max_val = int(numeric.max())
    col1, col2 = st.sidebar.columns([0.3,0.7])
    user_min = col1.number_input("Min", value=min_val, min_value=min_val, max_value=max_val, key="votes_min")
    user_max = col2.number_input("Max", value=max_val, min_value=min_val, max_value=max_val, key="votes_max")
    if user_min <= user_max:
        df = df[numeric.between(user_min, user_max) | numeric.isna() ]
    else:
        st.sidebar.warning("⚠️ Min should be less than or equal to Max")


## 'Style of images'
col = 'Style of images'
unique_vals = df[col].dropna().unique()
selected_vals = st.sidebar.multiselect(f"Filter by {col}", options=unique_vals, default=unique_vals)
df = df[df[col].isin(selected_vals) |  df[col].isna()]


## 'Data Format'
col = 'Data Format'
unique_vals = df[col].dropna().unique()
selected_vals = st.sidebar.multiselect(f"Filter by {col}", options=unique_vals, default=unique_vals)
df = df[df[col].isin(selected_vals) |  df[col].isna()]

## 'Data Available'
col = 'Data Available'
unique_vals = df[col].dropna().unique()
selected_vals = st.sidebar.multiselect(f"Filter by {col}", options=unique_vals, default=unique_vals)
df = df[df[col].isin(selected_vals) |  df[col].isna()]


# Display filtered data
st.subheader("📄 Filtered Data")
st.dataframe(df)

