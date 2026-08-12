import streamlit as st
from AT import AT_misc





AT_misc.build_heading(head=     'Aesthetics Toolbox',
                      notes=    'This is a toolbox for aesthetics research. \
                                  The features of this toolbox can be selected from the sidebar and are briefly explained below. \
                                  The toolbox is designed as an open source project and we hereby encourage any feedback \
                                  or extensions to the toolbox (see contacts below). A detailed description of the toolbox \
                                  and the implemented image properties is available here: https://doi.org/10.3758/s13428-025-02632-3. \
                                  If you use the Aesthetics Toolbox in your work, please consider citing the published paper.'
                        
                      )

    
st.divider() 




st.markdown('<p class="subhead">Toolbox Features</p>', unsafe_allow_html=True)

    
left, cen, right = st.columns( [ 0.45, 0.1 , 0.45])  
with left:
        
    ### QIP Machine
    st.markdown('<p class="greenL">QIP Machine</p>', unsafe_allow_html=True)
    st.markdown('<p class="desc">The QIP Machine is an interface for calculating commonly \
                studied quantitative image properties (QIPs).</p>', unsafe_allow_html=True)
    st.page_link("pages/1_📊_QIP_Machine.py", label='Go to the QIP Machine', icon="▶️")
    
with right:
    ### QIP Documentation
    st.markdown('<p class="greenL">QIP documentation</p>', unsafe_allow_html=True)
    st.markdown('<p class="desc">The QIP documentation provides the user with detailed information for each of the \
                quantitative image properties (QIPs) that can be calculated with the QIP Machine.</p>', unsafe_allow_html=True)
    st.page_link("pages/3_📒_QIP_Documentation.py", label='Go to the QIP Documentation', icon="▶️")
    
# st.write(' ')
left, cen, right = st.columns( [ 0.45, 0.1 , 0.45])  

with left:
     ### Aesthetics datasets
     st.markdown('<p class="greenL">DODA: Database of Datasets for Aesthetics</p>', unsafe_allow_html=True)
     st.markdown('<p class="desc">This feature lists an extensive collection of image datasets \
                 used in aesthetics research, along with important metrics for each dataset. </p>', unsafe_allow_html=True)
     st.page_link("pages/5_🗂️_DODA.py", label='Go to DODA', icon="▶️")         
                 
with right:
    ### Resizing and Cropping
    st.markdown('<p class="greenL">Image Preprocessing</p>', unsafe_allow_html=True)
    st.markdown('<p class="desc">This feature allows you to preprocess images. \
                A variety of resizing, cropping, padding and other options are implemented here. </p>', unsafe_allow_html=True)
    st.page_link("pages/2_🔧_Image_preprocessing.py", label='Go to Image preprocessing', icon="▶️")
                
st.write(' ')
left, cen, right = st.columns( [ 0.45, 0.1 , 0.45])  
    

with left:
    ### References
    st.markdown('<p class="greenL">References</p>', unsafe_allow_html=True)
    st.markdown('<p class="desc">Lists all references cited in this toolbox. </p>', unsafe_allow_html=True)
    st.page_link("pages/4_📚_References.py", label='Go to the References', icon="▶️")
    
st.divider()

st.markdown('<p class="contr">Contributors</p>', unsafe_allow_html=True)
st.markdown('Ralf Bartho: Toolbox concept, code development, maintenance, bugfixes, DODA', unsafe_allow_html=True)
st.markdown('Christoph Redies: Toolbox concept, supervision of the project, QIP documentation, DODA', unsafe_allow_html=True)
st.markdown('Gregor Hayn-Leichsenring: Toolbox concept', unsafe_allow_html=True)
st.markdown('Lisa Kossmann, Johan Wagemanns: DODA concept and maintenance', unsafe_allow_html=True)
st.markdown('Branka Spehar, Ronald Hübner, George Mather: Provided code to compute image properties', unsafe_allow_html=True)

        
st.write('')

st.markdown('<p class="contr">Contact and GitHub</p>', unsafe_allow_html=True)
st.markdown('Questions, suggestions, bugs: ralf.bartho@gmail.com', unsafe_allow_html=True)
st.markdown('GitHub repository: https://github.com/RBartho/Aesthetics-Toolbox', unsafe_allow_html=True)
st.markdown('GitHub repository: https://github.com/RBartho/Aesthetics-Toolbox', unsafe_allow_html=True)


    
