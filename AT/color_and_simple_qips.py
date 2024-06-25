import numpy as np
from scipy import stats
from skimage.measure import shannon_entropy



################################# Size QIPs ################################
    
def aspect_ratio(img_RGB):
    return img_RGB.shape[1] / img_RGB.shape[0]

def image_size(img_RGB):
    return img_RGB.shape[1] + img_RGB.shape[0] 


################################# Color QIPs ################################

### Mean RGB, Mean HSV, Mean LAB
def mean_channels(img):
    # returns 1 value for grayscale and 3 values for color channels
    return np.mean(img, axis=(0,1))
    
### STD of RGB, HSV, LAB; STD(L)="RMSContrast"
def std_channels(img):
    # returns 1 value for grayscale and 3 values for color channels
    return np.std(img, axis=(0,1))


def circ_stats(img_hsv):
    hue = img_hsv[:,:,0].astype("float")
    circ_mean = stats.circmean(hue, high=1, low=0)
    circ_std = stats.circstd(hue, high=1, low=0)
    return circ_mean, circ_std
  
### color entropy, shannon_entropy Gray, 
def shannonentropy_channels(img):
    ### grayscale 2 dim image
    if img.ndim == 2:
        return shannon_entropy(img)
    if img.ndim == 3:
        chan_0 = shannon_entropy(img[:,:,0])
        chan_1 = shannon_entropy(img[:,:,1])
        chan_2 = shannon_entropy(img[:,:,2])
        return chan_0, chan_1, chan_2
    

