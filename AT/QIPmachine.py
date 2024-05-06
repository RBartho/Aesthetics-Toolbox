#Import the required libraries
import streamlit as st
import numpy as np
from  PIL import Image
from skimage import color
import os
import timeit
import sys

from . import balance_sips, box_count_sips, CNN_sips, color_and_simple_sips, edge_entropy_sips, fourier_sips, PHOG_sips, scaling, AT_misc



def callback_upload_img_files():
    st.session_state.new_files_uploaded = True



def run_QIP_machine():
    #image1 = Image.open('images/logo_ukj.png')
    image2 = Image.open('images/LogoDesign EAJ final.png')
    
    #Create two columns with different width
    col1, col2 = st.columns( [0.85, 0.15])
    with col1:               # To display the header text using css style
        st.markdown('<p class="font0">QIP Machine</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">This is an interface to calculate Quantitative Image Properties (QIPs) for images</p>', unsafe_allow_html=True)
    with col2:               # To display brand logo
        st.image(image2,  width=120) 
    

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

    upload_file = st.file_uploader('Load image files', type=['jpg','png','jpeg','tif'], accept_multiple_files=True, label_visibility="collapsed", on_change=callback_upload_img_files )# Check to see if a  file has been uploaded
    
    
    if st.session_state.get('new_files_uploaded' , False): # check if upload files have been changed, and only then do checks again
        st.session_state.upload_files = upload_file
        # check for commas and large files
        st.session_state.commas = False
        for file in upload_file:
            if ',' in file.name:
                st.session_state.commas = True
            if sys.getsizeof(file) > 6e+6:
                st.session_state.large_files = True
        st.session_state.new_files_uploaded = False
        
        
    if upload_file:
        st.write('Examples of loaded images:')       
        if len(upload_file) >=20:
            st.image(upload_file[:20], width=120 )
        else:
            st.image(upload_file, width=120 )
     
        if st.session_state.get('large_files', None):
            st.warning('Some loaded images are quite large (more than 6 MB). Consider reducing their size, as for most SIPs the calculation time increases (exponentially) with the image size.', icon="⚠️")
     
        if st.session_state.get('commas', None):
            st.warning('Commas found in image filenames. This is not recommended as commas are the delimiters in the result.csv file. Commas will be replaced with underscores in the image names in the CSV file.', icon="⚠️")

        csv_name = st.text_input('Type filename for saving:', value="results.csv",  help='File should have .csv extension to be recognized by standard software.' ,  label_visibility="visible")
        
        

######################################

    dict_of_simple_color_measures = {
                        'means RGB' : ['mean R channel', 'mean G channel' , 'mean B channel (RGB)'],  
                        'means Lab' : ['mean L channel', 'mean a channel' , 'mean b channel (Lab)'],  
                        'means HSV' : ['mean H channel', 'mean S channel' , 'mean V channel'],
                        'std RGB'   : ['std R channel', 'std G channel' , 'std B channel'],
                        'std Lab'   : ['std L channel', 'std a channel' , 'std b channel (Lab)'],  
                        'std HSV'   : ['std H channel', 'std S channel' , 'std V channel'],
                        }
    
    

    check_dict = st.session_state.get("check_dict", None)
    if upload_file:
        with st.form('SIP Selection'):
            
            st.markdown("""       
            <style>
            div.stTitle {
            font-size:40px;
            }
            </style>""",unsafe_allow_html=True)
            st.markdown('<p class="font2">Choose SIPs to calculate:</p>', unsafe_allow_html=True)
        
            
            # Define the number of columns in the layout
            num_columns = 5
            columns = st.columns(num_columns)
            check_dict = {}
            # define each column
            with columns[0]:
                st.markdown('<p class="font2">' + 'Image dimensions' + '</p>', unsafe_allow_html=True)
                check_dict['Image size (pixels)'] = st.checkbox('Image size' , help='Image size = width + height')
                check_dict['Aspect ratio'] = st.checkbox('Aspect ratio' , help='Aspect ratio = width / height')
                st.markdown('<p class="font2">' + 'Luminance & Complexity & Contrast' + '</p>', unsafe_allow_html=True)
                check_dict['RMS contrast'] = st.checkbox('RMS contrast', help='RMS contrast = standard deviation of the Luminance channel (Lab)')
                check_dict['Luminance entropy'] = st.checkbox('Luminance entropy' , help='Luminance entropy = Shannon entropy of the Luminance channel (Lab)')
                check_dict['Edge density'] = st.checkbox('Edge density', help='Edge density = density of edges in the image (Gabor filters)'  )
                check_dict['Complexity'] = st.checkbox('Complexity', help='Complexity = mean of gradient strengths across the image (HOG method)'  )
            with columns[1]:
                st.markdown('<p class="font2">' + 'Color' + '</p>', unsafe_allow_html=True)
                check_dict['Color entropy'] =  st.checkbox('Color entropy', help='Color entropy = Shannon entropy of the Hue channel (HSV)'  )
                st.write('**Channel means**')
                check_dict['means RGB'] = st.checkbox('RGB', key='mean RGB' , help='Arithmetic mean for each color channel (RGB)'  )
                check_dict['means Lab'] = st.checkbox('Lab', key='mean Lab' , help='Arithmetic mean for each channel (Lab)'  )
                check_dict['means HSV'] = st.checkbox('HSV', key='mean HSV',  help='Arithmetic mean for S and V channel. Circular mean for H channel.'  )
                st.write('**Channel standard deviation**')
                check_dict['std RGB'] = st.checkbox('RGB',  key='std RGB', help='Standard deviation for each color channel (RGB)'  )
                check_dict['std Lab'] = st.checkbox('Lab',  key='std LAB', help='Standard deviation for each channel (Lab)'  )
                check_dict['std HSV'] = st.checkbox('HSV',  key='std HSV', help='Standard deviation for S and V channel. Circular standard deviation for H channel'  )
            with columns[2]:
                  st.markdown('<p class="font2">' + 'Symmetry & Balance' + '</p>', unsafe_allow_html=True)
                  st.write('**Pixel-based**')
                  check_dict['Mirror symmetry'] = st.checkbox('Mirror symmetry' , help = 'Left-right symmetry along the vertical image axis')
                  check_dict['DCM'] = st.checkbox('DCM', help = 'DCM = **D**eviation of the **C**enter of **M**ass from the image center'  )
                  check_dict['Balance'] = st.checkbox('Balance', help = 'Average symmetry of the vertical, horizontal and diagonal image axes'  )
                  st.write('**CNN-feature-based**')
                  check_dict['left-right'] = st.checkbox('left-right',  help = 'Left-right (vertical) symmetry of CNN layer feature maps')
                  check_dict['up-down'] = st.checkbox('up-down', help = 'Up-down (horizontal) symmetry of CNN layer feature maps.')
                  check_dict['left-right & up-down'] = st.checkbox('left-right & up-down', help = 'CNN symmetry betwenn the original image and a left-right & up-down flipped image based on CNN-layer feature maps.')
            with columns[3]:
                  st.markdown('<p class="font2">' + 'Fractality & Self-similarity' + '</p>', unsafe_allow_html=True)
                  st.write('**Fractal dimension**')
                  check_dict['2-dimensional'] = st.checkbox('2-dimensional', help = '2d fractal dimension: two spatial axes for binarized image')
                  check_dict['3-dimensional'] = st.checkbox('3-dimensional', help = '3d fractal dimension: two spatial axes and a pixel intensity axis')
                  st.write('**Fourier spectrum**')
                  check_dict['Slope'] = st.checkbox('Slope', help = 'Slope of straight line fitted to log-log plot of Fourier power vs. spatial frequency')
                  check_dict['Sigma'] = st.checkbox('Sigma', help = 'Deviation of Fourier spectral power curve from a straight line in log-log plot')
                  st.write('**Self-similarity**')
                  check_dict['PHOG-based'] = st.checkbox('PHOG-based', help = 'Self-similarity based on pyramid of histograms of oriented gradients (PHOG)')
                  check_dict['CNN-based'] = st.checkbox('CNN-based', help = 'Self-similarity based on low-level features of a convolutional neural network (CNN)')
            with columns[4]:
                  st.markdown('<p class="font2">' + 'Feature distribution & Entropy' + '</p>', unsafe_allow_html=True)
                  check_dict['Anisotropy'] = st.checkbox('Anisotropy', help ='Variance in the gradient strength across orientations (HOG method)')
                  check_dict['Homogeneity'] = st.checkbox('Homogeneity', help = 'Relative Shannon entropy of black pixel frequency in image bins')
                  st.write('**Edge orientation entropy**')
                  check_dict['1st-order'] = st.checkbox('1st-order', help = '1st-order Shannon entropy of the histogram of edge orientations across an image')
                  check_dict['2nd-order'] = st.checkbox('2nd-order', help = '2nd-order Shannon entropy based on pairwise statistics of edge orientations across an image')
                  st.write('**CNN feature variance**')
                  check_dict['Sparseness'] = st.checkbox('Sparseness', help = 'Total variance (Pa[n]) over all low-level CNN filter entries of all n ✕ n subregions of an image')
                  check_dict['Variability'] = st.checkbox('Variability', help = 'Median over the variance of entries for each CNN filter for all n ✕ n subregions of an image (Pf[n])')
                
            st.form_submit_button('**Commit selection**' , on_click=AT_misc.click_sub_SIPs, args=(check_dict,), use_container_width=True)

                    #########################################
                    ###### ADD Parameters for individual SIPs
                    #########################################
        
    
    if st.session_state.get("commit_sips", None):

        if  check_dict['Sparseness'] or check_dict['Variability'] or check_dict['Anisotropy'] or check_dict['Complexity'] or check_dict['PHOG-based'] or check_dict['Slope']:
                #with st.form('Param Selection'):
                    if check_dict['Slope']:
                        st.markdown('<p class="font2">Select Type and Parameters for Fourier Slope:</p>', unsafe_allow_html=True)
                        slope_selectbox = st.radio(
                            "slope_selectbox",
                            label_visibility="collapsed",
                            options=['**Redies**', 
                                      '**Spehar**', 
                                      '**Mather**',],
                            captions = ["", 
                                        "", 
                                        "",],
                            horizontal=True
                        )
                        
                        if slope_selectbox == '**Redies**':
                            lower_bound = int(st.text_input('Enter minimal cycles/img:', value="10",  help=None,  label_visibility="visible"))
                            upper_bound = int(st.text_input('Enter maximal cycles/img:', value="256",  help=None,  label_visibility="visible"))
                            bins = int(st.text_input('Enter width of bins:', value="2",  help=None,  label_visibility="visible"))
                        
                            
                        if slope_selectbox == '**Spehar**':
                            bins = int(st.text_input('Enter number of bins:', value="100",  help=None,  label_visibility="visible"))
                            low_cut = int(st.text_input('Enter percent of lower frequencies to drop:', value="2",  help=None,  label_visibility="visible"))
    
                    if check_dict['Sparseness'] or check_dict['Variability']:
                        st.markdown('<p class="font2">Parameters for Sparseness and Variability:</p>', unsafe_allow_html=True)
                
                    if check_dict['Sparseness']:
                        p22_Sparseness = int(st.text_input('Enter Configuration for Sparseness Measure. How many image Partitions should be used?', value="22",  help=None,  label_visibility="visible"))
                    
                    if check_dict['Variability']:
                        p12_Variability = int(st.text_input('Enter Configuration for Variability Measure. How many image Partitions should be used?', value="12",  help=None,  label_visibility="visible"))
                    

                    if check_dict['Anisotropy'] or check_dict['Complexity'] or check_dict['PHOG-based']:
                        st.markdown('<p class="font2">Parameters for PHOG Measures (Complexity, Anisotropy or PHOG-based Self-similarity):</p>', unsafe_allow_html=True)
                        
                        col1, col2 = st.columns(2)
                       
                        with col1:
                            re = int(st.text_input('Resize images to number of pixels (-1 = no resizing):', value="-1",  help=None,  label_visibility="visible"))
                            
                            
                            bins = int(st.text_input('Number of Bins:', value="16",  help=None,  label_visibility="visible"))
                            angle = int(st.text_input('Angle:', value="360",  help=None,  label_visibility="visible"))
                        with col2:
                            #levels = int(st.text_input('Number of levels:', value="3",  help=None,  label_visibility="visible"))
                            
                            levels = st.radio(
                                "Number of levels",
                                #label_visibility="visib",
                                options=[ '1', 
                                          '2', 
                                          '3',],
                                captions = ["", 
                                            "", 
                                            "",],
                                horizontal=True,
                                index=2
                            )
                            
                            col2a, col2b, col2c = st.columns(3)
                            with col2a:
                                weigths1 = int(st.text_input('Weights for level1:', value=1,  help=None,  label_visibility="visible"))
                            with col2b: 
                                weigths2 = int(st.text_input('Weights for level2:', value=1,  help=None,  label_visibility="visible"))
                            with col2c:
                                weigths3 = int(st.text_input('Weights for level3:', value=1,  help=None,  label_visibility="visible"))
                            
                    #st.form_submit_button("**Commit Parameter Selection**", on_click=click_sub_params())
                    
                    Commit_Parameter_Selection = st.button("**Commit parameter selection**")
                    if Commit_Parameter_Selection:
                        st.session_state.params_submitted = Commit_Parameter_Selection
        else:
            AT_misc.click_sub_params()


    counter_checked_keys = 0
    run = st.session_state.get("run", None)
    if st.session_state.get("params_submitted", None):

        run = st.button('**Run calculation**' )
        st.session_state.run = run
         
        placeholder = st.empty()
        placeholder_remaining_time = st.empty()
        
        if run: 
            if upload_file:
                ## check if at least one SIP is selected
                for key in check_dict:
                      counter_checked_keys += check_dict[key]
                if counter_checked_keys > 0:
                    # create output csv and write headings

                    result_csv = 'img_file,'
                    sep = ','
                    
                    for key in check_dict:
                        if check_dict[key]:
                            if key in dict_of_simple_color_measures:
                                for sub_key in dict_of_simple_color_measures[key]:
                                    result_csv += sub_key + ','
                            else:
                                ### get full names for indivual measures
                                if key == 'left-right':
                                    result_csv += 'CNN symmetry left-right' + sep
                                elif key == 'up-down':
                                    result_csv += 'CNN symmetry up-down' + sep
                                elif key == 'left-right & up-down':
                                    result_csv += 'CNN symmetry left-right & up-down' + sep
                                elif key == '2-dimensional':
                                    result_csv += '2D Fractal dimension' + sep
                                elif key == '3-dimensional':
                                    result_csv += '3D Fractal dimension' + sep
                                elif key == 'Slope':
                                    result_csv += 'Fourier slope' + sep   
                                elif key == 'Sigma':
                                    result_csv += 'Fourier sigma' + sep
                                elif key == 'PHOG-based':
                                    result_csv += 'Self-similarity (PHOG)' + sep                         
                                elif key == 'CNN-based':
                                    result_csv += 'Self-similarity (CNN)' + sep  
                                elif key == '1st-order':
                                    result_csv += '1st-order EOE' + sep
                                elif key == '2nd-order':
                                    result_csv += '2nd-order EOE' + sep
                                else:   
                                    result_csv += key + sep
                    result_csv = result_csv[:-1] + '\n'   
                
                    ### load values for CNN kernel and bias
                    [kernel,bias] = np.load(open("AT/bvlc_alexnet_conv1.npy", "rb"), encoding="latin1", allow_pickle=True)
                            
                    #progress_text = "Operation in progress. Please wait."
                    my_bar = st.progress(0)
                    
                    
                    
                    with st.spinner("Operation in progress. Please wait and don't refresh your browser."):
                    
                        num_images = len(upload_file)
                        start = timeit.default_timer()
                        expected_time_h = "..."
                        expected_time_m = "..."
                        for n in range(num_images):
                            
                            file_name = upload_file[n].name
                            
                            placeholder.text('Number of completed images: '  + str(n) + '    Number of remaining images: '  + str(num_images - (n+1)) + '     Calculating image: ' + file_name)
                            placeholder_remaining_time.text( 'Remaining time: '  + expected_time_h + ' hours and  ' +  expected_time_m + ' minuits.'        )
    

                            if st.session_state.commas != None:
                                file_name = file_name.replace(",", "_")
                                
                            result_csv += file_name + sep
                         
                            
                            ### load images in different color spaces
                            img_plain_PIL = Image.open(upload_file[n])
                            img_plain_np = np.asarray(img_plain_PIL)
                            
                            ### Check for grayscale image, skip calculating color features for grayscale images  later
                            gray_scale_img = False
                            if len(img_plain_np.shape) == 2:
                                gray_scale_img = True
                                
                            img_rgb = np.asarray(img_plain_PIL.convert('RGB'))
                            img_lab = color.rgb2lab(img_rgb)
                            img_hsv = color.rgb2hsv(img_rgb)
                            img_gray = np.asarray(Image.open(upload_file[n]).convert('L'))  ## color uses range [0-1], PIL uses Range [0-256] for intensity
                
                
                            # temp vals for edge entropy
                            first_ord = None
                            sec_ord   = None
                            edge_d    = None
                            # temp vals for CNN symmetry
                            sym_lr   = None
                            sym_ud   = None
                            sym_lrud = None
                            # temp vals for Fourier vals
                            sigma  = None
                            slope = None 
                            # temp vals for PHOG
                            self_sim = None
                            complexity = None
                            anisotropy = None
    
                            for key in check_dict:
                               
                                if (key == 'means RGB') and check_dict[key]:
                                    if gray_scale_img == False:
                                        res = color_and_simple_sips.mean_channels(img_rgb)
                                        result_csv += str(AT_misc.custom_round(res[0])) + sep
                                        result_csv += str(AT_misc.custom_round(res[1])) + sep
                                        result_csv += str(AT_misc.custom_round(res[2])) + sep
                                        
                                    else:
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep

                                elif (key == 'means Lab') and check_dict[key]:
                                    if gray_scale_img == False:
                                        res = color_and_simple_sips.mean_channels(img_lab)
                                        result_csv += str(AT_misc.custom_round(res[0])) + sep
                                        result_csv += str(AT_misc.custom_round(res[1])) + sep
                                        result_csv += str(AT_misc.custom_round(res[2])) + sep
                                    else:
                                        res = color_and_simple_sips.mean_channels(img_lab)
                                        result_csv += str(AT_misc.custom_round(res[0])) + sep
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                        
                                elif (key == 'means HSV') and check_dict[key]:
                                    if gray_scale_img == False:
                                        ## get circular statistic for H channel
                                        circ_mean, _ = color_and_simple_sips.circ_stats(img_hsv)
                                        # get normal mean for S and V
                                        res = color_and_simple_sips.mean_channels(img_hsv)
                                        result_csv += str(AT_misc.custom_round(circ_mean)) + sep
                                        result_csv += str(AT_misc.custom_round(res[1])) + sep
                                        result_csv += str(AT_misc.custom_round(res[2])) + sep
                                        
                                        
                                    else:
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
    
                                
                                elif (key == 'std RGB') and check_dict[key]:
                                    res = color_and_simple_sips.std_channels(img_rgb)
                                    if gray_scale_img == False:
                                        result_csv += str(AT_misc.custom_round(res[0])) + sep
                                        result_csv += str(AT_misc.custom_round(res[1])) + sep
                                        result_csv += str(AT_misc.custom_round(res[2])) + sep
                                    else:
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                
                                elif (key == 'std Lab') and check_dict[key]:
                                    if gray_scale_img == False:
                                        res = color_and_simple_sips.std_channels(img_lab)
                                        result_csv += str(AT_misc.custom_round(res[0])) + sep
                                        result_csv += str(AT_misc.custom_round(res[1])) + sep
                                        result_csv += str(AT_misc.custom_round(res[2])) + sep
                                    else:
                                        res = color_and_simple_sips.std_channels(img_lab)
                                        result_csv += str(AT_misc.custom_round(res[0])) + sep
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                    

                                elif (key == 'std HSV') and check_dict[key]:
                                    if gray_scale_img == False:
                                        ## get circular statistic for H channel
                                        _ , circ_std = color_and_simple_sips.circ_stats(img_hsv)
                                        res = color_and_simple_sips.std_channels(img_hsv)
                                        result_csv += str(AT_misc.custom_round(circ_std)) + sep
                                        result_csv += str(AT_misc.custom_round(res[1])) + sep
                                        result_csv += str(AT_misc.custom_round(res[2])) + sep
                                    else:
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
                                        result_csv += 'grayscale' + sep
    
    
                                elif (key == 'Color entropy') and check_dict[key]:
                                    if gray_scale_img == False:
                                        res = color_and_simple_sips.shannonentropy_channels(img_hsv[:,:,0])
                                        result_csv += str(AT_misc.custom_round(res)) + sep
                                    else:
                                        result_csv += 'grayscale' + sep
                                    
                                        
                                                              
                                elif ((key == '1st-order') and check_dict[key]) or ((key == '2nd-order') and check_dict[key]) or ((key == 'Edge density') and check_dict[key]):
                                    
                                    # if already first or second order entropy has been calculated
                                    if first_ord != None:
                                        
                                        if key == '1st-order':
                                            result_csv += str(AT_misc.custom_round(first_ord)) + sep
                                        elif key == '2nd-order':
                                            result_csv += str(AT_misc.custom_round(sec_ord)) + sep
                                        elif key == 'Edge density':
                                            result_csv += str(AT_misc.custom_round(edge_d)) + sep
                                            
                                    # if not jet calculated, calculate both
                                    else:
                                        res = edge_entropy_sips.do_first_and_second_order_entropy_and_edge_density (img_gray)
                                        first_ord = res[0]
                                        sec_ord   = res[1]
                                        edge_d    = res[2]
                                        if key == '1st-order':
                                            result_csv += str(AT_misc.custom_round(first_ord)) + sep
                                        elif key == '2nd-order':
                                            result_csv += str(AT_misc.custom_round(sec_ord)) + sep
                                        elif key == 'Edge density':
                                            result_csv += str(AT_misc.custom_round(edge_d)) + sep
                                        
                                elif (key == 'Luminance entropy') and check_dict[key]:
                                    res = color_and_simple_sips.shannonentropy_channels(img_lab[:,:,0])
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                elif (key == 'Image size (pixels)') and check_dict[key]:
                                    res = color_and_simple_sips.image_size(img_rgb)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
                                    
                                elif (key == 'Aspect ratio') and check_dict[key]:
                                    res = color_and_simple_sips.aspect_ratio(img_rgb)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                elif ((key == 'left-right') and check_dict[key]) or ((key == 'up-down') and check_dict[key]) or ((key == 'left-right & up-down') and check_dict[key]):
                                    
    
                                    # if one CNN sym has already been calculated, the others have been calculated as well
                                    if sym_lr != None:

                                        if key == 'left-right':
                                            result_csv += str(AT_misc.custom_round(sym_lr)) + sep
                                        elif key == 'up-down':
                                            result_csv += str(AT_misc.custom_round(sym_ud)) + sep
                                        elif key == 'left-right & up-down':
                                            result_csv += str(AT_misc.custom_round(sym_lrud)) + sep
                                            
                                    # if not jet calculated, calculate all syms together and store results
                                    else:
    
                                        sym_lr,sym_ud,sym_lrud = CNN_sips.get_symmetry(img_rgb, kernel, bias)
                                        if key == 'left-right':
                                            result_csv += str(AT_misc.custom_round(sym_lr)) + sep
                                        elif key == 'up-down':
                                            result_csv += str(AT_misc.custom_round(sym_ud)) + sep
                                        elif key == 'left-right & up-down':
                                            result_csv += str(AT_misc.custom_round(sym_lrud)) + sep
                                    
                                    
                                elif (key == 'Sparseness') and check_dict[key]:
                                    
                                    resp_scipy = CNN_sips.conv2d(img_rgb, kernel, bias)
                                    _, normalized_max_pooling_map_Sparseness  = CNN_sips.max_pooling (resp_scipy, patches=p22_Sparseness )
                                    sparseness =  CNN_sips.get_CNN_Variance (normalized_max_pooling_map_Sparseness   , kind='sparseness' )
                                    result_csv += str(AT_misc.custom_round(sparseness)) + sep
                              
    
                                elif (key == 'Variability') and check_dict[key]:
                                    
                                    resp_scipy = CNN_sips.conv2d(img_rgb, kernel, bias)
                                    _, normalized_max_pooling_map_Variability = CNN_sips.max_pooling (resp_scipy, patches=p12_Variability )
                                    variability = CNN_sips.get_CNN_Variance (normalized_max_pooling_map_Variability , kind='variability' )
                                    result_csv += str(AT_misc.custom_round(variability)) + sep
    
                                elif (key == 'CNN-based') and check_dict[key]:
                                    img_switch_channel = img_rgb[:,:,(2,1,0)].astype(np.float32)
                                    resp_scipy = CNN_sips.conv2d(img_switch_channel, kernel, bias)
                                    _, normalized_max_pooling_map_8 = CNN_sips.max_pooling (resp_scipy, patches=8 )
                                    _, normalized_max_pooling_map_1 = CNN_sips.max_pooling (resp_scipy, patches=1 )
                                    cnn_self_sym = CNN_sips.get_selfsimilarity (normalized_max_pooling_map_1 , normalized_max_pooling_map_8 )
                                    
                                    result_csv += str(AT_misc.custom_round(cnn_self_sym)) + sep
                                    
    
                                elif ((key == 'Slope') and check_dict[key]):
                                                                        
                                    if slope_selectbox == '**Redies**':

                                        _, slope = fourier_sips.fourier_redies(img_gray, bin_size = bins, cycles_min = lower_bound, cycles_max=upper_bound)
                                        #_, slope = fourier_sips.fourier_sigma(img_lab[:,:,0])
                                        result_csv += str(AT_misc.custom_round(slope)) + sep
                                    
                                    elif slope_selectbox == '**Spehar**':
                                        slope = fourier_sips.fourier_slope_branka_Spehar(img_gray, nbins=bins, lowcut=low_cut)
                                        result_csv += str(AT_misc.custom_round(slope)) + sep

                                    elif slope_selectbox == '**Mather**':
                                        slope = fourier_sips.fourier_slope_mather(img_rgb)
                                        result_csv += str(AT_misc.custom_round(slope)) + sep

                                elif ((key == 'Sigma') and check_dict[key]):
                                    sigma, _ = fourier_sips.fourier_redies(img_gray, bin_size = 2, cycles_min = 30, cycles_max=256)
                                    result_csv += str(AT_misc.custom_round(sigma)) + sep

                                elif (key == 'RMS contrast') and check_dict[key]:
                                    res = color_and_simple_sips.std_channels(img_lab)[0]
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                    
                                elif (key == 'Balance') and check_dict[key]:
                                    res = balance_sips.APB_Score(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                elif (key == 'DCM') and check_dict[key]:
                                    res = balance_sips.DCM_Key(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                elif (key == 'Mirror symmetry') and check_dict[key]:
                                    res = balance_sips.MS_Score(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
                                elif (key == 'Homogeneity') and check_dict[key]:
                                    res = balance_sips.entropy_score_2d(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
                                elif (key == '2-dimensional') and check_dict[key]:
                                    res = box_count_sips.box_count_2d(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
    
                                elif (key == '3-dimensional') and check_dict[key]:
                                    res = box_count_sips.custom_differential_box_count(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep

                               
                                ### PHOG
                                elif ((key == 'PHOG-based') and check_dict[key]) or ((key == 'Complexity') and check_dict[key]) or ((key == 'Anisotropy') and check_dict[key]):
                                    
                                    # if one PHOG measure has already been calculated, the others have been calculated as well
                                    if self_sim != None:
                                        if key == 'PHOG-based':
                                            result_csv += str(AT_misc.custom_round(self_sim)) + sep
                                        elif key == 'Complexity':
                                            result_csv += str(AT_misc.custom_round(complexity)) + sep
                                        elif key == 'Anisotropy':
                                            result_csv += str(AT_misc.custom_round(anisotropy)) + sep
                                                     
                                    else:
                                        self_sim, complexity, anisotropy = PHOG_sips.PHOGfromImage(img_rgb, section=2, bins=bins, angle=angle, levels=int(levels), re=re, sesfweight=[weigths1,weigths2,weigths3] )
                                        if key == 'PHOG-based':
                                            result_csv += str(AT_misc.custom_round(self_sim)) + sep
                                        elif key == 'Complexity':
                                            result_csv += str(AT_misc.custom_round(complexity)) + sep
                                        elif key == 'Anisotropy':
                                            result_csv += str(AT_misc.custom_round(anisotropy)) + sep
                                            
                                ### predict remaining time
                                
                                if n < 3:
                                    expected_time_h = "..."
                                    expected_time_m = "..."
                                else:
                                    stop = timeit.default_timer()
                                    
                                    temp_time = int( np.round( ((stop - start)/n) * (num_images - n)/60  )) 
                                    
                                    expected_time_h = str(  temp_time // 60  )
                                    expected_time_m = str(  temp_time % 60  )
                                    
                                    
                            result_csv += '\n'
                            # with open(csv_save_path, 'a') as log:
                            #     log.write('\n')   
                                
                            #my_bar.progress((n+1)* int(100 / (len(upload_file)))  )
                            my_bar.progress( int( (n+1)/len(upload_file) * 100) )
                        placeholder.text('')
    
                else:
                    st.write('Select SIP(s) to compute first.')       
            else:
                st.write('No image files found. Load images first.')
        
        
    

    enable_download = False
    if run and upload_file and (counter_checked_keys>0):
        enable_download = True
        download_file = result_csv
          
    if enable_download:
        st.success('Calculations finished. A csv-file has been created in your selected results folder.', icon="✅")
        
        st.download_button('Download Results', download_file, file_name=csv_name)  # Defaults to 'text/plain'
        