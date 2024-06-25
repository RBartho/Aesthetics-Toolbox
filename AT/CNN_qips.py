import numpy as np
from scipy.signal import correlate
from skimage.transform import resize

################################ helper functions #####################################


def resize_and_add_ImageNet_mean(img):
    ### resize img to desired dimension
    img = resize(img, [512,512], order=1) ### Not the same "resize" function as the old Caffe code, which leads to different results depending on the extent of the resizing. 
    ### normalize with image_net mean
    img = img  - np.array([104.00698793 , 116.66876762 , 122.67891434])
    ### add new additional axis and return
    return img


def conv2d(input_img, kernel, bias):
    
    input_img = input_img[:,:,(2,1,0)].astype(np.float32)  ## Caffe Net used different channel orders
    
    input_img = resize_and_add_ImageNet_mean(input_img )
    
    # Get input data dimensions
    in_height, in_width, in_channels = input_img.shape

    # Get kernel dimensions
    k_height, k_width, in_channels, out_channels = kernel.shape

    # Calculate output dimensions
    out_height = int(np.ceil(float(in_height - k_height + 1) / float(4)))
    out_width = int(np.ceil(float(in_width - k_width + 1) / float(4)))

    # Allocate output data
    output_data = np.zeros((out_height, out_width, out_channels))

    # Convolve each input channel with its corresponding kernel and sum the results
    for j in range(out_channels):
        for i in range(in_channels):
            output_data[:, :, j] += correlate(
                input_img[:, :, i],
                kernel[:, :, i, j],
                mode='valid'
            )[::4, ::4]

        # Add bias to the output
        output_data[:, :, j] += bias[j]
        
    ## relu activation function
    output_data[output_data < 0] = 0
    
    ### swap axis to order: filters, dim1_filters, dim2_filters (96,126,126)
    output_data = np.swapaxes(output_data,2,0)
    output_data = np.swapaxes(output_data,1,2)
        
    return output_data


def max_pooling (resp, patches ):
    (i_filters, ih, iw) = resp.shape
    max_pool_map = np.zeros((patches,patches,i_filters))
    patch_h = ih/float(patches)
    patch_w = iw/float(patches)

    for h in range(patches):
        for w in range(patches):
            ph = h*patch_h
            pw = w*patch_w
            patch_val = resp[:,int(ph):int(ph+patch_h), int(pw):int(pw+patch_w)]

            for b in range(i_filters):
                max_pool_map[h,w,b] = np.max(patch_val[b])

    max_pool_map_sum = np.sum(max_pool_map, axis=2)
    normalized_max_pool_map = max_pool_map / max_pool_map_sum[:,:,np.newaxis]

    return max_pool_map, normalized_max_pool_map


def get_differences(max_pooling_map_orig, max_pooling_map_flip):
    assert(max_pooling_map_orig.shape == max_pooling_map_flip.shape)
    sum_abs = np.sum(np.abs(max_pooling_map_orig - max_pooling_map_flip))
    sum_max = np.sum(np.maximum(max_pooling_map_orig, max_pooling_map_flip))
    return 1.0 - sum_abs / sum_max


###################### Variances ####################################################


def CNN_Variance(normalized_max_pool_map, kind):
    '''
    Calculates the 'variability' or 'sparseness' QIP 
    
    Input: Takes the CNN-features of the first layer of an AlexNet as input
    Output: CNN_Variance, Sparseness or Variability
    
    Usage:
    Import Image from PIL    
    
    img_rgb = np.asarray(Image.open( path_to_image_file ).convert('RGB')) 
    
    patches = 12 # default is 12 for variability and 22 for sparseness 
    kind = 'variability' or 'sparseness'
    
    [kernel,bias] = np.load(open("AT/bvlc_alexnet_conv1.npy", "rb"), encoding="latin1", allow_pickle=True)
    resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
    _, normalized_max_pooling_map_Variability = CNN_qips.max_pooling (resp_scipy, patches=patches )
    variability = CNN_qips.CNN_Variance (normalized_max_pooling_map_Variability , kind=kind )
    '''
    
    result = 0
    if kind == 'sparseness':
        result =  np.var( normalized_max_pool_map)
    elif kind == 'variability':
        result =  np.median(np.var(normalized_max_pool_map , axis=(0,1)))
    else:
        raise ValueError("Wrong input for kind of CNN_Variance. Use sparseness or variability")
    return result



################### Self-Similarity ################################

def CNN_selfsimilarity(histogram_ground, histogram_level):
    '''
    Calculates the 'CNN-based Self-similarity' QIP 
    
    Input: Takes the CNN-features of the first layer of an AlexNet as input
    Output: CNN-based Self-similarity
    
    Usage:
    Import Image from PIL    
    
    img_rgb = np.asarray(Image.open( path_to_image_file ).convert('RGB')) 
    
    [kernel,bias] = np.load(open("AT/bvlc_alexnet_conv1.npy", "rb"), encoding="latin1", allow_pickle=True)
    resp_scipy = CNN_qips.conv2d(img_rgb, kernel, bias)
    _, normalized_max_pooling_map_8 = CNN_qips.max_pooling (resp_scipy, patches=8 )
    _, normalized_max_pooling_map_1 = CNN_qips.max_pooling (resp_scipy, patches=1 )
    cnn_self_sym = CNN_qips.CNN_selfsimilarity (normalized_max_pooling_map_1 , normalized_max_pooling_map_8 )
    '''
    
    ph, pw, n = histogram_level.shape
    hiks = []
    for ih in range(ph):
        for iw in range(pw):
            hiks.append( np.sum(np.minimum( histogram_ground, histogram_level[ih,iw])) )
    sesim = np.median(hiks)
    return sesim


################### CNN Symmetry ################################


def CNN_symmetry(input_img, kernel, bias):
    '''
    Calculates the 'CNN-feature-based Symmetry' QIP 
    
    Input: Takes the CNN-features of the first layer of an AlexNet as input
    Output: CNN-based Symmetry, left-rigth Symmetry, up-down Symmetry and left-right-up-down Symmetry
    
    Usage:
    Import Image from PIL    
    
    img_rgb = np.asarray(Image.open( path_to_image_file ).convert('RGB')) 
    
    [kernel,bias] = np.load(open("AT/bvlc_alexnet_conv1.npy", "rb"), encoding="latin1", allow_pickle=True)
    sym_lr,sym_ud,sym_lrud = CNN_qips.CNN_symmetry(img_rgb, kernel, bias)
    '''
    
    ### get max pooling map for orig. image
    resp_orig = conv2d(input_img, kernel, bias)
    max_pooling_map_orig, _ = max_pooling (resp_orig, patches=17)
    
    ### get max pooling map for left-right fliped image
    img_lr = np.fliplr(input_img)
    resp_lr = conv2d(img_lr, kernel, bias)
    max_pooling_map_lr, _ = max_pooling (resp_lr, patches=17)
    sym_lr = get_differences(max_pooling_map_orig, max_pooling_map_lr)
    
    ### get max pooling map for up-down fliped image
    img_ud = np.flipud(input_img)
    resp_ud = conv2d(img_ud, kernel, bias)
    max_pooling_map_ud, _ = max_pooling (resp_ud, patches=17)
    sym_ud = get_differences(max_pooling_map_orig, max_pooling_map_ud)

    ### get max pooling map for up-down and left-right fliped image
    img_lrud = np.fliplr(np.flipud(input_img))
    resp_lrud = conv2d(img_lrud, kernel, bias)
    max_pooling_map_lrud, _ = max_pooling (resp_lrud, patches=17)
    sym_lrud = get_differences(max_pooling_map_orig, max_pooling_map_lrud)
    
    return sym_lr, sym_ud, sym_lrud
