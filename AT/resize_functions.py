import numpy as np
import PIL
import io
from skimage.color import lab2rgb, rgb2lab


PIL.Image.MAX_IMAGE_PIXELS = 933120000



### helper functions

def file_process_in_memory(images):
    """ Converts PIL image objects into BytesIO in-memory bytes buffers. """

    for i, (image_name, pil_image) in enumerate(images):
        file_object = io.BytesIO()
        pil_image.save(file_object, "PNG")
        pil_image.close()
        images[i][1] = file_object  # Replace PIL image object with BytesIO memory buffer.

    return images  # Return modified list.


###############################################

def resize_using_longer_side_kepp_aspect_ratio(img, longer_side):
    '''
    'Input 8 bit img in PILLOW format
    '''
    
    if img.size[0] >= img.size[1]:
        a = longer_side / float(img.size[0])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    else:
        a = longer_side / float(img.size[1])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img
        

def resize_using_shorter_side_kepp_aspect_ratio(img, shorter_side):
    '''
    'Input 8 bit img in PILLOW format
    '''
    if img.size[0] <= img.size[1]:
        a = shorter_side / float(img.size[0])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    else:
        a = shorter_side / float(img.size[1])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img


def resize_width_keep_aspect_ratio(img, width=1000):
    '''
    'Input 8 bit img in PILLOW format
    '''
    a = width / float(img.size[0])
    img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img

def resize_height_keep_aspect_ratio(img, height=1000):
    '''
    'Input 8 bit img in PILLOW format
    '''
    a = height / float(img.size[1])
    img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img
        
def resize_to_resolution(img, width=1000, height=1000):
    '''
    'Input 8 bit img in PILLOW format
    '''
    img = img.resize((int(width),int(height)), PIL.Image.Resampling.LANCZOS)
    return img

def resize_to_number_of_pixels_keep_aspect_ratio(img, num_pixels=100000):
    '''
    'Input 8 bit img in PILLOW format
    '''
    s = img.size
    old_num_pixels = s[0]*s[1]
    d = np.sqrt(num_pixels/old_num_pixels)
    s_new = np.round([s[0]*d, s[1]*d]).astype(np.int32)
    img = img.resize((s_new[0],s_new[1]), PIL.Image.Resampling.LANCZOS)
    return img

def resize_to_fit_display(img, disp_width=1920, disp_height=1080):
    '''
    'Input 8 bit img in PILLOW format
    '''
    disp_ratio = disp_width/disp_height
    s = img.size
    img_ratio = s[0] / s[1] 
    if img_ratio > disp_ratio:  # --> resize img to disp_hight,while maintaining image aspect ratio
        a = disp_width / float(img.size[0])
        img = img.resize((int(s[0]*a),int(s[1]*a)), PIL.Image.Resampling.LANCZOS)
    else: #  resize img to disp_width ,while maintaining image aspect ratio
        a = disp_height / float(img.size[1])
        img = img.resize((int(s[0]*a),int(s[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img

########################### cropping

def center_crop (img):
    '''
    'Input 8 bit img in PILLOW format
    '''
    width, height = img.size   # Get dimensions

    if width > height:
        # center
        c_width = np.floor(width/2)
        c_height = np.floor(height/2)
        # define corp borders
        top=0
        bottom = height
        left = c_width - c_height
        right =  c_width + c_height 
        if height%2 == 1: # for uneven pixels
            right += 1
        img = img.crop((left, top, right, bottom))
        
    elif width < height:
        # center
        c_width = np.floor(width/2)
        c_height = np.floor(height/2)
        # define corp borders
        top    = c_height - c_width
        bottom = c_height + c_width
        left   = 0
        right  =  width
        if width%2 == 1: # for uneven pixels
            bottom += 1
        img = img.crop((left, top, right, bottom))
    else:
        img = img

    return img


def center_crop_to_square_power_of_two (img): 
    '''
    'Input 8 bit img in PILLOW format
    '''
    # crop to largest center square with power of two
    width, height = img.size   # Get dimensions

    # find largest power of two in pixel
    if width > height:
        npow = np.floor(np.log2(height))
    else:  
        npow = np.floor(np.log2(width))
        
    c_new = 2**(npow-1) # middle of new img length
    
    # find image center
    c_width = np.floor(width/2)
    c_height = np.floor(height/2)
    
    # define corp borders
    top    = c_height - c_new
    bottom = c_height + c_new
    left   = c_width - c_new
    right  = c_width + c_new 
            
    img = img.crop((left, top, right, bottom))
    
    return img


def resize_to_image_size(img, des_img_size=900):
    '''
    'Input 8 bit img in PILLOW format
    '''
    
    width, height = img.size   
    img_size =  width + height
    
    resize_faktor = des_img_size / img_size
    
    n_width = int(width*resize_faktor)
    n_height = int(height*resize_faktor)
    
    img = img.resize((n_width,n_height), PIL.Image.Resampling.LANCZOS)
    
    return img
    


def padding_and_resizing_to_square_X_pixel(img, resize_to=1024):
    '''
    'Input 8 bit img in PILLOW format
    '''
    mean = np.round(np.mean(img, axis=(0,1))).astype(np.uint8) # mean RGB values or mean gray value for padding
    
    ### resize first if needes
    if resize_to != -1:
        ### resize longer side while maintaining aspect ratio
        if img.size[0] >= img.size[1]:
            a = resize_to / float(img.size[0])
            img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
        else:
            a = resize_to / float(img.size[1])
            img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
        
    ### padding with mean gray value or mean RGB values
    img = np.asarray(img)
    h,w = img.shape[:2]
    w_c = int(w/2)
    h_c = int(h/2)
    if h > w: 
        img_pad = np.full([h,h,3], mean) 
        if w%2 == 1: # uneven width
            img_pad[ :  ,  h_c - w_c : h_c + w_c +1  ] = img
        else:
            img_pad[ :  ,  h_c - w_c : h_c + w_c  ] = img
        img = img_pad
    elif h < w:
        img_pad = np.full([w,w,3], mean)  
        if h%2 == 1: # uneven height
            img_pad[w_c - h_c : w_c + h_c +1  , :  ] = img
        else: 
            img_pad[w_c - h_c : w_c + h_c  , :  ] = img     
        img = img_pad
        
    return PIL.Image.fromarray(img)

################################# LAB Color rotation ################################


def cart2pol(x, y):
    rho = np.sqrt(x**2 + y**2)
    phi = np.arctan2(y, x)
    return rho, phi

def pol2cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y


def rotate_image_in_LAB_colorspace(img_rgb, degree):
    '''
    'Input 8 bit RGB image in PILLOW format
    '''
    
    img_lab = rgb2lab(img_rgb)

    degree_in_pi = degree/(180)
    
    ### get polar coordinates for each pixel
    rho, phi = cart2pol(img_lab[:,:,1], img_lab[:,:,2])
  
    ### change angle
    phi = phi+  degree_in_pi * np.pi
    
    ### convert back to polar coordinates
    x, y = pol2cart(rho, phi)
    
    ## assign to image, ceeping original luminance
    img_lab[:,:,1] = x
    img_lab[:,:,2] = y
    
    # convert to RGB
    img_RGB_rotated = lab2rgb(img_lab) * 255

    return PIL.Image.fromarray(img_RGB_rotated.astype(np.uint8))