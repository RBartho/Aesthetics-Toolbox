#Import the required libraries
import streamlit as st
from PIL import Image


Image.MAX_IMAGE_PIXELS = 1e14

### custom libraries

from AT import QIPmachine, References, QIP_Documentation, Resizing, Frontpage

st.set_page_config(layout="wide")


### Define custom markdowns
st.markdown(""" <style> .font0 {
font-size:28px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font1 {
font-size:20px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .head {
font-size:35px ;  font-family: 'Cooper Black'; color: #FF9633;}
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .subhead {
font-size:28px ;  font-family: 'Cooper Black'; color: #FF9633;}
</style> """, unsafe_allow_html=True)

# st.markdown(""" <style> .font2 {
# font-size:35px ;  font-family: 'Cooper Black'; color: #FF9633;}
# </style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font2 {
font-size:20px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .greenL {
font-size:28px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font3 {
font-size:18px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font4 {
font-size:16px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

############################################################
################ define sidebar ############################
############################################################

### set width of the sidebar
st.markdown(
    """
    <style>
        section[data-testid="stSidebar"] {
            width: 100px !important; # Set the width to your desired value
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.sidebar.header("Sidebar")

### define order and names of sidebar menu
 
# app_mode = st.sidebar.selectbox('Select mode',['Home' , 'QIP Machine',  'Aesthetics Datasets',  'Resizing and Cropping', 'Docs QIPs', 'Docs Datasets', 'References', ] ) #three pages

app_mode = st.sidebar.selectbox('Select mode',['Home' , 'QIP Machine',   'Image preprocessing', 'Documentation QIPs',  'References', ] ) #three pages


if app_mode == 'Home':
    Frontpage.show_frontpage()

if app_mode == 'QIP Machine':
    QIPmachine.run_QIP_machine()
 
# if app_mode == 'Aesthetics Datasets':
#     Datasets.show_list()

if app_mode == 'Image preprocessing':
    Resizing.run_resizing()
    
if app_mode == 'Documentation QIPs':
    QIP_Documentation.show_docs()
    
# if app_mode == 'Documentation Datasets':
#     Datasets_documentation.show_data_docs()
    
if app_mode == 'References':
    References.show_references()
    
    