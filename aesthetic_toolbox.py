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
# check for different RGB color formats and prevent differences (Chris and Hannahs skaling experiment)
# Test image formats (png, tif, jpg)
# Individuelle Parameter für PHOG measures
# Slope Redies wieder auf 1024x1024 center crop

# resize funktion to image size funktion
# center crop algo zu image resizing
# help erklärungen zu resize funktion
# hinweis Upscaling und Warnunghinzufügen

# QIPs, Sips, Aquips, ...

# Correlation aller SIPs auf Basis aller Datensätze

# "Navigate to the downloaded files in the Anaconda-Prompt window." präzisieren
# x,y, Coordinate Schwerpunkt DCM ausgeben
# Subfolder image caluclation like Segmentation

## later
# Gitlab automatic Code Tests
# Minifehler in Code kommentieren, Richtige Version auskommentieren
# code dokumentieren
# add center cropp algo
# Wunschliste Lara Datensätze: filter und Kontaktfunktion
# From home is Code BC dimension 3 Algo Mather?
# Namen festlegen: Aesthetic Toolbox, image properties
### Collaboration fragen:
#    https://www.frontiersin.org/articles/10.3389/fcomp.2023.1140723/full
#    https://psycnet.apa.org/fulltext/2018-51763-001.html

##################### recently added/fixed
# Zähler einbauen, Remaining Time
# fix download path (using os.path.join)
# new standard for PHOG scaling to no scaling
# finish image resize options
# grayscale
# refresh, wenn Sidebar wechselt
# fix the names in result txt
# Test Mac, Windows (Hannahs neuster Bug ()

# Slopes überarbeitet und OSF Sloper Version eingefügt


st.set_page_config(layout="wide")


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
app_mode = st.sidebar.selectbox('Select mode',['SIP Calculation', 'Resizing images', 'Datasets', 'Documentation', 'References'] ) #three pages
   
### Define custom markdowns
st.markdown(""" <style> .font0 {
font-size:35px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font1 {
font-size:20px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .font2 {
font-size:20px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)


if app_mode == 'SIP Calculation':
    QIPmachine.run_QIP_machine()
 
if app_mode == 'Documentation':
    Documentation.show_docs()
    
if app_mode == 'References':
    References.show_references()
    
if app_mode == 'Datasets':
    Datasets.show_list()
        
    
if app_mode == 'Resizing images':
    Resizing.run_resizing()
    
    