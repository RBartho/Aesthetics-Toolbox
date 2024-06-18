import pandas as pd
import streamlit as st
from PIL import Image

from AT import AT_misc
 
# df = pd.read_csv("/home/ralf/Documents/18_SIP_Machine/Aesthetics-Toolbox/datasets/MSC.csv")  # read a CSV file inside the 'data" folder next to 'app.py'
# # df = pd.read_excel(...)  # will work for Excel files

# # st.title("Test")  # add a title
# # st.write(df)  # visualize my dataframe in the Streamlit app

# print(df)

def show_list():
    
     
    AT_misc.build_heading(head=     'Datasets in aesthetics research',
                          notes=    'This interactive table lists numerous datasets in aesthetics research.  Use the sidebar filters to narrow your search. '
                          )
    

    st.divider()
    
    df = pd.read_csv("./datasets/MSC.csv")  # read a CSV file inside the 'data" folder next to 'app.py'

    st.sidebar.divider()

    ### Image Type
    st.sidebar.markdown('<p class="font1"> Image Type </p>', unsafe_allow_html=True)
    # Image Type
    B_paintings = st.sidebar.checkbox('traditional paintings' , value=False)
    if B_paintings:
        df = df[df['Type'] == 'Traditional Paintings'].copy()

    B_pictures = st.sidebar.checkbox('pictures' , value=False)
    if B_pictures:
        df = df[df['Type'] == 'Pictures'].copy()

    B_gen = st.sidebar.checkbox('only AI-generated' , value=False)
    if B_gen:
        df = df[df['Type'] == 'AI-generated images'].copy()
    
    st.sidebar.divider()
    
    ### Image Origin
    st.sidebar.markdown('<p class="font1"> Image Origin </p>', unsafe_allow_html=True)
    # Image Type
    B_flickr = st.sidebar.checkbox('Flickr' , value=False)
    if B_flickr:
        df = df[df['Origin'] == 'Flickr'].copy()
    B_wiki = st.sidebar.checkbox('Wiki Art' , value=False)
    if B_wiki:
        df = df[df['Origin'] == 'WikiArt'].copy()
        
    st.sidebar.divider()
        
    ### Rating Type
    st.sidebar.markdown('<p class="font1"> Rating Type </p>', unsafe_allow_html=True)
    B_aq = st.sidebar.checkbox('aesthetic quality' , value=False)
    if B_aq:
        df = df[df['Rating Type'] == 'aesthetic quality'].copy()
        
    B_beauty = st.sidebar.checkbox('beauty' , value=False)
    if B_beauty:
        df = df[df['Rating Type'] == 'beauty'].copy()
        
    B_liking = st.sidebar.checkbox('liking' , value=False)
    if B_liking:
        df = df[df['Rating Type'] == 'liking'].copy()  
        
        
        
    st.sidebar.divider()
        
    ### Year
    st.sidebar.markdown('<p class="font1"> Year of publication </p>', unsafe_allow_html=True)
    year = st.sidebar.slider("Select range:",   2000, 2024, (2000, 2024))    
    df = df = df[df['Year'].between(year[0], year[1])]   


    st.sidebar.divider()
    
    ### num Ratings
    st.sidebar.markdown('<p class="font1"> Average Number of Rating per Image </p>', unsafe_allow_html=True)
    year = st.sidebar.slider("Select range:",   5, 7000, (5, 7000))    
    df = df = df[df['Average Number of Rating per Image'].between(year[0], year[1])]   





    #st.table(df)
    
    # st.dataframe(df, use_container_width=True)
    
    st.data_editor(
    df,
    column_config={
        "Download Link": st.column_config.LinkColumn(
            "Download link", display_text="link" ),
        
         "Paper Link": st.column_config.LinkColumn(
             "Link to scientific paper", display_text="link"),
    },
    hide_index=True,
)
  
  
