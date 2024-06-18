import streamlit as st

from . import AT_misc

def show_frontpage():
       
    
    AT_misc.build_heading(head=     'Aesthetics Toolbox',
                          notes=    'This is a toolbox for aesthetic research. \
                                      The features of this toolbox can be selected from the sidebar and are briefly explained below. \
                                      The toolbox is designed as an open source project and we hereby encourage any feedback,\
                                      or extensions to the toolbox (see contacts below). '
                          )
    
    st.divider() 
    
    st.markdown('<p class="subhead">Toolbox Features</p>', unsafe_allow_html=True)
    
        
    left, cen, right = st.columns( [ 0.45, 0.1 , 0.45])  
    with left:
            
        ### QIP Machine
        st.markdown('<p class="greenL">QIP Machine</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">The QIP Machine is an interface for calculating commonly \
                    studied quantitative image properties.</p>', unsafe_allow_html=True)
        
    with right:
        ### QIP Documentation
        st.markdown('<p class="greenL">QIP Documentation</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">The QIP documentation provides the user with detailed information for each of the \
                    quantitative image properties that can be calculated with the QIP machine.</p>', unsafe_allow_html=True)
        
    # st.write(' ')
    # left, cen, right = st.columns( [ 0.45, 0.1 , 0.45])  
    
    # with left:
    #     ### Aesthetics datasets
    #     st.markdown('<p class="greenL">Aesthetics Datasets</p>', unsafe_allow_html=True)
    #     st.markdown('<p class="font1">This feature lists an extensive collection of image datasets \
    #                 used in aesthetics research, along with important metrics for each dataset. \
    #                 It allows you to search and filter for specific datasets. A download link is provided for each dataset.</p>', unsafe_allow_html=True)
    # with right:
    #     ### Datasets Documentation
    #     st.markdown('<p class="greenL">Datasets Documentation</p>', unsafe_allow_html=True)
    #     st.markdown('<p class="font1">Addition information for each aesthetics dataset can be found in the Dataset Documentation.</p>', unsafe_allow_html=True)
        
        
    st.write(' ')
    left, cen, right = st.columns( [ 0.45, 0.1 , 0.45])  
        

    with left:
        ### Resizing and Cropping
        st.markdown('<p class="greenL">Resizing and Cropping</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">This feature allows you to upload sets of images and resize and crop them. \
                    A variety of resizing and cropping options often used in aesthetic research are implemented here, \
                    including resizing to a fixed resolution, resizing to the longer side of the image, \
                   while preserving the aspect ratio, or resizing to the number of pixels. </p>', unsafe_allow_html=True)
    with right:
        ### References
        st.markdown('<p class="greenL">References</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">Lists all references cited in this toolbox. </p>', unsafe_allow_html=True)
        
    st.divider()

    st.markdown('<p class="font1">Contributers</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">Ralf Bartho: Toolbox concept, code development, maintenance, bugfixes</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">Christoph Redies: Toolbox concept, supervision of the project, QIP documentation </p>', unsafe_allow_html=True)
    #st.markdown('<p class="font1">Lisa Kossmann: Maintainence list of datasets</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">Branka Spehar, Ronald Hübner, George Mather: Provided code to compute image properties </p>', unsafe_allow_html=True)

            
    st.write('')

    st.markdown('<p class="font1">Contact and GitHub</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">Questions, suggestions, bugs: ralf.bartho@med.uni-jena.de</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">GitHub repository: https://github.com/RBartho/Aesthetics-Toolbox </p>', unsafe_allow_html=True)

    
    