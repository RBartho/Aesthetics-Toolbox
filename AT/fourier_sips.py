import numpy as np
from skimage import color
import PIL

################################ Redies Group - OSF #################################


def calc_bin(val, binsize, x_min, x_max):
    x_max = x_max+1
    x_min = x_min+1
    
    bin_num = np.ceil((x_max - x_min) / binsize).astype(int)
    bin_log_size = (np.log10(x_max) - np.log10(x_min)) / bin_num
    bin_mean_bar = np.zeros((2, bin_num))
    bin_x_val = np.zeros(bin_num)
        
    for i in range(bin_num):
        i+=1
        # interval
        a_x = np.log10(x_min) + (i - 1) * bin_log_size
        b_x = np.log10(x_min) + i * bin_log_size

        # interval, abgerundet
        from_val = np.floor(10 ** a_x).astype(int)
        to_val = np.floor(10 ** b_x).astype(int)
        
        if to_val > len(val):
            to_val = len(val)
        # mean
        i-=1
        bin_mean_bar[0, i] = np.mean(np.arange(from_val, to_val + 1))  # x-val
        bin_mean_bar[1, i] = np.mean(val[np.arange(from_val-1, to_val)])  # y-val
        bin_x_val[i] = from_val

    return bin_mean_bar, bin_x_val


def var_eigen(log_m, log_n, log_x, log_y):
    fit = log_m * log_x + log_n
    diff = fit - log_y
    return np.var(diff)


def rotavg(array):
    N = array.shape[0]
    X, Y = np.meshgrid(np.arange(-N//2, N//2), np.arange(-N//2, N//2))
    theta, rho = np.arctan2(Y, X), np.sqrt(X**2 + Y**2)
    rho = np.round(rho).astype(int)
    I = np.zeros((N//2+1, 9))
    f = np.zeros((N//2+1, 9))
    a = np.arange(0, np.pi + np.pi/8, np.pi/8)
    
    for i in range(rho.shape[0]):
        for j in range(rho.shape[1]):
            rh = rho[i, j]
            value = array[i, j]
            
            if rh <= N/2:
                I[rh, 8] += 1
                if I[rh, 8] == 1:
                    f[rh, 8] = value
                    #print(value)
                else:
                    f[rh, 8] = f[rh, 8] + (value - f[rh, 8]) / I[rh, 8]
            
            for k in range(8):
                if a[k] <= theta[i, j] < a[k+1]:
                    if rh <= N/2:
                        I[rh, k] += 1
                        if I[rh, k] == 1:
                            f[rh, k] = value
                        else:
                            f[rh, k] = f[rh, k] + (value - f[rh, k]) / I[rh, k]
                    break
    return f


def center_crop (img_gray):
    
    img_PIL = PIL.Image.fromarray(img_gray)
    width, height = img_PIL.size   # Get dimensions

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
        img = img_PIL.crop((left, top, right, bottom))
        
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
        img = img_PIL.crop((left, top, right, bottom))
    else:
        img = img_PIL

    return np.asarray(img)



def fourier_redies(img_gray, bin_size=2, cycles_min=30, cycles_max=256):
    ## takes grayscale image
    
    ### center crop image
    img_gray_cropped = center_crop (img_gray)
    
    
    power = np.fft.fftshift(np.fft.fft2(img_gray_cropped.astype(float)))
    A = rotavg(np.abs(power)**2)
    A = A[:,8].copy()
        
    ### limit max frequency for small images
    
    
    if cycles_max > len(A):
        cycles_max = len(A)
        
    
    rang = np.arange(cycles_min, cycles_max + 1) - 1

    x_min = rang[0]
    x_max = rang[-1]
    
    # print(rang)
    
    using_range = A[rang]
    log_rang = np.log10(rang+1)
    log_using_range = np.log10(using_range)


    bin_mean_bar, bin_x_val = calc_bin(A, bin_size, x_min, x_max)
    
    param = np.linalg.lstsq(np.vstack([np.ones(len(bin_mean_bar[1])), np.log10(bin_mean_bar[0])]).T, np.log10(bin_mean_bar[1]), rcond=None)[0]
    
    log_m_bin = param[1]
    log_n_bin = param[0]

    SIGMA = var_eigen(log_m_bin, log_n_bin, log_rang, log_using_range)
    SLOPE = log_m_bin
    
    return SIGMA, SLOPE


################################ Branka Spehar #################################

# Original Matlab Code by Peter Kovesi

#% Copyright (c) Peter Kovesi
#% www.peterkovesi.com
#% 
#% Permission is hereby granted, free of charge, to any person obtaining a copy
#% of this software and associated documentation files (the "Software"), to deal
#% in the Software without restriction, subject to the following conditions:
#% 
#% The above copyright notice and this permission notice shall be included in 
#% all copies or substantial portions of the Software.
#%
#% The Software is provided "as is", without warranty of any kind.


def fourier_slope_branka_Spehar(img_gray, nbins=100, lowcut=2):

    ### power and ffshift
    f = np.fft.fftshift(np.fft.fft2(img_gray.astype(float), axes=(0, 1))) #,  axes=(0, 1))

    # Calculate magnitude spectrum
    mag = np.abs(f)

    # Generate a matrix 'radius' every element of which has a value
    # given by its distance from the centre. This is used to index
    # the frequency values in the spectrum.
    rows, cols = img_gray.shape
    x, y = np.meshgrid(np.arange(1, cols + 1), np.arange(1, rows + 1))

    # The following fiddles the origin to the correct position
    # depending on whether we have and even or odd size.  
    # In addition the values of x and y are normalised to +- 0.5
    if cols % 2 == 0:
        x = (x - cols / 2 - 1) / cols
    else:
        x = (x - (cols + 1) / 2) / cols
    if rows % 2 == 0:
        y = (y - rows / 2 - 1) / rows
    else:
        y = (y - (rows + 1) / 2) / rows

    radius = np.sqrt(x ** 2 + y ** 2)

    # Quantise radius to the desired number of frequency bins
    radius = np.round(radius / np.max(radius) * (nbins - 1)) + 1

    # Preallocate memory
    amp = np.zeros(nbins)
    fcount = np.ones(nbins)

    for i in range(1, nbins + 1):
         indices = np.where(radius == i)
         amp[i - 1] = np.sum(mag[indices])
         fcount[i - 1] = len(indices[0])
            
    # Average the amplitude at each frequency bin. We also add 'eps'
    # to avoid potential problems later on in taking logs.
    amp = amp / fcount + np.finfo(float).eps

    # Generate corrected frequency scale for each quantised frequency bin.
    # Note that the maximum frequency is sqrt(0.5) corresponding to the
    # points in the corners of the spectrum
    f = np.arange(1, nbins + 1) / nbins * np.sqrt(0.5)

    # Find first index value beyond the specified histogram cutoff
    fst = int(nbins * lowcut / 100)

    # Find line of best fit (ignoring specified fraction of low frequency values)
    p = np.polyfit(np.log(f[fst:]), np.log(amp[fst:]), 1)
    slope = p[0]

    return slope


################################ George Mather #################################


def rotavg_mather(array):
    N, _ = array.shape
    X, Y = np.meshgrid(np.arange(-N/2, N/2), np.arange(-N/2, N/2))
    rho = np.round(np.sqrt(X**2 + Y**2)).astype(int)
    f = np.zeros(int(N/2) + 1)
    for r in range(int(N/2) + 1):
        f[r] = np.mean(array[np.where(rho == r)])
    return f




def center_crop_mather (img_rgb): 
    # crop to largest center square with power of two
    
    img_PIL = PIL.Image.fromarray(img_rgb)
    width, height = img_PIL.size   # Get dimensions

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
            
    img = img_PIL.crop((left, top, right, bottom))
    
    return np.asarray(img)


def fourier_slope_mather(img_rgb):
    ## NO bining; num bins == num possible frequ.
    
    # # Crop the image to the largest central rectangle, power of 2
    # nr, nc, N = img_rgb.shape
    # if nr < nc:
    #     npow = np.ceil(np.log2(nr))
    #     if nr < 2**npow:
    #         nnr = 2**(npow - 1)
    #     else:
    #         nnr = 2**npow
    #     dc = nc - nnr
    #     dr = nr - nnr
    #     nnc = nnr
    # else:
    #     npow = np.ceil(np.log2(nc))
    #     if nc < 2**npow:
    #         nnc = 2**(npow - 1)
    #     else:
    #         nnc = 2**npow
    #     dr = nr - nnc
    #     dc = nc - nnc
    #     nnr = nnc
    
    # nr = nnr;
    # nc = nnc;
    
    # ci = img_rgb[int(np.round(1 + dr / 2))-1:int(np.round(dr / 2 + nr)), int(np.round(1 + dc / 2))-1:int(np.round(dc / 2 + nc)), :]
    
    ci = center_crop_mather (img_rgb)
        
    [nr,nc, _] = ci.shape
    
    print(ci.shape)
    
    ci = color.rgb2lab(ci)
    
    tmp = (ci[:, :, 0] / 100.0) *255.0  # Assuming Lab space with 'L' channel
    cg = tmp.astype(np.uint8)
    
    # Spectral slope calculation
    minf = int(np.round((nr / 2) * (1 / 25)))
    maxf = int(np.round((nr / 2) * 0.5))
    
    f = np.fft.fftshift(np.fft.fft2(cg.astype(float) / 255)) 
    impf = np.abs(f)**2
    
     # Calculate magnitude spectrum
    Pf = rotavg_mather(impf)
    f1 = np.arange(nr // 2 + 1)
    
    f11 = f1[minf-1:maxf]
    Pf1 = Pf[minf-1:maxf]
    c = np.polyfit(np.log(f11), np.log(Pf1), 1)
    slope = c[0] / 2

    return slope

