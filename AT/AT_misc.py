import streamlit as st
import numpy as np
from PIL import Image




# def load_image(file_path):
#     ## check for RGB 16 bit
    
    
#     ### load images in different color spaces
#     img_plain_PIL = Image.open(upload_file[n])
#     img_plain_np = np.asarray(img_plain_PIL)
#     img_rgb = np.asarray(img_plain_PIL.convert('RGB'))
#     img_lab = color.rgb2lab(img_rgb)
#     img_hsv = color.rgb2hsv(img_rgb)
#     img_gray = np.asarray(Image.open(upload_file[n]).convert('L'))  ## color uses range [0-1], PIL uses Range [0-256] for intensity
    
      




def custom_round(num):
    '''
    if values are smaler than 1, round to 3 digits after the first nonzero digit,
    since measures have very different range
    '''
    if num < 1:
        ### convert to scientific_notation
        scientific_notation = "{:e}".format(num)
        ### get the e-value 
        e_val = scientific_notation[-2:]
        return np.round(num , 3 + int(e_val))
    
    else:
        return np.round(num,3)


def click_sub_QIPs(check_dict):
    st.session_state.commit_qips = True
    st.session_state.check_dict = check_dict
    
def click_sub_params():
    st.session_state.params_submitted = True
    

def click_sub_scaling(check_dict_scaling):
    st.session_state.commit_scaling = True
    st.session_state.check_dict_scaling = check_dict_scaling

def click_sub_params_resizing():
    st.session_state.params_resizing_submitted = True


def check_upscaling_img(img_PIL, res_type, PHOG_Pixel = -1):
    w,h = img_PIL.size  
    
    ### Edge QIPs use different resizing to 300*400 pixels
    if res_type == 'EOE':  
        if w*h < 120000:
            return True
  
    ### PHOG resizing   
    elif res_type == 'PHOG': 
        if (PHOG_Pixel != -1): # upscaling used
            if w*h < PHOG_Pixel:
                return True

    ### CNN QIPs use 512x512 pixels
    elif res_type == 'CNN':  
        if (w<512) or (h<512):
            return True
        
    ### Fourier Slope **Redies** resize longer image side to 1024 pixels
    elif res_type == 'Fourier':  
        if w>=h:
            if w<1024:
                return True
        else:
            if h<1024:
                return True
    else:
        raise('Not implemented error')
    
 
    return False

def callback_upload_img_files():
    st.session_state.new_files_uploaded = True
    
def build_heading(head,notes):
    
    st.markdown(""" <style> .font1 {
    font-size:20px ; font-family: 'Cooper Black'; color: black;} 
    </style> """, unsafe_allow_html=True)
    
    st.markdown(""" <style> .head {
    font-size:35px ;  font-family: 'Cooper Black'; color: #FF9633;}
    </style> """, unsafe_allow_html=True)

    image1 = Image.open('images/LogoDesign EAJ final.png')
    image2 = Image.open('images/GestatltReVision_Logo_mod.png')

    #Create two columns with different width
    col1, col2, col3 = st.columns( [0.10, 0.7, 0.2])
    with col2:               # To display the header text using css style
        st.markdown('<p class="head">' + head + '</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">' + notes + '</p>', unsafe_allow_html=True)
    with col1:
        st.image(image1,  use_column_width=True) 
    with col3:
        st.image(image2,  use_column_width=True) 
        
        
    