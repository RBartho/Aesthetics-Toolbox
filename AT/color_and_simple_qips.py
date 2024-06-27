import numpy as np
from scipy import stats
from skimage.measure import shannon_entropy



################################# Size QIPs ################################
    

def aspect_ratio(img_rgb):
    '''
    Calculates the "Aspect ratio" QIP 
    
    Input: Takes a rgb image in Pillow format as input. Grayscale works as well. 
    Output: Aspect ratio
    
    Usage:     
    Import Image from PIL    
    img_gray = np.asarray(Image.open( path_to_image_file )) 
    aspect_ratio(img_rgb)
    '''
    return img_rgb.shape[1] / img_rgb.shape[0]


def image_size(img_rgb):
    '''
    Calculates the "Image size" QIP 
    
    Input: Takes a rgb image in Pillow format as input. Grayscale works as well. 
    Output: Image size
    
    Usage:     
    Import Image from PIL    
    img_gray = np.asarray(Image.open( path_to_image_file )) 
    image_size(img_rgb)
    '''
    return img_rgb.shape[1] + img_rgb.shape[0] 


################################# Color QIPs ################################


def mean_channels(img):
    '''
    Calculates the "Mean values for color channels" 
    
    Input: RGB or grayscale images in Pillow format 
    Output: returns 1 mean value for grayscale and 3 mean color channels values for rgb, hsv or Lab images
    
    Usage:     
    Import Image from PIL    
    img_gray = np.asarray(Image.open( path_to_image_file )) 
    mean_channels(img_rgb)
    '''
    return np.mean(img, axis=(0,1)) # returns 1 value for grayscale and 3 values for color channels
    

### STD of RGB, HSV, LAB; STD(L)="RMSContrast"
def std_channels(img):
    '''
    Calculates the "Standard deviation for color channels" 
    
    Input: RGB or grayscale images in Pillow format 
    Output: returns 1 std value for grayscale and 3 std color channels values for rgb, hsv or Lab images
    
    Usage:     
    Import Image from PIL    
    img_gray = np.asarray(Image.open( path_to_image_file )) 
    std_channels(img_rgb)
    '''
    return np.std(img, axis=(0,1))


def circ_stats(img_hsv):
    '''
    Calculates the "Circular mean and circular standard deviation for color channels" 
    
    Input: hsv images in Pillow format 
    Output: returns circular mean and std for H channel of the hsv color space
    
    Usage:     
    Import Image from PIL 
    from skimage import color
    img_rgb = Image.open( path_to_image_file ).convert('RGB')
    img_hsv = color.rgb2hsv(img_rgb)
    circ_stats(img_hsv)
    '''
    hue = img_hsv[:,:,0].astype("float")
    circ_mean = stats.circmean(hue, high=1, low=0)
    circ_std = stats.circstd(hue, high=1, low=0)
    return circ_mean, circ_std
  
    
### color entropy, shannon_entropy Gray, 
def shannonentropy_channels(img):
    '''
    Used to calculate the "Color entropy" QIP  
    
    Input: all image formats possivle, for Color entropy use Pillow hsv image
    Output: returns shannon entropy for color channels
    
    Usage:     
    Import Image from PIL 
    from skimage import color
    img_rgb = Image.open( path_to_image_file ).convert('RGB')
    img_hsv = color.rgb2hsv(img_rgb)
    color_entropy = shannonentropy_channels(img_hsv[:,:,0])
    '''
    
    ### grayscale 2 dim image
    if img.ndim == 2:
        return shannon_entropy(img)
    if img.ndim == 3:
        chan_0 = shannon_entropy(img[:,:,0])
        chan_1 = shannon_entropy(img[:,:,1])
        chan_2 = shannon_entropy(img[:,:,2])
        return chan_0, chan_1, chan_2
    

