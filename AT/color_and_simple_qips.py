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




def image_size(img_rgb, kind = 'sum'):
    '''
    Calculates the "Image size" QIP 
    
    Input: Takes a rgb image in Pillow format as input. Grayscale works as well. 
    kind: Select Type of image size, default = 'sum' ; valid alternatives are: sum, num_pixels, diagonal, average, minumum, maximum
    Output: Image size
    
    Usage:     
    Import Image from PIL    
    img_rgb = np.asarray(Image.open( path_to_image_file )) 
    image_size(img_rgb)
    '''
    
    if kind == 'sum':
        return img_rgb.shape[1] + img_rgb.shape[0] 
    
    elif kind == 'num_pixel':
        return img_rgb.shape[1] * img_rgb.shape[0] 
    
    elif kind == 'diagonal':
        return int( np.linalg.norm([ img_rgb.shape[1] , img_rgb.shape[0]]) )
    
    elif kind == 'average':
        return int( np.mean([ img_rgb.shape[1] , img_rgb.shape[0]]) )
    
    elif kind == 'minimum':
        return  np.min([ img_rgb.shape[1] , img_rgb.shape[0]]) 
    
    elif kind == 'maximum':
        return np.max([ img_rgb.shape[1] , img_rgb.shape[0]]) 
    
    
    else:
        raise NotImplementedError ('not implemented, wrong kind image size selected')
    


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
  
    
def shannonentropy_channels(img):
    '''
    Used to calculate the "Color entropy" and "Ligtness entropy) QIPs  
    
    Input: single color channel, for Color entropy use Pillow hsv image, for ligthness entropy Lab image
    Output: returns shannon entropy for color channels
    
    Usage:     
    Import Image from PIL 
    from skimage import color
    img_rgb = Image.open( path_to_image_file ).convert('RGB')
    img_hsv = color.rgb2hsv(img_rgb)
    color_entropy = shannonentropy_channels(img_hsv[:,:,0])
    '''
    
    # change range of values to 256 bins [0-255]
    if np.max(img) > 0:
        img = img / np.max(img)
    img = img*255
    img = np.round(img)

    return shannon_entropy(img)
   
    

