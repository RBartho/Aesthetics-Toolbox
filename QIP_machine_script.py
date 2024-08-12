#Import the required Libraries
import numpy as np
from  PIL import Image
from skimage import color
import os
import pandas as pd
from tqdm import tqdm

### custom import
from AT import balance_qips, CNN_qips, color_and_simple_qips, edge_entropy_qips, fourier_qips, fractal_dimension_qips, PHOG_qips


########################################## set image paths and results.csv ##########################

### set path to save the results csv files
results_path = '/home/ralf/Documents/18_SIP_Machine/Full_Datasets_SIPs/Full_dataset_stats_new/'


### each entry is a pair of the name of the csv file and the path to the image folder, you can enter several datasets/pairs
datasets = [
            ['results.csv'  , 'path_to_images'],   
            ]

####################################### set wanted QIPs to 'True', otherwise "False"  #########################

check_dict = {}

check_dict['Image size (pixels)'] = True
check_dict['Aspect ratio'] = True
check_dict['RMS contrast'] = True
check_dict['Luminance entropy'] = True
check_dict['Complexity'] = True
check_dict['Edge density'] = True
check_dict['Color entropy'] =  True
check_dict['means RGB'] = True
check_dict['means Lab'] = True
check_dict['means HSV'] = True
check_dict['std RGB'] = True
check_dict['std Lab'] = True
check_dict['std HSV'] = True
check_dict['Mirror symmetry'] = True
check_dict['DCM'] = True
check_dict['Balance'] = True
check_dict['left-right'] = True
check_dict['up-down'] = True
check_dict['left-right & up-down'] = True
check_dict['Slope Redies'] = True
check_dict['Slope Spehar'] = True
check_dict['Slope Mather'] = True
check_dict['Sigma'] = True
check_dict['2-dimensional'] = True
check_dict['3-dimensional'] = True
check_dict['PHOG-based'] = True
check_dict['CNN-based'] = True
check_dict['Anisotropy'] = True
check_dict['Homogeneity'] = True
check_dict['1st-order'] = True
check_dict['2nd-order'] = True
check_dict['Sparseness'] = True
check_dict['Variability'] = True


#######################################################################################################
##################################### run script ######################################################
#######################################################################################################


Image.MAX_IMAGE_PIXELS = 1e10
			      
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
    'Sigma'         :  'Fourier sigma',
    'PHOG-based'    :  'Self-similarity (PHOG)',
    'CNN-based'     :  'Self-similarity (CNN)',
    '1st-order'     :  '1st-order EOE',
    '2nd-order'     :  '2nd-order EOE',
    }

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

######################################

for entry in datasets:
    csv_name = entry[0]
    image_path = entry[1]
    print('##########################')
    print(csv_name)
    print('##########################')
    
    
       
    
    
    ### load values for CNN kernel and bias
    [kernel,bias] = np.load(open("AT/bvlc_alexnet_conv1.npy", "rb"), encoding="latin1", allow_pickle=True)
            
    #progress_text = "Operation in progress. Please wait."

    file_names = []
    for root, dirs, files in os.walk(image_path):
        for file in files:
            file_names.append( os.path.join(root,file) )
       
    ## create new CSV file, if it does not already exists
    if not os.path.exists(results_path + csv_name):   
        with open(results_path + csv_name, 'w') as log:
            log.write('img_file,')
            for key in check_dict:
                if check_dict[key]:
                    if key in dict_of_multi_measures:
                        
                        for sub_key in dict_of_multi_measures[key]:
                            log.write(sub_key + ',')
                    else:
                        log.write(dict_full_names_QIPs.get(key,key) + ',')     
            log.write('\n')  
            
        file_names = []
        for root, dirs, files in os.walk(image_path):
            for file in files:
                file_names.append( os.path.join(root,file) )
                
    else:
        df = pd.read_csv(results_path + csv_name, sep=',')
        exist_img_list = list(df['img_file'])
        
        file_names = []
        for root, dirs, files in os.walk(image_path):
            for file in files:
                if file not in exist_img_list:
                    file_names.append( os.path.join(root,file) )
            
    for file in tqdm(file_names, total=len(file_names)):
            try:
                # print(' ')
                # print('Finished percent: ' , np.round(100* img_counter/num_images),  '   Calculating image:  '  , file_name)
                file_dir = os.path.join(  image_path , file)
    
                #replace_commas:
                file_name = file.split('/')[-1]
                file_name = file_name.replace(",", "_")
                    
                with open(results_path + csv_name, 'a') as log:
                    log.write(str(file_name) + ',')
        
                ### load images in different color spaces
                img_plain_PIL = Image.open(file_dir)
                img_plain_np = np.asarray(img_plain_PIL)
                img_rgb = np.asarray(img_plain_PIL.convert('RGB'))
                img_lab = color.rgb2lab(img_rgb)
                img_hsv = color.rgb2hsv(img_rgb)
                img_gray = np.asarray(Image.open(file_dir).convert('L'))  ## color uses range [0-1], PIL uses Range [0-256] for intensity
        
            
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
                        #if gray_scale_img == False:
                        res = color_and_simple_qips.mean_channels(img_rgb)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res[0])) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
                        
                    
                    elif (key == 'means Lab') and check_dict[key]:
                        #if gray_scale_img == False:
                        res = color_and_simple_qips.mean_channels(img_lab)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res[0])) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
                            
                                                            
                    elif (key == 'means HSV') and check_dict[key]:
                        ## get circular statistic for H channel
                        circ_mean, _ = color_and_simple_qips.circ_stats(img_hsv)
                        # get normal mean for S and V
                        res = color_and_simple_qips.mean_channels(img_hsv)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(circ_mean)) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
            
                    
                    elif (key == 'std RGB') and check_dict[key]:
                        res = color_and_simple_qips.std_channels(img_rgb)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res[0])) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
                    
                    
                    elif (key == 'std Lab') and check_dict[key]:
                        res = color_and_simple_qips.std_channels(img_lab)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res[0])) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
        
                    elif (key == 'std HSV') and check_dict[key]:
                        ## get circular statistic for H channel
                        _ , circ_std = color_and_simple_qips.circ_stats(img_hsv)
                        res = color_and_simple_qips.std_channels(img_hsv)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(circ_std)) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
            
            
                    elif (key == 'Color entropy') and check_dict[key]:
                        res = color_and_simple_qips.shannonentropy_channels(img_hsv[:,:,0])
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                                                  
                    elif ((key == '1st-order') and check_dict[key]) or ((key == '2nd-order') and check_dict[key]) or ((key == 'Edge density') and check_dict[key]):
                        
                        # if already first or second order entropy has been calculated
                        if first_ord != None:
                            with open(results_path + csv_name, 'a') as log:
                                if key == '1st-order':
                                    log.write(str(custom_round(first_ord)) + ',')
                                elif key == '2nd-order':
                                    log.write(str(custom_round(sec_ord)) + ',')
                                elif key == 'Edge density':
                                    log.write(str(custom_round(edge_d)) + ',')
                        # if not jet calculated, calculate both
                        else:
                            res = edge_entropy_qips.do_first_and_second_order_entropy_and_edge_density (img_gray)
                            first_ord = res[0]
                            sec_ord   = res[1]
                            edge_d    = res[2]
                            with open(results_path + csv_name, 'a') as log:
                                if key == '1st-order':
                                    log.write(str(custom_round(first_ord)) + ',')
                                elif key == '2nd-order':
                                    log.write(str(custom_round(sec_ord)) + ',')
                                elif key == 'Edge density':
                                    log.write(str(custom_round(edge_d)) + ',')
                            
                    elif (key == 'Luminance entropy') and check_dict[key]:
                        res = color_and_simple_qips.shannonentropy_channels(img_lab[:,:,0])
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                        
                    elif (key == 'Image size (pixels)') and check_dict[key]:
                        res = color_and_simple_qips.image_size(img_rgb)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
            
                        
                    elif (key == 'Aspect ratio') and check_dict[key]:
                        res = color_and_simple_qips.aspect_ratio(img_rgb)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                        
                    elif ((key == 'left-right') and check_dict[key]) or ((key == 'up-down') and check_dict[key]) or ((key == 'left-right & up-down') and check_dict[key]):
                        
                        # if one CNN sym has already been calculated, the others have been calculated as well
                        if sym_lr != None:
                            with open(results_path + csv_name, 'a') as log:
                                if key == 'left-right':
                                    log.write(str(custom_round(sym_lr)) + ',')
                                elif key == 'up-down':
                                    log.write(str(custom_round(sym_ud)) + ',')
                                elif key == 'left-right & up-down':
                                    log.write(str(custom_round(sym_lrud)) + ',')
                                
                        # if not jet calculated, calculate all syms together and store results
                        else:
        
                            sym_lr,sym_ud,sym_lrud = CNN_qips.CNN_symmetry(img_rgb, kernel, bias)
                            with open(results_path + csv_name, 'a') as log:
                                if key == 'left-right':
                                    log.write(str(custom_round(sym_lr)) + ',')
                                elif key == 'up-down':
                                    log.write(str(custom_round(sym_ud)) + ',')
                                elif key == 'left-right & up-down':
                                    log.write(str(custom_round(sym_lrud)) + ',')
                        
                        
                    elif (key == 'Sparseness') and check_dict[key]:
                        resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
                        _, normalized_max_pooling_map_Sparseness  = CNN_qips.max_pooling (resp_scipy, patches=22 )
                        sparseness =  CNN_qips.CNN_Variance (normalized_max_pooling_map_Sparseness   , kind='sparseness' )
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(sparseness)) + ',')
                  
            
                    elif (key == 'Variability') and check_dict[key]:
                        resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
                        _, normalized_max_pooling_map_Variability = CNN_qips.max_pooling (resp_scipy, patches=12 )
                        variability = CNN_qips.CNN_Variance (normalized_max_pooling_map_Variability , kind='variability' )
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(variability)) + ',')
            
                    elif (key == 'CNN-based') and check_dict[key]:
                        resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
                        _, normalized_max_pooling_map_8 = CNN_qips.max_pooling (resp_scipy, patches=8 )
                        _, normalized_max_pooling_map_1 = CNN_qips.max_pooling (resp_scipy, patches=1 )
                        cnn_self_sym = CNN_qips.CNN_selfsimilarity (normalized_max_pooling_map_1 , normalized_max_pooling_map_8 )
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(cnn_self_sym)) + ',')
            
        
        
                    elif ((key == 'Sigma') and check_dict[key]) or ((key == 'Slope Redies') and check_dict[key]):
        
                        # if one of both fourier measures has already been calc
                        if sigma != None:
                            with open(results_path + csv_name, 'a') as log:
                                if key == 'Sigma':
                                    log.write(str(custom_round(sigma)) + ',')
                                elif key == 'Slope Redies':
                                    log.write(str(custom_round(slope)) + ',')
                        else:
                            with open(results_path + csv_name, 'a') as log:
                                sigma , slope = fourier_qips.fourier_redies(img_gray, bin_size = 2, cycles_min = 10, cycles_max=256)
                                if key == 'Sigma':
                                    log.write(str(custom_round(sigma)) + ',')
                                elif key == 'Slope Redies':
                                    log.write(str(custom_round(slope)) + ',')
                                    
                    elif (key == 'Slope Spehar') and check_dict[key]:
                        res = fourier_qips.fourier_slope_branka_Spehar_Isherwood(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                            
                    elif (key == 'Slope Mather') and check_dict[key]:
                        res = fourier_qips.fourier_slope_mather(img_rgb)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                         
                    elif (key == 'RMS contrast') and check_dict[key]:
                        res = color_and_simple_qips.std_channels(img_lab)[0]
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                        
                    elif (key == 'Balance') and check_dict[key]:
                        res = balance_qips.Balance(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                        
                    elif (key == 'DCM') and check_dict[key]:
                        res = balance_qips.DCM(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res[0])) + ',')
                            log.write(str(custom_round(res[1])) + ',')
                            log.write(str(custom_round(res[2])) + ',')
               
                    elif (key == 'Mirror symmetry') and check_dict[key]:
                        res = balance_qips.Mirror_symmetry(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
            
                    elif (key == 'Homogeneity') and check_dict[key]:
                        res = balance_qips.Homogeneity(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
            
                    elif (key == '2-dimensional') and check_dict[key]:
                        res = fractal_dimension_qips.fractal_dimension_2d(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
            
                    elif (key == '3-dimensional') and check_dict[key]:
                        res = fractal_dimension_qips.fractal_dimension_3d(img_gray)
                        with open(results_path + csv_name, 'a') as log:
                            log.write(str(custom_round(res)) + ',')
                    
                        
                   
                    ### PHOG
                    elif ((key == 'PHOG-based') and check_dict[key]) or ((key == 'Complexity') and check_dict[key]) or ((key == 'Anisotropy') and check_dict[key]):
                        
                        # if one PHOG measure has already been calculated, the others have been calculated as well
                        if self_sim != None:
                            with open(results_path + csv_name, 'a') as log:
                                if key == 'PHOG-based':
                                    log.write(str(custom_round(self_sim)) + ',')
                                elif key == 'Complexity':
                                    log.write(str(custom_round(complexity)) + ',')
                                elif key == 'Anisotropy':
                                    log.write(str(custom_round(anisotropy)) + ',')
                                         
                        else:
                            self_sim, complexity, anisotropy = PHOG_qips.PHOGfromImage(img_rgb, section=2, bins=16, angle=360, levels=3, re=-1, sesfweight=[1,1,1] )
                            with open(results_path + csv_name, 'a') as log:
                                if key == 'PHOG-based':
                                    log.write(str(custom_round(self_sim)) + ',')
                                elif key == 'Complexity':
                                    log.write(str(custom_round(complexity)) + ',')
                                elif key == 'Anisotropy':
                                    log.write(str(custom_round(anisotropy)) + ',')
               
                        
                with open(results_path + csv_name, 'a') as log:
                    log.write('\n')   
            except:
                print('############  ', file_name , '  an error occured. QIPs for file not calculated!')
