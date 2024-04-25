#Import the required Libraries
import streamlit as st
import numpy as np
from  PIL import Image
from skimage import color
import sys

### custom import
from SIPmachine import balance_sips, box_count_sips, CNN_sips, color_and_simple_sips, edge_entropy_sips, fourier_sips, PHOG_sips


###################### TODO's

# finish image resize option --> seperate window

# add parameters for Slope und drei Slope version zusammenbringen/zusammenbringbar?

# Gitlab automatic Code Tests

# Minifehler in Code kommentieren, Richtige Version auskommentieren

### Anleitung
# How to stop the program
# clear function for image upload?
    

# fix the names in result txt


## change seperator to ';'



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



### functions to update session state
def selected_SIPs():
    st.session_state["stage"] = "SIPs_selected"
    
def selected_Params():
    st.session_state["stage"] = "Params_selected"



st.set_page_config(layout="wide")


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

app_mode = st.sidebar.selectbox('Select Page',['SIP Calculation','Documentation', 'References'] ) #three pages
   
if app_mode == 'SIP Calculation':
    
    st.markdown(""" <style> .font0 {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    
    st.markdown(""" <style> .font1 {
    font-size:20px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    
    st.markdown(""" <style> .font2 {
    font-size:20px ; font-family: 'Cooper Black'; color: green;} 
    </style> """, unsafe_allow_html=True)

    
    image1 = Image.open('images/logo_ukj.png')
    image2 = Image.open('images/LogoDesign EAJ final.png')
    
    #Create two columns with different width
    col1, col2, col3 = st.columns( [0.7, 0.15, 0.15])
    with col1:               # To display the header text using css style
        st.markdown('<p class="font0">SIP Machine</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">This is a web app to calculate Statistical Image Properties (SIPs) for images</p>', unsafe_allow_html=True)
    with col2:               # To display brand logo
        st.image(image1,  width=150) 
    with col3:               # To display brand logo
        st.image(image2,  width=120) 
    

    upload_file = st.file_uploader('Load image files (Images are only loaded to your local machine. They are not uploaded to the internet)', type=['jpg','png','jpeg'], accept_multiple_files=True, label_visibility="collapsed" )# Check to see if a  file has been uploaded

    # st.markdown('''
    #     <style>
    #         .uploadedFile {display: none}
    #     <style>''',
    #     unsafe_allow_html=True)


    if len(upload_file) != 0 :
        st.write('Examples of loaded images:')       
        st.image(upload_file[:20], width=120 )

## check for large files and for commas in filenames
    
    has_large_image_files = False
    has_comma = False
    for file in upload_file:
        if ',' in file.name:
            has_comma = True
        if sys.getsizeof(file) > 4e+6:
            has_large_image_files = True
        
    if has_large_image_files:
        st.warning('Some loaded images are quite large (more than 4 MB). Consider reducing their size, as for most SIPs the calculation time increases (exponentially) with the image size.', icon="⚠️")


    replace_commas = False
    if has_comma:
        st.warning('Commas found in image filenames. This is not recommended as commas are the delimiters in the downloaded CSV file containing the results. Replace the commas with underscores in the image names in the CSV file?', icon="⚠️")
        replace_commas = st.checkbox('Replace commas with underscores.')

    
######################################

    dict_of_simple_color_measures = {
                        'means RGB' : ['mean R channel', 'mean G channel' , 'mean (RG)B channel'],  
                        'means LAB' : ['mean L channel', 'mean A channel' , 'mean (LA)B channel'],  
                        'means HSV' : ['mean H channel', 'mean S channel' , 'mean V channel'],
                        'std RGB'   : ['std R channel', 'std G channel' , 'std (RG)B channel'],
                        'std LAB'   : ['std L channel', 'std A channel' , 'std (LA)B channel'],  
                        'std HSV'   : ['std H channel', 'std S channel' , 'std V channel'],
                        }
    
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
            check_dict['means LAB'] = st.checkbox('Lab', key='mean Lab' , help='Arithmetic mean for each channel (Lab)'  )
            check_dict['means HSV'] = st.checkbox('HSV', key='mean HSV',  help='Arithmetic mean for S and V channel. Circular mean for H channel.'  )
            st.write('**Channel standard deviation**')
            check_dict['std RGB'] = st.checkbox('RGB',  key='std RGB', help='Standard deviation for each color channel (RGB)'  )
            check_dict['std LAB'] = st.checkbox('Lab',  key='std LAB', help='Standard deviation for each channel (Lab)'  )
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
             check_dict['Anisotropy'] = st.checkbox('Anisotropy', help ='Difference in the strength of the gradients across orientations')
             check_dict['Homogeneity'] = st.checkbox('Homogeneity', help = 'Relative Shannon entropy of black pixel frequency in image bins')
             st.write('**Edge orientation entropy**')
             check_dict['1st-order'] = st.checkbox('1st-order', help = '1st-order Shannon entropy of the histogram of edge orientations across an image')
             check_dict['2nd-order'] = st.checkbox('2nd-order', help = '2nd-order Shannon entropy based on pairwise statistics of edge orientations across an image')
             st.write('**CNN feature variance**')
             check_dict['Sparseness'] = st.checkbox('Sparseness', help = 'Total variance (Pa[n]) over all low-level CNN filter entries of all n ✕ n subregions of an image')
             check_dict['Variability'] = st.checkbox('Variability', help = 'Median over the variance of entries for each CNN filter for all n ✕ n subregions of an image (Pf[n])')
            
        commit_sips = st.form_submit_button('**Commit selection**' , on_click =  selected_SIPs() )
            
                #########################################
                ###### ADD Parameters for individual SIPs
                #########################################
        
    

    if  check_dict['Sparseness'] or check_dict['Variability'] or check_dict['Anisotropy'] or check_dict['Complexity'] or check_dict['PHOG-based']:
        if st.session_state["stage"] == "SIPs_selected":
            with st.form('Param Selection'):

                if check_dict['Sparseness'] or check_dict['Variability']:
                    st.markdown('<p class="font2">Parameters for Sparseness and Variability:</p>', unsafe_allow_html=True)
            
                if check_dict['Sparseness']:
                    p22_Sparseness = int(st.text_input('Enter Configuration for Sparseness Measure. How many image Partitions should be used?:', value="22",  help=None,  label_visibility="visible"))
                
                if check_dict['Variability']:
                    p12_Variability = int(st.text_input('Enter Configuration for Variability Measure. How many image Partitions should be used?:', value="12",  help=None,  label_visibility="visible"))
                
                if check_dict['Anisotropy'] or check_dict['Complexity'] or check_dict['PHOG-based']:
                    st.markdown('<p class="font2">Parameters for PHOG Measures (Complexity, Anisotropy or PHOG-based Self-similarity):</p>', unsafe_allow_html=True)
                    
                    col1, col2 = st.columns(2)
                   
                    with col1:
                        re = int(st.text_input('Scale images to Number of Pixels (-1 = no scaling):', value="100000",  help=None,  label_visibility="visible"))
                        
                        
                        bins = int(st.text_input('Number of Bins:', value="16",  help=None,  label_visibility="visible"))
                        angle = int(st.text_input('Angle:', value="360",  help=None,  label_visibility="visible"))
                    with col2:
                        section = int(st.text_input('Number of Sections:', value="2",  help=None,  label_visibility="visible"))
                        levels = int(st.text_input('Number of levels:', value="3",  help=None,  label_visibility="visible"))
                        
                        col2a, col2b, col2c = st.columns(3)
                        with col2a:
                            weigths1 = int(st.text_input('Weights for level1:', value=1,  help=None,  label_visibility="visible"))
                        with col2b: 
                            weigths2 = int(st.text_input('Weights for level2:', value=1,  help=None,  label_visibility="visible"))
                        with col2c:
                            weigths3 = int(st.text_input('Weights for level3:', value=1,  help=None,  label_visibility="visible"))
                        
                submitted = st.form_submit_button("**Commit Parameter Selection**", on_click=selected_Params())
                


    run = st.button('**Run calculation**' )
    
    counter_checked_keys = 0
    placeholder = st.empty()
    if run: 
    
        if len(upload_file) != 0 :
            ## check if at least one SIP is selected
            
            for key in check_dict:
                 counter_checked_keys += check_dict[key]
            if counter_checked_keys > 0:
                print('##############################')
                # create output txt and write headings
                result_txt = 'img_file,'
                for key in check_dict:
                    if check_dict[key]:
                        if key in dict_of_simple_color_measures:
                            for sub_key in dict_of_simple_color_measures[key]:
                                result_txt = result_txt + sub_key + ','
                        else:
                            result_txt = result_txt + key + ','          
                result_txt = result_txt[:-1] + '\n'
            
                ### load values for CNN kernel and bias
                [kernel,bias] = np.load(open("bvlc_alexnet_conv1.npy", "rb"), encoding="latin1", allow_pickle=True)
                        
                #progress_text = "Operation in progress. Please wait."
                my_bar = st.progress(0)
                
                
                
                with st.spinner("Operation in progress. Please wait. Download button will appear when finished"):
                
                    for n in range(len(upload_file)):
                        
                        placeholder.text('Calculation for image:   ' + upload_file[n].name)

                        file_name = str(upload_file[n].name)
                        if replace_commas:
                            file_name = file_name.replace(",", "_")
                        result_txt = result_txt + str(file_name) + ','
                        
                                   
                        img_rgb = np.asarray(Image.open(upload_file[n]).convert('RGB'))
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
                            if check_dict[key]:
                                print(key)
                            
                            
                            if (key == 'means RGB') and check_dict[key]:
                                res = color_and_simple_sips.mean_channels(img_rgb)
                                result_txt = result_txt + str(custom_round(res[0])) + ','
                                result_txt = result_txt + str(custom_round(res[1])) + ','
                                result_txt = result_txt + str(custom_round(res[2])) + ','
                                # print('Hello:'  , result_txt)
                            
                            elif (key == 'means LAB') and check_dict[key]:
                                res = color_and_simple_sips.mean_channels(img_lab)
                                result_txt = result_txt + str(custom_round(res[0])) + ','
                                result_txt = result_txt + str(custom_round(res[1])) + ','
                                result_txt = result_txt + str(custom_round(res[2])) + ','
                                # print('Hello:'  , result_txt)
                                
                            elif (key == 'means HSV') and check_dict[key]:
                                ## get circular statistic for H channel
                                circ_mean, _ = color_and_simple_sips.circ_stats(img_hsv)
                                result_txt = result_txt + str(custom_round(circ_mean)) + ','
                                # get normal mean for S and V
                                res = color_and_simple_sips.mean_channels(img_hsv)
                                result_txt = result_txt + str(custom_round(res[1])) + ','
                                result_txt = result_txt + str(custom_round(res[2])) + ','
                                # print('Hello:'  , result_txt)
                                
                            
                            elif (key == 'std RGB') and check_dict[key]:
                                res = color_and_simple_sips.std_channels(img_rgb)
                                result_txt = result_txt + str(custom_round(res[0])) + ','
                                result_txt = result_txt + str(custom_round(res[1])) + ','
                                result_txt = result_txt + str(custom_round(res[2])) + ','
                                # print('Hello:'  , result_txt)
                            
                            elif (key == 'std LAB') and check_dict[key]:
                                res = color_and_simple_sips.std_channels(img_lab)
                                result_txt = result_txt + str(custom_round(res[0])) + ','
                                result_txt = result_txt + str(custom_round(res[1])) + ','
                                result_txt = result_txt + str(custom_round(res[2])) + ','
                                # print('Hello:'  , result_txt)
                                
                            elif (key == 'std HSV') and check_dict[key]:
                                ## get circular statistic for H channel
                                _ , circ_std = color_and_simple_sips.circ_stats(img_hsv)
                                result_txt = result_txt + str(custom_round(circ_std)) + ','
                                ## get normal std for S and V channel
                                res = color_and_simple_sips.std_channels(img_hsv)
                                result_txt = result_txt + str(custom_round(res[1])) + ','
                                result_txt = result_txt + str(custom_round(res[2])) + ','
                                # print('Hello:'  , result_txt)
                                

                                
                            elif (key == 'Color entropy') and check_dict[key]:
                                res = color_and_simple_sips.shannonentropy_channels(img_hsv[:,:,0])
                                result_txt = result_txt + str(custom_round(res)) + ','
                                # print('Hello:'  , result_txt)

                                                          
                            elif ((key == '1st-order') and check_dict[key]) or ((key == '2nd-order') and check_dict[key]) or ((key == 'Edge density') and check_dict[key]):
                                
                                # if already first or second order entropy has been calculated
                                if first_ord != None:
                                    if key == '1st-order':
                                        result_txt = result_txt + str(custom_round(first_ord)) + ','
                                    elif key == '2nd-order':
                                        result_txt = result_txt + str(custom_round(sec_ord)) + ','
                                    elif key == 'Edge density':
                                        result_txt = result_txt + str(custom_round(edge_d)) + ','
                                # if not jet calculated, calculate both
                                else:
                                    res = edge_entropy_sips.do_first_and_second_order_entropy_and_edge_density (img_gray)
                                    first_ord = res[0]
                                    sec_ord   = res[1]
                                    edge_d    = res[2]
                                    if key == '1st-order':
                                        result_txt = result_txt + str(custom_round(first_ord)) + ','
                                    elif key == '2nd-order':
                                        result_txt = result_txt + str(custom_round(sec_ord)) + ','
                                    elif key == 'Edge density':
                                        result_txt = result_txt + str(custom_round(edge_d)) + ','
                                    
                            elif (key == 'Luminance entropy') and check_dict[key]:
                                res = color_and_simple_sips.shannonentropy_channels(img_lab[:,:,0])
                                result_txt = result_txt + str(custom_round(res)) + ','
                                # print('Hello:'  , result_txt)
                                
                            elif (key == 'Image size (pixels)') and check_dict[key]:
                                res = color_and_simple_sips.image_size(img_rgb)
                                result_txt = result_txt + str(custom_round(res)) + ','
                                # print('Hello:'  , result_txt)
                                
                            elif (key == 'Aspect ratio') and check_dict[key]:
                                res = color_and_simple_sips.aspect_ratio(img_rgb)
                                result_txt = result_txt + str(custom_round(res)) + ','
                                # print('Hello:'  , result_txt)
                                
                                
                            elif ((key == 'left-right') and check_dict[key]) or ((key == 'up-down') and check_dict[key]) or ((key == 'left-right & up-down') and check_dict[key]):
                                

                                # if one CNN sym has already been calculated, the others have been calculated as well
                                if sym_lr != None:
                                    if key == 'left-right':
                                        result_txt = result_txt + str(custom_round(sym_lr)) + ','
                                    elif key == 'up-down':
                                        result_txt = result_txt + str(custom_round(sym_ud)) + ','
                                    elif key == 'left-right & up-down':
                                        result_txt = result_txt + str(custom_round(sym_lrud)) + ','
                                        
                                # if not jet calculated, calculate all syms together and store results
                                else:

                                    sym_lr,sym_ud,sym_lrud = CNN_sips.get_symmetry(img_rgb, kernel, bias)
                                    
                                    if key == 'left-right':
                                        result_txt = result_txt + str(custom_round(sym_lr)) + ','
                                    elif key == 'up-down':
                                        result_txt = result_txt + str(custom_round(sym_ud)) + ','
                                    elif key == 'left-right & up-down':
                                        result_txt = result_txt + str(custom_round(sym_lrud)) + ','
                                
                                
                            elif (key == 'Sparseness') and check_dict[key]:
                                
                                resp_scipy = CNN_sips.conv2d(img_rgb, kernel, bias)
                                _, normalized_max_pooling_map_Sparseness  = CNN_sips.max_pooling (resp_scipy, patches=p22_Sparseness )
                                sparseness =  CNN_sips.get_CNN_Variance (normalized_max_pooling_map_Sparseness   , kind='sparseness' )
                                result_txt = result_txt + str(custom_round(sparseness)) + ','
                                

                            elif (key == 'Variability') and check_dict[key]:
                                
                                resp_scipy = CNN_sips.conv2d(img_rgb, kernel, bias)
                                _, normalized_max_pooling_map_Variability = CNN_sips.max_pooling (resp_scipy, patches=p12_Variability )
                                variability = CNN_sips.get_CNN_Variance (normalized_max_pooling_map_Variability , kind='variability' )
                                result_txt = result_txt + str(custom_round(variability)) + ','

                            elif (key == 'CNN-based') and check_dict[key]:
                                img_switch_channel = img_rgb[:,:,(2,1,0)].astype(np.float32)
                                resp_scipy = CNN_sips.conv2d(img_switch_channel, kernel, bias)
                                _, normalized_max_pooling_map_8 = CNN_sips.max_pooling (resp_scipy, patches=8 )
                                _, normalized_max_pooling_map_1 = CNN_sips.max_pooling (resp_scipy, patches=1 )
                                cnn_self_sym = CNN_sips.get_selfsimilarity (normalized_max_pooling_map_1 , normalized_max_pooling_map_8 )
                                result_txt = result_txt + str(custom_round(cnn_self_sym)) + ','


                            elif ((key == 'Sigma') and check_dict[key]) or ((key == 'Slope') and check_dict[key]):
                                
                                # if one of both fourier measures has already been calc
                                if sigma != None:
                                    if key == 'Sigma':
                                        result_txt = result_txt + str(custom_round(sigma)) + ','
                                    elif key == 'Slope':
                                        result_txt = result_txt + str(custom_round(slope)) + ','
                                else:
                                    sigma , slope = fourier_sips.fourier_sigma(img_lab[:,:,0])
                                    if key == 'Sigma':
                                        result_txt = result_txt + str(custom_round(sigma)) + ','
                                    elif key == 'Slope':
                                        result_txt = result_txt + str(custom_round(slope)) + ','
                                
                            elif (key == 'RMS contrast') and check_dict[key]:
                                res = color_and_simple_sips.std_channels(img_lab)[0]
                                result_txt = result_txt + str(custom_round(res)) + ','
                                
                                
                            elif (key == 'Balance') and check_dict[key]:
                                res = balance_sips.APB_Score(img_gray)
                                result_txt = result_txt + str(custom_round(res)) + ','
                                
                            elif (key == 'DCM') and check_dict[key]:
                                res = balance_sips.DCM_Key(img_gray)
                                result_txt = result_txt + str(custom_round(res)) + ','
                                
                            elif (key == 'Mirror symmetry') and check_dict[key]:
                                res = balance_sips.MS_Score(img_gray)
                                result_txt = result_txt + str(custom_round(res)) + ','

                            elif (key == 'Homogeneity') and check_dict[key]:
                                res = balance_sips.entropy_score_2d(img_gray)
                                result_txt = result_txt + str(custom_round(res)) + ','

                            elif (key == '2-dimensional') and check_dict[key]:
                                res = box_count_sips.custom_differential_box_count(img_gray)
                                result_txt = result_txt + str(custom_round(res)) + ','

                            elif (key == '3-dimensional') and check_dict[key]:
                                res = box_count_sips.box_count_2d(img_gray)
                                result_txt = result_txt + str(custom_round(res)) + ','
                            
                                
                           
                            ### PHOG
                            elif ((key == 'PHOG-based') and check_dict[key]) or ((key == 'Complexity') and check_dict[key]) or ((key == 'Anisotropy') and check_dict[key]):
                                
                                # if one PHOG measure has already been calculated, the others have been calculated as well
                                if self_sim != None:
                                    if key == 'PHOG-based':
                                        result_txt = result_txt + str(custom_round(self_sim)) + ','
                                    elif key == 'Complexity':
                                        result_txt = result_txt + str(custom_round(complexity)) + ','
                                    elif key == 'Anisotropy':
                                        result_txt = result_txt + str(custom_round(anisotropy)) + ','
                                                 
                                else:
                                    self_sim, complexity, anisotropy = PHOG_sips.PHOGfromImage(img_rgb, section=section, bins=bins, angle=angle, levels=levels, re=re, sesfweight=[weigths1,weigths2,weigths3] )
                                    if key == 'PHOG-based':
                                        result_txt = result_txt + str(custom_round(self_sim)) + ','
                                    elif key == 'Complexity':
                                        result_txt = result_txt + str(custom_round(complexity)) + ','
                                    elif key == 'Anisotropy':
                                        result_txt = result_txt + str(custom_round(anisotropy)) + ','
   
                                
                                
                        result_txt = result_txt[:-1] + '\n'

                        #my_bar.progress((n+1)* int(100 / (len(upload_file)))  )
                        my_bar.progress( int( (n+1)/len(upload_file) * 100) )


            else:
                st.write('Select SIP(s) to compute first.')       
        else:
            st.write('No image files found. Load images first.')
    
    
    
    
   
    enable_download = False
    if run & (len(upload_file) != 0) & (counter_checked_keys>0):
        enable_download = True
        download_file = result_txt
          
    if enable_download:
       st.success('Calculations finished. Click Download Results. A txt-file containing the results will be downloaded to your default download folder.', icon="✅")
       download = st.download_button('Download Results', download_file, file_name='SIPmachine_results.csv')  # Defaults to 'text/plain'
        
  
    

    
if app_mode == 'Documentation':
    
    st.markdown(""" <style> .font0 {
    font-size:35px ; font-family: 'Cooper Black'; color: #FF9633;} 
    </style> """, unsafe_allow_html=True)
    st.markdown('<p class="font0">Documentation</p>', unsafe_allow_html=True)
    
    st.markdown(""" <style> .font2 {
    font-size:16px ; font-family: 'Cooper Black'; color: green;} 
    </style> """, unsafe_allow_html=True)
    
    
    
    st.markdown('<p class="font2">Contrast and Luminance Entropy</p>', unsafe_allow_html=True)
    
    st.write(""" Contrast is a widely studied feature in aesthetic research and there
    are many different methods to calculate it. It is unclear to what extent these different methods capture the
    same visually perceivable image property (Schifanella et al., 2015; Tong et al., 2005; Li and Chen, 2009;
    Luo and Tang, 2008). In the present work, Contrast is defined as the root mean square (rms) contrast (Peli,
    1990), which is the standard deviation of the L channel of the CIELAB color space. We also calculate the
    Shannon entropy (Shannon, 1948) of the L channel of the CIELAB color space. Since different entropy
    measures are calculated in the present work, we refer to this entropy measure as Luminance Entropy. In
    other publications (Sidhu et al., 2018; Mather, 2018; Iigaya et al., 2021), it is often referred to simply as
    entropy or Shannon entropy.""")
    
        
    
    st.markdown('<p class="font2">Edge-Orientation Entropy</p>', unsafe_allow_html=True)
    """
    Second-Order Edge-Orientation Entropy is used to measure how
    independently (randomly) edge orientations are distributed across an image (Redies et al., 2017). To
    obtain this measure, the orientation of each edge element is related to the orientation of all other edge
    elements in the same image by pairwise comparison. An image whose edges all have the same orientation
    and are distributed over the image at regular intervals would have a very low Edge-Orientation Entropy.
    An image with edge elements that have a random orientations and are randomly distributed over the image
    would have maximal Edge-Orientation Entropy. In this case, the orientations of the edge elements would
    be maximally independent of each other across the image."""
    
    
    
    st.markdown('<p class="font2">PHOG Measures (Self-Similarity, Complexity and Anisotropy)</p>', unsafe_allow_html=True)
    """
    Self-Similarity, Complexity and
    Anisotropy measures are assessed using the (Pyramid of) Histograms of Orientation Gradients ([P]HOG)
    method, which was originally developed for object recognition and image categorization (Bosch et al.,
    2007). For details on the computation of Self-Similarity, Complexity, and Anisotropy, see the appendix in
    Braun et al. (2013). In brief, Self-Similarity captures how similar the histograms of gradient orientations
    are in a pyramid of subregions of an image compared to the histogram of the entire image or other
    subregions. High values for Self-Similarity indicate that the subregions are more similar to the entire
    image. Anisotropy measures how different the strengths of the gradients are across orientations in an
    image. Lower anisotropy indicates that the strength of the oriented gradients is more uniform across
    orientations. Higher anisotropy means that oriented gradient strength differs more strongly. Complexity
    is calculated as the mean gradient strength throughout an image. Higher complexity indicates a stronger
    mean gradient."""
    
    
    
    st.markdown('<p class="font2">Fourier Slope and Fourier Sigma</p>', unsafe_allow_html=True)
    """
    Fourier Slope and Fourier Sigma are based on the Fourier power
    spectrum of the gray-scale version of an image. Roughly speaking, the Fourier Slope indicates the relative
    strength of high spatial frequencies versus low spatial frequencies. The Fourier Sigma indicates how
    linearly the log-log plot of the Fourier spectrum decreases with increasing spatial frequency. Higher values
    for Fourier Sigma correspond to larger deviations from a linear course. For a more detailed description of
    these SIPs, see Redies et al. (2008)."""
    
    
    
    st.markdown('<p class="font2">Symmetry-lr and Symmetry-ud</p>', unsafe_allow_html=True)
    """
    Brachmann and Redies (2016) developed a symmetry measure that is
    based on the first layer of CNN filters from a pre-trained AlexNet (Hinton et al., 2012). Since these filters
    capture both color-opponent features, luminance edges, and texture information, the symmetry measures
    computed from these filters more closely match the human perception of symmetry than earlier measures
    based on the symmetry of gray-scale pixels. For the present work, left/right symmetry (Symmetry-lr)
    and up/down symmetry (Symmetry-ud) were calculated with this method. For a broader overview of the
    importance and previous results on symmetry in aesthetics research, see Bertamini and Rampone (2020)."""
    
    
    st.markdown('<p class="font2">Sparseness and Variability</p>', unsafe_allow_html=True)
    """
    Brachmann et al. (2017) used the first
    convolutional layer of a pre-trained AlexNet to also measure Sparseness/Richness and Variability of the
    feature responses. A max-pooling operation was applied to each map of the filter responses of the 96
    filters in the first CNN layer. Sparseness is calculated as the median of the variances of each max-pooling
    map. Variability is the variance over all entries of all max-pooling maps. Note that in the original paper
    by Brachmann et al. (2017), Sparseness of SIPs was referred to as the inverse of Richness. In the present
    work, we decided to use the term Sparseness because the calculated variance relates directly to it (and
    not to its inverse value). For a visualization of Sparseness, see the boxplots in Figure 2 for the JA dataset
    (traditional oil paintings; low Sparseness) compared to the ArtPics dataset (style-transferred objects on
    large white background; high Sparseness)."""
    
if app_mode == 'References':
    
    """
    Amirshahi, S. A., Hayn-Leichsenring, G. U., Denzler, J., and Redies, C. (2015). Jenaesthetics subjective
    dataset: Analyzing paintings by subjective scores. Lect. Notes Comp. Sci. 8925, 3–19. doi:10.1007/
    978-3-319-16178-5 1"""
    
    
    """
    Bertamini, M. and Rampone, G. (2020). The Study of Symmetry in Empirical Aesthetics. In The
    Oxford Handbook of Empirical Aesthetics (Oxford University Press). 488–509. doi:10.1093/oxfordhb/
    9780198824350.013.23"""

    """
    Bosch, A., Zisserman, A., and Munoz, X. (2007). Representing shape with a spatial pyramid kernel.
    In Proceedings of the 6th ACM International Conference on Image and Video Retrieval. 401–408.
    doi:10.1145/1282280.1282340"""
    
    """
    Brachmann, A., Barth, E., and Redies, C. (2017). Using CNN features to better understand what makes
    visual artworks special. Front. Psychol. 8, 830. doi:10.3389/fpsyg.2017.00830
    
    Brachmann, A. and Redies, C. (2016). Using convolutional neural network filters to measure left-right
    mirror symmetry in images. Symmetry 8, 144. doi:10.3390/sym8120144
    
    Brachmann, A. and Redies, C. (2017). Computational and experimental approaches to visual aesthetics.
    Front. Comput. Neurosc. 11, 102. doi:10.3389/fncom.2017.00102
    
    Braun, J., Amirshahi, S. A., Denzler, J., and Redies, C. (2013). Statistical image properties of print
    advertisements, visual artworks and images of architecture. Front. Psychol. 4, 808. doi:10.3389/fpsyg.
    2013.00808
    
    Brielmann, A. A. and Pelli, D. G. (2019). Intense beauty requires intense pleasure. Front. Psychol. 10,
    2420. doi:10.3389/fpsyg.2019.02420
    
    Chu, W.-T., Chen, Y.-K., and Chen, K.-T. (2013). Size does matter: How image size affects aesthetic
    perception? In Proceedings of the 21st ACM International Conference on Multimedia (Association for
    Computing Machinery), 53–62. doi:10.1145/2502081.2502102
    
    Conwell, C., Graham, D., and Vessel, E. (2022). The perceptual primacy of feeling: Affectless machine
    vision models robustly predict human visual arousal, valence, and aesthetics. PsyArXiv [Preprint]
    doi:10.31234/osf.io/5wg4s. Available at: https://psyarxiv.com/5wg4s/ (accessed Sep 15, 2022)
    
    Datta, R., Li, J., and Wang, J. Z. (2008). Algorithmic inferencing of aesthetics and emotion in natural
    images: An exposition. In 2008 15th IEEE International Conference on Image Processing (IEEE),
    105–108. doi:10.1109/ICIP.2008.4711702
    
    Deng, J., Dong, W., Socher, R., Li, L.-J., Li, K., and Fei-Fei, L. (2009). Imagenet: A large-scale
    hierarchical image database. In 2009 IEEE Conference on Computer Vision and Pattern Recognition
    (IEEE), 248–255. doi:10.1109/CVPR.2009.5206848
    
    Fekete, A., Pelowski, M., Specker, E., Brieber, D., Rosenberg, R., and Leder, H. (2022). The Vienna
    Art Picture System (VAPS): A data set of 999 paintings and subjective ratings for art and aesthetics
    research. Psychol. Aesthet. Crea. doi:10.1037/aca0000460
    
    Forsythe, A., Mulhern, G., and Sawey, M. (2008). Confounds in pictorial sets: The role of complexity
    and familiarity in basic-level picture processing. Behav. Res. Methods 40, 116–129. doi:10.3758/brm.
    40.1.116
    
    Friedman, L. and Wall, M. (2005). Graphical views of suppression and multicollinearity in multiple linear
    regression. Am. Stat. 59, 127–136. doi:10.1198/000313005X41337
    
    Gatys, L. A., Ecker, A. S., and Bethge, M. (2016). Image style transfer using convolutional neural
    networks. In Proceedings of the IEEE Conference on Computer Vision and Pattern Recognition. 2414–2423. doi:10.1109/CVPR.2016.265
    
    Geisser, S. (1975). The predictive sample reuse method with applications. J. Am. Stat. Assoc. 70, 320–328.
    doi:10.1080/01621459.1975.10479865
    
    Geller, H. A., Bartho, R., Thömmes, K., and Redies, C. (2022). Statistical image properties predict
    aesthetic ratings in abstract paintings created by neural style transfer. Front. Neurosci. 16, 999720.
    doi:10.3389/fnins.2022.999720
    
    Graham, D. and Field, D. (2008). Statistical regularities of art images and natural scenes: Spectra,
    sparseness and nonlinearities. Spat. Vis. 21, 149–164. doi:10.1163/156856807782753877
    
    Hinton, G. E., Krizhevsky, A., and Sutskever, I. (2012). Imagenet classification with deep convolutional
    neural networks. Adv. Neural Inf. Process. Syst. 25, 1. doi:10.1145/3065386
    
    Iigaya, K., Yi, S., Wahle, I. A., Tanwisuth, K., and O’Doherty, J. P. (2021). Aesthetic preference for art
    can be predicted from a mixture of low-and high-level visual features. Nat. Hum. Behav. 5, 743–755.
    doi:10.1038/s41562-021-01124-6
    
    Jović, A., Brkić, K., and Bogunović, N. (2015). A review of feature selection methods with applications.
    In 2015 38th International Convention on Information and Communication Technology, Electronics
    and Microelectronics (MIPRO) (IEEE), 1200–1205. doi:10.1109/MIPRO.2015.7160458
    
    Kang, C., Valenzise, G., and Dufaux, F. (2020). Eva: An explainable visual aesthetics dataset. In
    Joint Workshop on Aesthetic and Technical Quality Assessment of Multimedia and Media Analytics for
    Societal Trends. 5–13. doi:10.1145/3423268.3423590"""
        
    
# ##################################################################################################################
# ############################## SIP calc functions ################################################################
# ##################################################################################################################


