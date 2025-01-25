#Import the required libraries
import streamlit as st
import numpy as np
from  PIL import Image
from skimage import color
import timeit
import sys
import io
from zipfile import ZipFile

from AT import balance_qips, CNN_qips, color_and_simple_qips, edge_entropy_qips, fourier_qips, fractal_dimension_qips, PHOG_qips, AT_misc

st.set_page_config(layout="wide")


version = 'v1.0.2'


AT_misc.build_heading(head=     'QIP Machine',
                      notes=    'This is an interface to calculate Quantitative Image Properties (QIPs) for images.'
                      )


st.markdown(""" <style> .font2 {
font-size:20px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .subhead {
font-size:28px ;  font-family: 'Cooper Black'; color: #FF9633;}
</style> """, unsafe_allow_html=True)


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

upload_file = st.file_uploader('Load image files', type=['jpg','jpeg','png','tif'], accept_multiple_files=True, label_visibility="collapsed", on_change=AT_misc.callback_upload_img_files )# Check to see if a  file has been uploaded


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
        st.warning('Some loaded images are quite large (more than 6 MB). Consider reducing their size, as for most QIPs the calculation time increases (exponentially) with the image resolution.', icon="⚠️")
 
    if st.session_state.get('commas', None):
        st.warning('Commas found in image filenames. This is not recommended as commas are the delimiters in the result.csv file. Commas will be replaced with underscores in the image names in the CSV file.', icon="⚠️")

 

    zip_file_name = st.text_input('Type filename for download:', value="results.zip",  help='File should have .zip extension to be recognized by standard software.' ,  label_visibility="visible")



######################################

dict_of_multi_measures = {
                    'means RGB' : ['mean R channel', 'mean G channel' , 'mean B channel (RGB)'],  
                    'means Lab' : ['mean L channel', 'mean a channel' , 'mean b channel (Lab)'],  
                    'means HSV' : ['mean H channel', 'mean S channel' , 'mean V channel'],
                    'std RGB'   : ['std R channel', 'std G channel' , 'std B channel'],
                    'std Lab'   : ['std L channel', 'std a channel' , 'std b channel (Lab)'],  
                    'std HSV'   : ['std H channel', 'std S channel' , 'std V channel'],
                    'DCM'       : ['DCM distance', 'DCM x position' , 'DCM y position'],
                    }

dict_full_names_QIPs = {
    'left-right' : 'CNN symmetry left-right',
    'up-down'    : 'CNN symmetry up-down',
    'left-right & up-down' : 'CNN symmetry left-right & up-down' ,
    '2-dimensional' : '2D Fractal dimension',
    '3-dimensional' : '3D Fractal dimension',
    'Slope'         :  'Fourier slope',
    'Sigma'         :  'Fourier sigma',
    'PHOG-based'    :  'Self-similarity (PHOG)',
    'CNN-based'     :  'Self-similarity (CNN)',
    '1st-order'     :  '1st-order EOE',
    '2nd-order'     :  '2nd-order EOE',
    }



check_dict = st.session_state.get("check_dict", None)
if upload_file:
    
    st.divider()
    
    
    ALL_QIPS = st.checkbox("Calculate all QIPs")

    
    with st.form('QIP Selection'):
        
        st.markdown("""       
        <style>
        div.stTitle {
        font-size:40px;
        }
        </style>""",unsafe_allow_html=True)
        st.markdown('<p class="subhead">Choose QIPs to calculate:</p>', unsafe_allow_html=True)
    
        
        # Define the number of columns in the layout
        num_columns = 5
        columns = st.columns(num_columns)
        check_dict = {}
        # define each column
        with columns[0]:
            st.markdown('<p class="font2">' + 'Image dimensions' + '</p>', unsafe_allow_html=True)
            check_dict['Image size (pixels)'] = st.checkbox('Image size' , help='Image size = width + height', value=ALL_QIPS)
            check_dict['Aspect ratio'] = st.checkbox('Aspect ratio' , help='Aspect ratio = width / height', value=ALL_QIPS)
            st.markdown('<p class="font2">' + 'Lightness & Complexity & Contrast' + '</p>', unsafe_allow_html=True)
            check_dict['RMS contrast'] = st.checkbox('RMS contrast', help='RMS contrast = standard deviation of the Lightness channel (Lab)', value=ALL_QIPS)
            check_dict['Lightness entropy'] = st.checkbox('Lightness entropy' , help='Lightness entropy = Shannon entropy of the Lightness channel (Lab)', value=ALL_QIPS)
            check_dict['Complexity'] = st.checkbox('Complexity', help='Complexity = mean of gradient strengths across the image (HOG method)'  , value=ALL_QIPS)
            check_dict['Edge density'] = st.checkbox('Edge density', help='Edge density = density of edges in the image (Gabor filters)'  , value=ALL_QIPS)
        with columns[1]:
            st.markdown('<p class="font2">' + 'Color' + '</p>', unsafe_allow_html=True)
            st.write('**Channel mean**')
            check_dict['means RGB'] = st.checkbox('RGB', key='mean RGB' , help='Arithmetic mean for each color channel (RGB)', value=ALL_QIPS)
            check_dict['means Lab'] = st.checkbox('Lab', key='mean Lab' , help='Arithmetic mean for each channel (Lab)' , value=ALL_QIPS)
            check_dict['means HSV'] = st.checkbox('HSV', key='mean HSV',  help='Arithmetic mean for S and V channel. Circular mean for H channel.' , value=ALL_QIPS)
            st.write('**Channel standard deviation**')
            check_dict['std RGB'] = st.checkbox('RGB',  key='std RGB', help='Standard deviation for each color channel (RGB)' , value=ALL_QIPS)
            check_dict['std Lab'] = st.checkbox('Lab',  key='std LAB', help='Standard deviation for each channel (Lab)', value=ALL_QIPS)
            check_dict['std HSV'] = st.checkbox('HSV',  key='std HSV', help='Standard deviation for S and V channel. Circular standard deviation for H channel' , value=ALL_QIPS)
            st.write('**Channel entropy**')
            check_dict['Color entropy'] =  st.checkbox('Color entropy', help='Color entropy = Shannon entropy of the Hue channel (HSV)' , value=ALL_QIPS)
        with columns[2]:
              st.markdown('<p class="font2">' + 'Symmetry & Balance' + '</p>', unsafe_allow_html=True)
              st.write('**Pixel-based**')
              check_dict['Mirror symmetry'] = st.checkbox('Mirror symmetry' , help = 'Left-right symmetry along the vertical image axis', value=ALL_QIPS)
              check_dict['Balance'] = st.checkbox('Balance', help = 'Average symmetry of the vertical, horizontal and diagonal image axes' , value=ALL_QIPS)
              check_dict['DCM'] = st.checkbox('DCM', help = 'DCM = **D**eviation of the **C**enter of **M**ass from the image center' , value=ALL_QIPS)
              st.write('**CNN feature-based symmetry**')
              check_dict['left-right'] = st.checkbox('left-right',  help = 'Left-right (vertical) symmetry of CNN layer feature maps', value=ALL_QIPS)
              check_dict['up-down'] = st.checkbox('up-down', help = 'Up-down (horizontal) symmetry of CNN layer feature maps.', value=ALL_QIPS)
              check_dict['left-right & up-down'] = st.checkbox('left-right & up-down', help = 'CNN symmetry between the original image and a left-right & up-down flipped image based on CNN-layer feature maps.', value=ALL_QIPS)
        with columns[3]:
              st.markdown('<p class="font2">' + 'Scale invariance & Self-similarity' + '</p>', unsafe_allow_html=True)
              st.write('**Fourier spectrum**')
              check_dict['Slope'] = st.checkbox('Slope', help = 'Slope of straight line fitted to log-log plot of Fourier power vs. spatial frequency', value=ALL_QIPS)
              check_dict['Sigma'] = st.checkbox('Sigma', help = 'Deviation of Fourier spectral power curve from a straight line in log-log plot', value=ALL_QIPS)
              st.write('**Fractal dimension**')
              check_dict['2-dimensional'] = st.checkbox('2-dimensional', help = '2d fractal dimension: two spatial axes for binarized image', value=ALL_QIPS)
              check_dict['3-dimensional'] = st.checkbox('3-dimensional', help = '3d fractal dimension: two spatial axes and a pixel intensity axis', value=ALL_QIPS)
              st.write('**Self-similarity**')
              check_dict['PHOG-based'] = st.checkbox('PHOG-based', help = 'Self-similarity based on pyramid of histograms of oriented gradients (PHOG)', value=ALL_QIPS)
              check_dict['CNN-based'] = st.checkbox('CNN-based', help = 'Self-similarity based on low-level features of a convolutional neural network (CNN)', value=ALL_QIPS)
        with columns[4]:
              st.markdown('<p class="font2">' + 'Feature distribution & Entropy' + '</p>', unsafe_allow_html=True)
              check_dict['Homogeneity'] = st.checkbox('Homogeneity', help = 'Relative Shannon entropy of black pixel frequency in binary image', value=ALL_QIPS)
              check_dict['Anisotropy'] = st.checkbox('Anisotropy', help ='Variance in the gradient strength across orientations (HOG method)', value=ALL_QIPS)
              st.write('**Edge-orientation entropy (EOE)**')
              check_dict['1st-order'] = st.checkbox('1st-order EOE', help = '1st-order Shannon entropy of the histogram of edge orientations across an image', value=ALL_QIPS)
              check_dict['2nd-order'] = st.checkbox('2nd-order EOE', help = '2nd-order Shannon entropy based on pairwise statistics of edge orientations across an image', value=ALL_QIPS)
              st.write('**CNN feature variance**')
              check_dict['Sparseness'] = st.checkbox('Sparseness', help = 'Total variance (Pa[n]) over all low-level CNN filter entries of all n ✕ n subregions of an image', value=ALL_QIPS)
              check_dict['Variability'] = st.checkbox('Variability', help = 'Median over the variance of entries for each CNN filter for all n ✕ n subregions of an image (Pf[n])', value=ALL_QIPS)
            
        ### always add check for gray_scale images and check for upscaling images
        check_dict['gray_scale'] = True
        check_dict['upscaled'] = True
            
        st.form_submit_button('**Commit selection**' , on_click=AT_misc.click_sub_QIPs, args=(check_dict,), use_container_width=True)

                #########################################
                ###### ADD Parameters for individual QIPs
                #########################################


if st.session_state.get("commit_qips", None):

    if  check_dict['Sparseness'] or check_dict['Variability'] or check_dict['Anisotropy'] or check_dict['Complexity'] or check_dict['PHOG-based'] or check_dict['Slope'] or check_dict['Image size (pixels)']:
           
                st.divider()

                if check_dict['Slope']:
                    st.markdown('<p class="font2">Select Type and Parameters for Fourier Slope:</p>', unsafe_allow_html=True)
                    slope_selectbox = st.radio(
                        "slope_selectbox",
                        label_visibility="collapsed",
                        options=[ '**Redies**', 
                                  '**Spehar**', 
                                  '**Mather**',],
                        
                        horizontal=True
                    )
                    
                    if slope_selectbox == '**Redies**':
                        lower_bound = int(st.text_input('Enter minimal cycles/img:', value="10",  help=None,  label_visibility="visible"))
                        upper_bound = int(st.text_input('Enter maximal cycles/img:', value="256",  help=None,  label_visibility="visible"))
                        bins = int(st.text_input('Enter width of bins:', value="2",  help=None,  label_visibility="visible"))
                    
                st.divider()
                    
                if check_dict['Image size (pixels)']:
                    st.markdown('<p class="font2">Select Type of Image size. Default is the sum of image height and width:</p>', unsafe_allow_html=True)
                    img_size_selectbox = st.radio(
                        "img_size_selectbox",
                        label_visibility="collapsed",
                        options=[ 'Sum of height and width', 
                                  'Product of height and width (number of pixels)', 
                                  'Image diagonal',
                                  'Average of height and width',
                                  'Minimum of height and width',
                                  'Maximum of height and width'],
                        
                        horizontal=True
                    )

                st.divider()

                if check_dict['Sparseness'] or check_dict['Variability']:
                    st.markdown('<p class="font2">Parameters for Sparseness and Variability:</p>', unsafe_allow_html=True)
            
                if check_dict['Sparseness']:
                    p22_Sparseness = int(st.text_input('Enter Configuration for Sparseness Measure. How many image Partitions should be used?', value="22",  help=None,  label_visibility="visible"))
                
                if check_dict['Variability']:
                    p12_Variability = int(st.text_input('Enter Configuration for Variability Measure. How many image Partitions should be used?', value="12",  help=None,  label_visibility="visible"))
                
                st.divider()

                if check_dict['Anisotropy'] or check_dict['Complexity'] or check_dict['PHOG-based']:
                    st.markdown('<p class="font2">Parameters for PHOG Measures (Complexity, Anisotropy or PHOG-based Self-similarity):</p>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                   
                    with col1:
                        PHOG_resizing = int(st.text_input('Resize images to number of pixels (-1 = no resizing):', value="-1",  help=None,  label_visibility="visible"))
                        

                        
                        bins = int(st.text_input('Number of Bins:', value="16",  help=None,  label_visibility="visible"))
                        angle = int(st.text_input('Angle:', value="360",  help=None,  label_visibility="visible"))
                    with col2:

                        levels = st.radio(
                            "Number of levels",
                            #label_visibility="visib",
                            options=[ '1', 
                                      '2', 
                                      '3',],
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
                        

                Commit_Parameter_Selection = st.button("**Commit parameter selection**")
                if Commit_Parameter_Selection:
                    st.session_state.params_submitted = Commit_Parameter_Selection
    else:
        AT_misc.click_sub_params()


counter_checked_keys = 0
run = st.session_state.get("run", None)
if st.session_state.get("params_submitted", None):

    st.divider()
    run = st.button('**Run calculation**' )
    st.session_state.run = run
     
    placeholder = st.empty()
    placeholder_QIP = st.empty()
    placeholder_remaining_time = st.empty()
    
    if run: 
        if upload_file:
            ## check if at least one QIP is selected
            for key in check_dict:
                  counter_checked_keys += check_dict[key]
            if counter_checked_keys > 0:
                # create results csv, write QIP parameters and write headings. write Notes
                
                sep = ','

                result_csv = 'sep='+sep + '\n'  # denote column seperator for Excel software
                result_csv += 'img_file,'
                
                
                for key in check_dict:
                    if check_dict[key]:
                        if key in dict_of_multi_measures:
                            for sub_key in dict_of_multi_measures[key]:
                                result_csv += sub_key + ','
                        else:
                            result_csv += dict_full_names_QIPs.get(key,key) + sep
                   
                result_csv += 'external_color_profile_found' + sep
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
                        try:
                        
                            file_name = upload_file[n].name
                            
                            if st.session_state.commas != None:
                                file_name = file_name.replace(",", "_")
                                
                            result_csv      += file_name + sep

                            
                            ### load images in different color spaces
                            img_plain_PIL = Image.open(upload_file[n])
                            img_plain_np = np.asarray(img_plain_PIL)
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
    
                            calculated_QIP = ''
                            for key in check_dict:
                                
                                if check_dict[key] and key not in ['upscaled', 'gray_scale']:
                                    calculated_QIP = key
                                
                                placeholder.text('Number of completed images: '  + str(n) + '     Number of remaining images: '  + str(num_images - (n)) )
                                placeholder_QIP.text('Calculating image: ' + file_name + '   Calculating QIP:  '  +  dict_full_names_QIPs.get(calculated_QIP, calculated_QIP))
                                placeholder_remaining_time.text( 'Remaining time: '  + expected_time_h + ' hours and  ' +  expected_time_m + ' minutes.'        )
        
                               
                                if (key == 'means RGB') and check_dict[key]:
                                    res = color_and_simple_qips.mean_channels(img_rgb)
                                    result_csv += str(AT_misc.custom_round(res[0])) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep
                                        

                                elif (key == 'means Lab') and check_dict[key]:
                                    res = color_and_simple_qips.mean_channels(img_lab)
                                    result_csv += str(AT_misc.custom_round(res[0])) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep

                                        
                                elif (key == 'means HSV') and check_dict[key]:
                                    ## get circular statistic for H channel
                                    circ_mean, _ = color_and_simple_qips.circ_stats(img_hsv)
                                    # get normal mean for S and V
                                    res = color_and_simple_qips.mean_channels(img_hsv)
                                    result_csv += str(AT_misc.custom_round(circ_mean)) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep
                                        

                                elif (key == 'std RGB') and check_dict[key]:
                                    res = color_and_simple_qips.std_channels(img_rgb)
                                    result_csv += str(AT_misc.custom_round(res[0])) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep

                                elif (key == 'std Lab') and check_dict[key]:
                                    res = color_and_simple_qips.std_channels(img_lab)
                                    result_csv += str(AT_misc.custom_round(res[0])) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep

                                elif (key == 'std HSV') and check_dict[key]:
                                    ## get circular statistic for H channel
                                    _ , circ_std = color_and_simple_qips.circ_stats(img_hsv)
                                    res = color_and_simple_qips.std_channels(img_hsv)
                                    result_csv += str(AT_misc.custom_round(circ_std)) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep
                          
    
                                elif (key == 'Color entropy') and check_dict[key]:
                                    res = color_and_simple_qips.shannonentropy_channels(img_hsv[:,:,0])
                                    result_csv += str(AT_misc.custom_round(res)) + sep

                                                              
                                elif ((key == '1st-order' ) and check_dict['1st-order']) or ((key == '2nd-order' ) and check_dict['2nd-order']) or ((key == 'Edge density' ) and check_dict['Edge density']):
                                    
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
                                        res = edge_entropy_qips.do_first_and_second_order_entropy_and_edge_density (img_gray)
                                        first_ord = res[0]
                                        sec_ord   = res[1]
                                        edge_d    = res[2]
                                        if key == '1st-order':
                                            result_csv += str(AT_misc.custom_round(first_ord)) + sep
                                        elif key == '2nd-order':
                                            result_csv += str(AT_misc.custom_round(sec_ord)) + sep
                                        elif key == 'Edge density':
                                            result_csv += str(AT_misc.custom_round(edge_d)) + sep
                                        
                                elif (key == 'Lightness entropy') and check_dict[key]:
                                    res = color_and_simple_qips.shannonentropy_channels(img_lab[:,:,0])
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    

                                elif (key == 'Image size (pixels)') and check_dict[key]:
                                                                        
                                    if img_size_selectbox == 'Sum of height and width':
                                        res = color_and_simple_qips.image_size(img_rgb, kind = 'sum')
                                        result_csv += str(AT_misc.custom_round(res)) + sep
                                        
                                    elif img_size_selectbox == 'Product of height and width (number of pixels)':
                                        res = color_and_simple_qips.image_size(img_rgb, kind = 'num_pixel')
                                        result_csv += str(AT_misc.custom_round(res)) + sep
                                        
                                    elif img_size_selectbox == 'Image diagonal':
                                        res = color_and_simple_qips.image_size(img_rgb, kind = 'diagonal')
                                        result_csv += str(AT_misc.custom_round(res)) + sep
                                        
                                    elif img_size_selectbox == 'Average of height and width':
                                        res = color_and_simple_qips.image_size(img_rgb, kind = 'average')
                                        result_csv += str(AT_misc.custom_round(res)) + sep 
                                        
                                    elif img_size_selectbox == 'Minimum of height and width':
                                        res = color_and_simple_qips.image_size(img_rgb, kind = 'minimum')
                                        result_csv += str(AT_misc.custom_round(res)) + sep 
                                        
                                    elif img_size_selectbox == 'Maximum of height and width':
                                        res = color_and_simple_qips.image_size(img_rgb, kind = 'maximum')
                                        result_csv += str(AT_misc.custom_round(res)) + sep 

                                elif (key == 'Aspect ratio') and check_dict[key]:
                                    res = color_and_simple_qips.aspect_ratio(img_rgb)
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
    
                                        sym_lr,sym_ud,sym_lrud = CNN_qips.CNN_symmetry(img_rgb, kernel, bias)
                                        if key == 'left-right':
                                            result_csv += str(AT_misc.custom_round(sym_lr)) + sep
                                        elif key == 'up-down':
                                            result_csv += str(AT_misc.custom_round(sym_ud)) + sep
                                        elif key == 'left-right & up-down':
                                            result_csv += str(AT_misc.custom_round(sym_lrud)) + sep
                                    
                                    
                                elif (key == 'Sparseness') and check_dict[key]:
                                    
                                    resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
                                    _, normalized_max_pooling_map_Sparseness  = CNN_qips.max_pooling (resp_scipy, patches=p22_Sparseness )
                                    sparseness =  CNN_qips.CNN_Variance (normalized_max_pooling_map_Sparseness   , kind='sparseness' )
                                    result_csv += str(AT_misc.custom_round(sparseness)) + sep
                              
    
                                elif (key == 'Variability') and check_dict[key]:
                                    
                                    resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
                                    _, normalized_max_pooling_map_Variability = CNN_qips.max_pooling (resp_scipy, patches=p12_Variability )
                                    variability = CNN_qips.CNN_Variance (normalized_max_pooling_map_Variability , kind='variability' )
                                    result_csv += str(AT_misc.custom_round(variability)) + sep
    
                                elif (key == 'CNN-based') and check_dict[key]:
                            
                                    resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
                                    _, normalized_max_pooling_map_8 = CNN_qips.max_pooling (resp_scipy, patches=8 )
                                    _, normalized_max_pooling_map_1 = CNN_qips.max_pooling (resp_scipy, patches=1 )
                                    cnn_self_sym = CNN_qips.CNN_selfsimilarity (normalized_max_pooling_map_1 , normalized_max_pooling_map_8 )
                                    
                                    result_csv += str(AT_misc.custom_round(cnn_self_sym)) + sep
                                    
    
                                elif ((key == 'Slope') and check_dict[key]):
                                                                        
                                    if slope_selectbox == '**Redies**':

                                        _, slope = fourier_qips.fourier_redies(img_gray, bin_size = bins, cycles_min = lower_bound, cycles_max=upper_bound)
                                        result_csv += str(AT_misc.custom_round(slope)) + sep
                                    
                                    elif slope_selectbox == '**Spehar**':
                                        slope = fourier_qips.fourier_slope_branka_Spehar_Isherwood(img_gray)
                                        
                                        result_csv += str(AT_misc.custom_round(slope)) + sep

                                    elif slope_selectbox == '**Mather**':
                                        slope = fourier_qips.fourier_slope_mather(img_rgb)
                                        result_csv += str(AT_misc.custom_round(slope)) + sep

                                elif ((key == 'Sigma') and check_dict[key]):
                                    sigma, _ = fourier_qips.fourier_redies(img_gray, bin_size = 2, cycles_min = 10, cycles_max=256)
                                    result_csv += str(AT_misc.custom_round(sigma)) + sep

                                elif (key == 'RMS contrast') and check_dict[key]:
                                    res = color_and_simple_qips.std_channels(img_lab)[0]
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                    
                                elif (key == 'Balance') and check_dict[key]:
                                    res = balance_qips.Balance(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
                                    
                                elif (key == 'DCM') and check_dict[key]:
                                    res = balance_qips.DCM(img_gray)
                                    result_csv += str(AT_misc.custom_round(res[0])) + sep
                                    result_csv += str(AT_misc.custom_round(res[1])) + sep
                                    result_csv += str(AT_misc.custom_round(res[2])) + sep
                                    
                                elif (key == 'Mirror symmetry') and check_dict[key]:
                                    res = balance_qips.Mirror_symmetry(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
                                elif (key == 'Homogeneity') and check_dict[key]:
                                    res = balance_qips.Homogeneity(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
                                elif (key == '2-dimensional') and check_dict[key]:
                                    res = fractal_dimension_qips.fractal_dimension_2d(img_gray)
                                    result_csv += str(AT_misc.custom_round(res)) + sep
    
    
                                elif (key == '3-dimensional') and check_dict[key]:
                                    res = fractal_dimension_qips.fractal_dimension_3d(img_gray)
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
                                        self_sim, complexity, anisotropy = PHOG_qips.PHOGfromImage(img_rgb, section=2, bins=bins, angle=angle, levels=int(levels), re=PHOG_resizing, sesfweight=[weigths1,weigths2,weigths3] )
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
                                    
                                    
                                    
                                    
                                    
                            ### outside of key loop
                            
                            ### check if images are upscaled, check for grayscale, always in last columns of results
                            # check for grayscale with the QIP "Color entropy"        
                            color_check = color_and_simple_qips.shannonentropy_channels(img_hsv[:,:,0])
                            if color_check < 0.01:
                                result_csv += '1' + sep
                            else:
                                result_csv += '0' + sep
                                
                            ### check for upscaled images
                            # PHOG scaling
                            upscaled = False
                            if check_dict['PHOG-based'] or check_dict['Complexity'] or check_dict['Anisotropy']:
                                if AT_misc.check_upscaling_img(img_plain_PIL, res_type='PHOG', PHOG_Pixel = PHOG_resizing):
                                    upscaled = True
                            # CNN scaling
                            if check_dict['left-right'] or check_dict['up-down'] or check_dict['left-right & up-down'] or check_dict['Sparseness']  or check_dict['Variability'] or check_dict['Sparseness'] or check_dict['CNN-based']:
                                if AT_misc.check_upscaling_img(img_plain_PIL, res_type='CNN'):
                                    upscaled = True
                                    
                            # EOE scaling
                            if check_dict['1st-order'] or check_dict['2nd-order'] or check_dict['Edge density']:
                                if AT_misc.check_upscaling_img(img_plain_PIL, res_type='EOE'):
                                    upscaled = True
                                    
                            # Fourier Scaling
                            if check_dict['Sigma'] or (check_dict['Slope'] and  (slope_selectbox == '**Redies**')):
                                if AT_misc.check_upscaling_img(img_plain_PIL, res_type='Fourier'):
                                    upscaled = True
                            
                            if upscaled:
                                result_csv += '1' + sep
                            else:
                                result_csv += '0' + sep
                                
                            ### check if images have color profile
                            if img_plain_PIL.info.get("icc_profile"):
                                st.session_state.color_profile = True
                                result_csv += '1' + sep
                            elif img_plain_PIL.info.get("icc_profile") == None:
                                result_csv += '0' + sep
                            
                            

                            ## finish line in result.csv
                            result_csv += '\n'

                            my_bar.progress( int( (n+1)/len(upload_file) * 100) )
                        except:
                            
                            file_name = upload_file[n].name
                            
                            print('An error occured', file_name)
                            
                            if st.session_state.commas != None:
                                file_name = file_name.replace(",", "_")
                                
                            result_csv += file_name + sep
                            result_csv += 'This image could not be processed. Check image properties (image may be truncated)'
                            result_csv += '\n'
                            
                            
                    placeholder.text('')

            else:
                st.write('Select QIP(s) to compute first.')       
        else:
            st.write('No image files found. Load images first.')

enable_download = False
if run and upload_file and (counter_checked_keys>0):
    enable_download = True
    
    ### write used QIP params to info csv
    params_vers_csv = 'Aesthetics Toolbox version used:'  + sep + version + '\n'
    if check_dict['Slope']:
        params_vers_csv += 'Fourier Slope Type:'  + sep + slope_selectbox + '\n' 
        if slope_selectbox == '**Redies**':
            params_vers_csv += 'Fourier Slope Redies min cycles:'  + sep + str(lower_bound) + '\n' 
            params_vers_csv += 'Fourier Slope Redies max cycles:'  + sep + str(upper_bound) + '\n' 
            params_vers_csv += 'Fourier Slope Redies width of bins:'  + sep + str(bins) + '\n'
    if check_dict['Sparseness']:
        params_vers_csv += 'Parameter for Sparseness:'  + sep + str(p22_Sparseness) + '\n'
    if check_dict['Variability']:
        params_vers_csv += 'Parameter for Variability:' + sep + str(p12_Variability) + '\n' 
    if check_dict['PHOG-based'] or check_dict['Complexity'] or check_dict['Anisotropy']:
        params_vers_csv += 'Parameter for PHOG: Resize images to number of pixels:' + sep + str(PHOG_resizing) + '\n' 
        params_vers_csv += 'Parameter for PHOG: Number of bins:' + sep + str(bins) + '\n' 
        params_vers_csv += 'Parameter for PHOG: Range of angles:' + sep + str(angle) + '\n'
        params_vers_csv += 'Parameter for PHOG: Number of levels:' + sep + str(levels) + '\n' 
        params_vers_csv += 'Parameter for PHOG: Weight Level 1:' + sep + str(weigths1) + '\n' 
        params_vers_csv += 'Parameter for PHOG: Weight Level 2:' + sep + str(weigths2) + '\n' 
        params_vers_csv += 'Parameter for PHOG: Weight Level 3:' + sep + str(weigths3) + '\n' 
    if check_dict['Image size (pixels)']:
        params_vers_csv += 'Type of Image size:'  + sep + str(img_size_selectbox) + '\n'
        
    
    zip_file_bytes_io = io.BytesIO()
    with ZipFile(zip_file_bytes_io, 'w') as zip_file:
        zip_file.writestr('QIP_results.csv', result_csv)  
        zip_file.writestr('QIP_parameters_used_and_Toolbox_version.csv', params_vers_csv)
      
if enable_download:
    if st.session_state.get('color_profile', None):
        st.warning('Some images have specific color profiles (e.g. Photoshop RGB or similar). Make sure that all your images have the same color profile as this may affect the QIP results.', icon="⚠️")
    st.success('Calculations finished. A zip file with the calculated QIPs and used parameters is ready for download.', icon="✅")
    st.download_button('Download Results', file_name=zip_file_name, data=zip_file_bytes_io)  
        
