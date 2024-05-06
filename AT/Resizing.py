import streamlit as st
import os

from AT import scaling, AT_misc

def run_resizing():
    st.markdown('<p class="font0">Resizing images</p>', unsafe_allow_html=True)
    st.markdown('<p class="font1">Common options for resizing images</p>', unsafe_allow_html=True)
    
    st.markdown(
        """
    <style>
    .stButton > button {
    color: black;
    background: white;
    width: auto;
    height: auto;
    }
    </style>
    """,
        unsafe_allow_html=True,
    )


    
    selected_img_path_r = st.session_state.get("img_path_r", 'none_selected')
    folder_path_r = st.text_input("Select the folder with the images (jpg, jpeg, png Format)", value='none_selected')
    if folder_path_r != 'none_selected':
        selected_img_path_r = folder_path_r
        st.session_state.img_path_r = selected_img_path_r
        st.write('Selected image path:', selected_img_path_r)
        

    list_of_images_r = st.session_state.get("list_of_images_r", 'none_selected')
    selected_img_path_r = st.session_state.get("img_path_r", 'none_selected')
    
    if selected_img_path_r != 'none_selected':
        
        #img_save_path_r = st.text_input("Select the folder to save the resized images", value='none_selected', key='2222')
        
        # st.session_state.img_path_r = selected_img_path_r
        # st.write('Selected image path:', selected_img_path_r)
        st.divider()
        list_of_images_r = []
        for root, dirs, files in os.walk(selected_img_path_r):
            for file in files:
                if ('.jpg' in file) or ('.jpeg' in file) or ('.png' in file) or ('.tif' in file) or ('.TIF' in file) or ('.TIFF' in file) or ('.tiff' in file): 
                    list_of_images_r.append(os.path.join(  root , file))
        st.session_state.list_of_images_r = list_of_images_r
    
    
    example_img_r = st.session_state.get("example_img_r", None)
    
    if (selected_img_path_r != 'none_selected') and (example_img_r == None):
        st.write('Examples of loaded images:') 
        example_img_r = []
        if len(list_of_images_r) >=20:
            for k in range(20):
                img_tmp = scaling.scale_to_width_keep_aspect_ratio(list_of_images_r[k], width=120)
                example_img_r.append(img_tmp)
        else:
            for k in list_of_images_r:
                img_tmp = scaling.scale_to_width_keep_aspect_ratio(k, width=120)
                example_img_r.append(img_tmp)
                 
        st.session_state.example_img_r = example_img_r

    if example_img_r:
        st.image(example_img_r, width=120 )
      
    st.divider()
        

    #with col_down:
    selected_download_path_r = st.session_state.get("download_path_r", 'none_selected')

    if selected_img_path_r != 'none_selected':
        selected_download_path_r =st.text_input("Select folder to save resized images", value='none_selected')
        if selected_download_path_r != 'none_selected':
            st.session_state.download_path_r = selected_download_path_r
            st.write("The results will be saved to:", os.path.join(selected_download_path_r))
             
    sacling_selectbox   = st.session_state.get( "sacling_selectbox", None)  
    if selected_download_path_r != 'none_selected':

        st.markdown("""       
        <style>
        div.stTitle {
        font-size:40px;
        }
        </style>""",unsafe_allow_html=True)
        st.markdown('<p class="font2">Select the type of resizing:</p>', unsafe_allow_html=True)
                
        sacling_selectbox = st.radio(
            "sacling_selectbox",
            label_visibility="collapsed",
            options=['**Resize longer side**', 
                      '**Resize shorter side**', 
                      '**Resize image width**',
                      '**Resize image height**',
                      '**Resize to fit display**',
                      '**Resize to number of pixel**',
                      '**Resize to fixed resolution**'],
            captions = ["Resize longer side  \n while maintaining  \n aspekt ratio.", 
                        "Resize shorter side  \n while maintaining  \n aspect ratio.", 
                        "Resize width  \n while maintaining  \n aspect ratio.",
                        "Resize height  \n while maintaining  \n aspect ratio.",
                        "Fit image to resolution  \n on the given display while  \n maintaining aspect ratio.", 
                        "Resize image to a given number  \n of pixels while maintaining  \n aspect ratio.",
                        "Resize image to the given resolution  \n  **not** maintaining the  \n aspect ratio.",],
            horizontal=True
        )
        
        st.session_state.sacling_selectbox = sacling_selectbox
        
    
    if sacling_selectbox:
        with st.form('Parameter for Resizing'):
            if sacling_selectbox == '**Resize longer side**':
                st.markdown('<p class="font2">Parameters for scaling longer side:</p>', unsafe_allow_html=True)
                longer_side = int(st.text_input('To how many pixels should the longer side be resized?:', value="255",  help=None,  label_visibility="visible"))
            
            elif sacling_selectbox == '**Resize shorter side**':
                st.markdown('<p class="font2">Parameters for scaling shorter side:</p>', unsafe_allow_html=True)
                shorter_side = int(st.text_input('To how many pixels should the shorter side be resized?:', value="255",  help=None,  label_visibility="visible"))
                
            elif sacling_selectbox == '**Resize image width**':
                  st.markdown('<p class="font2">Parameters for scaling image width:</p>', unsafe_allow_html=True)
                  img_width = int(st.text_input('To how many pixels should the image width be resized?:', value="255",  help=None,  label_visibility="visible"))   
                 
            elif sacling_selectbox == '**Resize image height**':
                  st.markdown('<p class="font2">Parameters for scaling image height:</p>', unsafe_allow_html=True)
                  img_height = int(st.text_input('To how many pixels should the image height be resized?:', value="255",  help=None,  label_visibility="visible"))   
                      
            elif sacling_selectbox == '**Resize to fit display**':
                  st.markdown('<p class="font2">Parameters for scaling to fit display:</p>', unsafe_allow_html=True)
                  disp_width = int(st.text_input('Whats the width of the display you want to fit?:', value="1920",  help=None,  label_visibility="visible"))   
                  disp_height = int(st.text_input('Whats the height of the display you want to fit?:', value="1080",  help=None,  label_visibility="visible"))   
                  
            elif sacling_selectbox == '**Resize to number of pixel**':
                  st.markdown('<p class="font2">Parameters for scaling to number of pixels:</p>', unsafe_allow_html=True)
                  num_pixels = int(st.text_input('To how many pixels should the image be resized?:', value="100000",  help='Number of pixels = height*width',  label_visibility="visible"))   

            elif sacling_selectbox == '**Resize to fixed resolution**':
                  st.markdown('<p class="font2">Parameters for scaling to fixed resolution:</p>', unsafe_allow_html=True)
                  img_width = int(st.text_input('To what width you want to resize the images?:', value="900",  help=None,  label_visibility="visible"))   
                  img_height = int(st.text_input('To what height you want to resize the images?:', value="900",  help=None,  label_visibility="visible"))    
            else:
                raise('wrong resizing option selected, not implemented error')
                
            st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)

    params_resizing_submitted = st.session_state.get("params_resizing_submitted", None)
######################################

    if params_resizing_submitted:
        run = st.button('**Start resizing**' )
    
        placeholder = st.empty()
        if run: 
            if list_of_images_r:
                    #progress_text = "Operation in progress. Please wait."
                    my_bar = st.progress(0)
                    # create folder to save resized images
                    os.makedirs(os.path.join(selected_download_path_r , 'Resized_images'), exist_ok=True)
                    with st.spinner("Operation in progress. Please wait and don't refresh your browser."):
                        
                        
                        
                        for n in range(len(list_of_images_r)):
                            
                            placeholder.text('Resizing image:   ' + list_of_images_r[n].split('/')[-1])
    
                            file_path = list_of_images_r[n]
                            if sacling_selectbox == '**Resize longer side**':
                                img_resized = scaling.scale_longer_side_keep_aspect_ratio(file_path, longer_side)
                                
                            elif sacling_selectbox == '**Resize shorter side**':
                                img_resized = scaling.scale_shorter_side_keep_aspect_ratio(file_path, shorter_side)
                               
                            elif sacling_selectbox == '**Resize image width**':
                                img_resized = scaling.scale_to_width_keep_aspect_ratio(file_path, img_width)
                               
                            elif sacling_selectbox == '**Resize image height**':
                                img_resized =  scaling.scale_to_height_keep_aspect_ratio(file_path, img_height)
                                
                            elif sacling_selectbox == '**Resize to fit display**':
                                img_resized = scaling.resize_to_fit_display(file_path, disp_width, disp_height)
                                
                            elif sacling_selectbox == '**Resize to number of pixel**':
                                img_resized = scaling.scale_to_number_of_pixels_keep_aspect_ratio(file_path, num_pixels)
                                
                            elif sacling_selectbox == '**Resize to fixed resolution**':
                                img_resized = scaling.scale_to_resolution(file_path, img_width, img_height)
                                
                            else:
                                raise('wrong resizing option selected, not implemented error')

                            img_resized.save( os.path.join(selected_download_path_r , 'Resized_images', list_of_images_r[n].split('/')[-1]) ,  quality=100, subsampling=0)  

                            my_bar.progress( int( (n+1)/len(list_of_images_r) * 100) )
    
    
            else:
                st.write('No image files found. Load images first.')
        
    
        enable_download = False
        if run and list_of_images_r:
            enable_download = True
              
        if enable_download:
            st.success('Resizing finished.', icon="✅")
          
    