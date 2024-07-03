import numpy as np
from scipy.ndimage import convolve
import PIL
import warnings



def create_gabor(size, theta=0, octave=3):
    
    amplitude = 1.0
    phase = np.pi/2.0
    frequency = 0.5**octave # 0.5**(octave+0.5)
    hrsf = 4 # half response spatial frequency bandwith
    sigma = 1/(np.pi*frequency) * np.sqrt(np.log(2)/2) * (2.0**hrsf+1)/(2.0**hrsf-1)
    valsy = np.linspace(-size//2+1, size//2, size)
    valsx = np.linspace(-size//2+1, size//2, size)
    xgr,ygr = np.meshgrid(valsx, valsy);

    omega = 2*np.pi*frequency
    gaussian = np.exp(-(xgr*xgr + ygr*ygr)/(2*sigma*sigma))
    slant = xgr*(omega*np.sin(theta)) + ygr*(omega*np.cos(theta))

    gabor = np.round(gaussian, decimals=4) * amplitude*np.cos(slant + phase);
    # e^(-(x^2+y^2)/(2*1.699^2)) *cos(pi/4*(x*sin(2)+y*cos(2)) + pi/2)

    return np.round(gabor, decimals=4)

def create_filterbank(flt_size=31 , num_filters=24):
    flt_raw = np.zeros([num_filters, flt_size, flt_size])
    BINS_VEC = np.linspace(0, 2*np.pi, num_filters+1)[:-1]
    for i in range(num_filters):
        flt_raw[i,:,:] = create_gabor(flt_size, theta=BINS_VEC[i], octave=3)
        #print(i, flt_size, BINS_VEC[i])
    return flt_raw


def run_filterbank(flt_raw, img, num_filters=24):
    (h, w) = img.shape
    num_filters = flt_raw.shape[0]
    image_flt = np.zeros((num_filters,h,w))

    for i in range(num_filters):
        image_flt[i,:,:] = convolve(img, flt_raw[i,:,:])

    resp_bin = np.argmax(image_flt, axis=0)
    resp_val = np.max(image_flt, axis=0)
    
    return resp_bin, resp_val


def edge_density(resp_val):
    normalize_fac = float(resp_val.shape[0] * resp_val.shape[1])
    edge_d = np.sum(resp_val)/normalize_fac
    return edge_d


def do_counting(resp_val, resp_bin, CIRC_BINS=48, GABOR_BINS=24, MAX_DIAGONAL = 500):
    """creates histogram (distance, relative orientation in image, relative gradient)"""
    
    h, w = resp_val.shape;
   
    # cutoff minor filter responses
    cutoff = np.sort(resp_val.flatten())[-10000] # get 10000th highest response for cutting of beneath
    resp_val[resp_val<cutoff] = 0
    ey, ex = resp_val.nonzero()

    # lookup tables to speed up calculations
    edge_dims = resp_val.shape
    xx, yy = np.meshgrid(np.linspace(-edge_dims[1],edge_dims[1],2*edge_dims[1]+1), np.linspace(-edge_dims[0],edge_dims[0],2*edge_dims[0]+1))
    dist = np.sqrt(xx**2+yy**2)

    orientations = resp_bin[ey,ex]
    counts = np.zeros([500, CIRC_BINS, GABOR_BINS])

    #print ("Counting", 'image name', resp_val.shape, "comparing", ex.size)
    for cp in range(ex.size):

        orientations_rel = orientations - orientations[cp]
        orientations_rel = np.mod(orientations_rel + GABOR_BINS, GABOR_BINS)

        distance_rel = np.round(dist[(ey-ey[cp])+edge_dims[0], (ex-ex[cp])+edge_dims[1]]).astype("uint32")
        distance_rel[distance_rel>=MAX_DIAGONAL] = MAX_DIAGONAL-1

        direction = np.round(np.arctan2(ey-ey[cp], ex-ex[cp]) / (2.0*np.pi)*CIRC_BINS + (orientations[cp]/float(GABOR_BINS)*CIRC_BINS)).astype("uint32")
        direction = np.mod(direction+CIRC_BINS, CIRC_BINS)
        np.add.at(counts, tuple([distance_rel, direction, orientations_rel]), resp_val[ey,ex] * resp_val[ey[cp],ex[cp]])

    return counts, resp_val


def entropy(a):
    if np.sum(a)!=1.0 and np.sum(a)>0:
        a = a / np.sum(a)
    v = a>0.0
    return -np.sum(a[v] * np.log2(a[v]))


def do_statistics(counts, GABOR_BINS=24):
    # normalize by sum
    counts_sum = np.sum(counts, axis=2) + 0.00001
    normalized_counts = counts / (counts_sum[:,:,np.newaxis])
    d,a,_ = normalized_counts.shape
    shannon_nan = np.zeros((d,a))
    for di in range(d):
      for ai in range(a):
        if counts_sum[di,ai]>1:  ## ignore bins without pixels
            shannon_nan[di,ai] = entropy(normalized_counts[di,ai,:])
        else:
            shannon_nan[di,ai] = np.nan
    return shannon_nan

         
def edge_resize (img_gray_np, max_pixels = 300*400):
    if max_pixels != None:
        img_gray_PIL = PIL.Image.fromarray(img_gray_np)
        s0,s1 = img_gray_PIL.size
        a = np.sqrt(max_pixels / float(s0*s1))
        img_gray_PIL_rez = img_gray_PIL.resize((int(s0*a),int(s1*a)), PIL.Image.LANCZOS)
        img_gray_np = np.asarray(img_gray_PIL_rez, dtype='float')
    return img_gray_np


def do_first_and_second_order_entropy_and_edge_density (img_gray, GABOR_BINS=24):
    '''
    Calculates the 'Edge density, 1st-order and 2nd-order Edge orientation entropy' QIPs 
    
    Input: 8 bit grayscale image in Pillow format
    Output: Edge density, 1st-order and 2nd-order Edge orientation entropy
    
    Usage:
    Import Image from PIL    
    
    img_gray = np.asarray(Image.open( path_to_image_file ).convert('L')) 
    do_first_and_second_order_entropy_and_edge_density (img_gray)
    '''
    
    flt_raw = create_filterbank()
    img = edge_resize (img_gray)
    resp_bin, resp_val = run_filterbank(flt_raw, img)
    
    ### edge density
    edge_d = edge_density(resp_val)
    
    ### do_counting must run before first_order_entropy but after edge density because it modifies resp_val!!! 
    counts, resp_val = do_counting(resp_val, resp_bin)

    ### first order entropy
    first_order_bin = np.zeros(GABOR_BINS)
    for b in range(GABOR_BINS):
        first_order_bin[b] = np.sum(resp_val[resp_bin==b])
    first_order = entropy(first_order_bin)
    ###second order entropy
    shannon_nan = do_statistics(counts)
    ## suppress "mean of empty slice warning"
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", category=RuntimeWarning)
        second_order = np.nanmean(np.nanmean(shannon_nan, axis=1)[20:240])
    return first_order, second_order, edge_d

