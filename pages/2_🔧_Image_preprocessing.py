import streamlit as st
import io
from PIL import Image
from zipfile import ZipFile

from AT import resize_functions, AT_misc

st.set_page_config(layout="wide")

AT_misc.build_heading(head=     'Resizing, Cropping, Padding, Color rotation',
                      notes=    'Common options for image preprocessing in aesthetic research.'
                      )


upload_file = st.file_uploader('Load image files', type=['jpg','png','jpeg','tif'], accept_multiple_files=True, label_visibility="collapsed" )# Check to see if a  file has been uploaded



st.markdown(""" <style> .font2 {
font-size:20px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .subhead {
font-size:28px ;  font-family: 'Cooper Black'; color: #FF9633;}
</style> """, unsafe_allow_html=True)

if upload_file:
    st.write('Examples of loaded images:')       
    if len(upload_file) >=20:
        st.image(upload_file[:20], width=120 )
    else:
        st.image(upload_file, width=120 )

  
st.divider()
    
         
resizing_selectbox   = st.session_state.get( "resizing_selectbox", None)  
if upload_file:

    st.markdown("""       
    <style>
    div.stTitle {
    font-size:40px;
    }
    </style>""",unsafe_allow_html=True)
    st.markdown('<p class="font2">Select the type of resizing:</p>', unsafe_allow_html=True)
            
    resizing_selectbox = st.radio(
        "sacling_selectbox",
        label_visibility="collapsed",
        options=['**Resize longer side**', 
                  '**Resize shorter side**', 
                  '**Resize image width**',
                  '**Resize image height**',
                  '**Resize to fit display**',
                  '**Resize to number of pixel**',
                  '**Resize to fixed resolution**',
                  '**Resize to image size**',
                  '**Padding to square**',
                  '**Center crop to square**',
                  '**Center crop to power of two**',
                  '**Color rotation in Lab color space**'],
        captions = ["Resize longer side  \n while maintaining  \n aspect ratio.",    ### use two spaces for "\n" to get a line brake
                    "Resize shorter side  \n while maintaining  \n aspect ratio.", 
                    "Resize width  \n while maintaining  \n aspect ratio.",
                    "Resize height  \n while maintaining  \n aspect ratio.",
                    "Fit image to resolution  \n on the given display while  \n maintaining aspect ratio.", 
                    "Resize image to a given number  \n of pixels while maintaining  \n aspect ratio.",
                    "Resize image to the given resolution  \n  **not** maintaining the  \n aspect ratio.",
                    "Resize image to the given  \n image size (width+height) maintaining the  \n aspect ratio.",
                    'Pad image to square using  \n the mean gray values or the  \n mean RGB values, resizing optional.',
                    "Center crop image to  \n largest possible square  \n image.", 
                    'Center crop image to  \n largest square with side  \n length of power of two.',
                    'Rotate the color of  \n all images to a specified  \n degree in the Lab color space.' ],
        horizontal=True
    )
    
    st.session_state.resizing_selectbox = resizing_selectbox
    

if resizing_selectbox:
    with st.form('Parameter for Resizing'):
        if resizing_selectbox == '**Resize longer side**':
            st.markdown('<p class="font2">Parameters for resizing longer side:</p>', unsafe_allow_html=True)
            longer_side = int(st.text_input('To how many pixels should the longer side be resized?:', value="1024",  help=None,  label_visibility="visible"))
            st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
        
        elif resizing_selectbox == '**Resize shorter side**':
            st.markdown('<p class="font2">Parameters for resizing shorter side:</p>', unsafe_allow_html=True)
            shorter_side = int(st.text_input('To how many pixels should the shorter side be resized?:', value="1024",  help=None,  label_visibility="visible"))
            st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
            
        elif resizing_selectbox == '**Resize image width**':
              st.markdown('<p class="font2">Parameters for resizing image width:</p>', unsafe_allow_html=True)
              img_width = int(st.text_input('To how many pixels should the image width be resized?:', value="1024",  help=None,  label_visibility="visible"))  
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
             
        elif resizing_selectbox == '**Resize image height**':
              st.markdown('<p class="font2">Parameters for resizing image height:</p>', unsafe_allow_html=True)
              img_height = int(st.text_input('To how many pixels should the image height be resized?:', value="1024",  help=None,  label_visibility="visible"))   
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
                  
        elif resizing_selectbox == '**Resize to fit display**':
              st.markdown('<p class="font2">Parameters for resizing to fit display:</p>', unsafe_allow_html=True)
              disp_width = int(st.text_input('Whats is the width of the display you want to fit?:', value="1920",  help=None,  label_visibility="visible"))   
              disp_height = int(st.text_input('Whats is the height of the display you want to fit?:', value="1080",  help=None,  label_visibility="visible"))  
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
              
        elif resizing_selectbox == '**Resize to number of pixel**':
              st.markdown('<p class="font2">Parameters for resizing to number of pixels:</p>', unsafe_allow_html=True)
              num_pixels = int(st.text_input('To how many pixels should the image be resized?:', value="100000",  help='Number of pixels = height*width',  label_visibility="visible"))   
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)

        elif resizing_selectbox == '**Resize to fixed resolution**':
              st.markdown('<p class="font2">Parameters for resizing to fixed resolution:</p>', unsafe_allow_html=True)
              img_width = int(st.text_input('To what width do you want to resize the images?:', value="1024",  help=None,  label_visibility="visible"))   
              img_height = int(st.text_input('To what height do you want to resize the images?:', value="1024",  help=None,  label_visibility="visible"))   
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
              
        elif resizing_selectbox == '**Resize to Image size**':
              st.markdown('<p class="font2">Parameters for resizing to image size:</p>', unsafe_allow_html=True)
              des_img_size = int(st.text_input('To what image size do you want to resize the images?:', value="1024",  help=None,  label_visibility="visible"))   
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
       
        elif resizing_selectbox == '**Padding to square**':
              st.markdown('<p class="font2">Parameters for padding image to square:</p>', unsafe_allow_html=True)
              pad_resize_to = int(st.text_input('Do you want to resize the longer image side before padding (-1 = no resizing, or enter the desired pixel lenght for the longer side)?:', value="-1",  help=None,  label_visibility="visible"))   
              st.form_submit_button("**Commit resize parameter selection**", on_click=AT_misc.click_sub_params_resizing)
              
        elif resizing_selectbox == '**Color rotaion in LAB color space**':
              st.markdown('<p class="font2">Parameters for color space rotation:</p>', unsafe_allow_html=True)
              rotaion_degree = int(st.text_input('How many degrees do you want to rotate the images?:', value="45",  help=None,  label_visibility="visible"))   
              st.form_submit_button("**Commit parameter selection**", on_click=AT_misc.click_sub_params_resizing)
                  
        elif resizing_selectbox == '**Center crop to square**':
              st.session_state.params_resizing_submitted = True
            
        elif resizing_selectbox == '**Center crop to power of two**':
              st.session_state.params_resizing_submitted = True

        else:
            raise('wrong resizing option selected, not implemented error')
            
        

params_resizing_submitted = st.session_state.get("params_resizing_submitted", None)
######################################

if params_resizing_submitted:
    run = st.button('**Start resizing, cropping or color rotation**' )

    placeholder = st.empty()
    if run: 
        if upload_file:
                #progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0)
                # create folder to save resized images
                #os.makedirs(os.path.join(selected_download_path_r , 'Resized_images'), exist_ok=True)
                with st.spinner("Operation in progress. Please wait and don't refresh your browser."):
                    
                    
                    name_images_pairs = []
                    
                    for n in range(len(upload_file)):
                        
                        img_PIL = Image.open(upload_file[n]).convert('RGB')
                        
                        
                        placeholder.text('Resizing image:   ' + upload_file[n].name)

                        #file_path = list_of_images_r[n]
                        if resizing_selectbox == '**Resize longer side**':
                            img_resized = resize_functions.resize_using_longer_side_kepp_aspect_ratio(img_PIL, longer_side)
                            
                        elif resizing_selectbox == '**Resize shorter side**':
                            img_resized = resize_functions.resize_using_shorter_side_kepp_aspect_ratio(img_PIL, shorter_side)
                           
                        elif resizing_selectbox == '**Resize image width**':
                            img_resized = resize_functions.resize_width_keep_aspect_ratio(img_PIL, img_width)
                           
                        elif resizing_selectbox == '**Resize image height**':
                            img_resized =  resize_functions.resize_height_keep_aspect_ratio(img_PIL, img_height)
                            
                        elif resizing_selectbox == '**Resize to fit display**':
                            img_resized = resize_functions.resize_to_fit_display(img_PIL, disp_width, disp_height)
                            
                        elif resizing_selectbox == '**Resize to number of pixel**':
                            img_resized = resize_functions.resize_to_number_of_pixels_keep_aspect_ratio(img_PIL, num_pixels)
                            
                        elif resizing_selectbox == '**Resize to fixed resolution**':
                            img_resized = resize_functions.resize_to_resolution(img_PIL, img_width, img_height)
                            
                        elif resizing_selectbox == '**Resize to Image size**':
                            img_resized = resize_functions.resize_to_image_size(img_PIL, des_img_size = des_img_size)

                        elif resizing_selectbox == '**Center crop to square**':
                            img_resized = resize_functions.center_crop (img_PIL)
                              
                        elif resizing_selectbox == '**Center crop to power of two**':
                            img_resized = resize_functions.center_crop_to_square_power_of_two (img_PIL)
                            
                        elif resizing_selectbox == '**Padding to square**':
                            img_resized = resize_functions.padding_and_resizing_to_square_X_pixel(img_PIL, resize_to=pad_resize_to)
                        
                        elif resizing_selectbox == '**Color rotaion in LAB color space**':
                            
                            img_resized = resize_functions.rotate_image_in_LAB_colorspace(img_PIL, degree=rotaion_degree)

                        else:
                            raise('wrong resizing option selected, not implemented error')

                        img_name = upload_file[n].name
                        name_images_pairs.append([img_name[:-4], img_resized])

                        my_bar.progress( int( (n+1)/len(upload_file) * 100) )

                images = resize_functions.file_process_in_memory(name_images_pairs )
                zip_file_bytes_io = io.BytesIO()
                
                with ZipFile(zip_file_bytes_io, 'w') as zip_file:
                    for image_name, bytes_stream in images:
                        zip_file.writestr(image_name+".png", bytes_stream.getvalue())



        else:
            st.write('No image files found. Load images first.')
    

    enable_download = False
    if run and upload_file:
        enable_download = True
          
    if enable_download:
        st.download_button('Download resized images', zip_file_bytes_io, file_name='resized_or_cropped_images.zip')  # Defaults to 'text/plain'
        st.success('Resizing finished.', icon="✅")
          
    
