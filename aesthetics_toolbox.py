#Import the required libraries
import streamlit as st
import numpy as np
from  PIL import Image
from skimage import color
import os
import pandas as pd
import timeit

Image.MAX_IMAGE_PIXELS = 1e14

### custom libraries
# from SIPmachine import balance_sips, box_count_sips, CNN_sips, color_and_simple_sips, edge_entropy_sips, fourier_sips, PHOG_sips, scaling

from AT import QIPmachine, References, Documentation, Datasets, Resizing


		      

###################### TODO's
## important
# Slope Redies 1024x1024 center crop erwähnen

# resize funktion to image size funktion
# center crop algo zu image resizing
# help erklärungen zu resize funktion
# hinweis Upscaling und Warnunghinzufügen
# upsizing images KI info
# Correlation aller SIPs auf Basis aller Datensätze
# "Navigate to the downloaded files in the Anaconda-Prompt window." präzisieren
# x,y, Coordinate Schwerpunkt DCM ausgeben
# cropping to power of two

# replace SIPs qith QIPs

# option to disable standard image preprocessing where possible (resizing and cropping)

# color also for black secren

# CSV add Parameters, add extra column for grayscale, upscaling, version of toolbox used

# add Version numbers to the toolbox

# add warning and recomadation fpr image size/ image preprocessing


# indicate type of FS in results.csv
# indicate choosen parameters in results.csv

## later
# Gitlab automatic Code Tests
# Minifehler in Code kommentieren, Richtige Version auskommentieren
# code dokumentieren
# add center cropp algo

# add Dataset Part




### Collaboration fragen:
#    https://www.frontiersin.org/articles/10.3389/fcomp.2023.1140723/full
#    https://psycnet.apa.org/fulltext/2018-51763-001.html




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
#app_mode = st.sidebar.selectbox('Select mode',['SIP Calculation', 'Resizing images', 'Datasets', 'Documentation', 'References'] ) #three pages
   
app_mode = st.sidebar.selectbox('Select mode',['QIP Calculation', 'Documentation', 'References'] ) #three pages


if app_mode == 'QIP Calculation':
    QIPmachine.run_QIP_machine()
 
if app_mode == 'Documentation':
    Documentation.show_docs()
    
if app_mode == 'References':
    References.show_references()
    
if app_mode == 'Datasets':
    Datasets.show_list()
        
if app_mode == 'Resizing images':
    Resizing.run_resizing()
    
    
