import numpy as np
from scipy import stats



def sfsl_get_radius(_input, img_input = True):
    shape = _input.shape
    ######%get cartesian coordinates for shifted image (center in the middle)
    grid_x = np.arange(1, shape[1] + 1) - shape[1]/2 - 1
    grid_y = np.arange(1, shape[0] + 1) - shape[0]/2 - 1
    #np.meshgrid(grid_x,grid_y)[1]  
    x_idx, y_idx = np.meshgrid(grid_x,grid_y)
    
    return np.round( np.sqrt(x_idx**2 + y_idx**2) )


def sfsl_calc_radial_average(img):
    #### get matrix of radii for fftshifted image
    rad = sfsl_get_radius(img);
    #### get sorted list of radius entries
    r_list = np.unique(rad)
    ###preallocate memory for result
    avg = np.zeros(len(r_list)); 
    for r in range(len(r_list)):
        avg[r] = np.mean(img[ rad  == r_list[r]  ]) 
    return avg, r_list


def tff_image(img):    
    ### fastfuriertransform
    f = np.fft.fft2(img, axes=(0, 1))
    ### power and ffshift
    f_shift = np.fft.fftshift(np.abs(f)**2) #,  axes=(0, 1))

    return  f_shift


def fourier_sigma(img):
    f_pow = tff_image( img )
    avg, r_list = sfsl_calc_radial_average(f_pow)
    l_lim = 10 ### cutoff artifacts
    u_lim =  256 ### cutoff artifacts
    y = np.log10( avg[ l_lim : u_lim] )
    x = np.log10( r_list[ l_lim : u_lim] )
    slope, intercept, r_value, p_value, std_err = stats.linregress(x , y)
    
    line_points = x*slope + intercept
    sigma = np.mean((line_points - y)**2)

    return sigma , slope