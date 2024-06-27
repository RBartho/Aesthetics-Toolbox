import numpy as np
from skimage import color
import PIL
import statsmodels.api as sm

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


def padding_and_resizing_to_square_1024_pixel(img):
   

    mean = np.round(np.mean(img)).astype(np.uint8) # mean gray value for padding
    
    ### resize longer side to 1024 pixels, maintain aspect ratio
    img = PIL.Image.fromarray(img)
    if img.size[0] >= img.size[1]:
        a = 1024 / float(img.size[0])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    else:
        a = 1024 / float(img.size[1])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    
    ### padding with mean gray value
    img = np.asarray(img)
    h,w = img.shape
    w_c = int(w/2)
    h_c = int(h/2)
    if h > w: 
        img_pad = np.full([h,h], mean) 
        if w%2 == 1: # uneven width
            img_pad[ :  ,  h_c - w_c : h_c + w_c +1  ] = img
        else:
            img_pad[ :  ,  h_c - w_c : h_c + w_c  ] = img
        img = img_pad
    elif h < w:
        img_pad = np.full([w,w], mean)  
        if h%2 == 1: # uneven height
            img_pad[w_c - h_c : w_c + h_c +1  , :  ] = img
        else: 
            img_pad[w_c - h_c : w_c + h_c  , :  ] = img     
        img = img_pad
        
    return img
    

def fourier_redies(img_gray, bin_size=2, cycles_min=10, cycles_max=256):
    '''
    Calculates the 'Fourier Slope **Redies** and the Fourier Sigma' QIPs 
    
    Input: 8 bit grayscale image in Pillow format
    Output: Fourier Slope **Redies** and the Fourier Sigma
    
    Usage:
    Import Image from PIL    

    img_gray = np.asarray(Image.open( path_to_image_file ).convert('L')) 
    fourier_redies(img_gray)
    '''
    
    
    ### center crop image
    img_gray_resized = padding_and_resizing_to_square_1024_pixel(img_gray)

    power = np.fft.fftshift(np.fft.fft2(img_gray_resized.astype(float)))
    A = rotavg(np.abs(power)**2)
    A = A[:,8].copy()
        
    ### limit max frequency for small images
    if cycles_max > len(A):
        cycles_max = len(A)
        
    rang = np.arange(cycles_min, cycles_max + 1) - 1

    x_min = rang[0]
    x_max = rang[-1]

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


################################ Zoey Isherwoods & Branka Spehar #################################


'''
  Translation to Python 3 from Zoey Isherwoods Matlab Code on GitHub:
  https://github.com/zoeyisherwood/pp-spatiotemp
  
  Isherwood, Z. J., Clifford, C. W. G., Schira, M. M., Roberts, M. M. & Spehar, B. (2021) 
  Nice and slow: Measuring sensitivity and visual preference toward naturalistic stimuli 
  varying in their amplitude spectra in space and time. Vision Research 181, 47-60, 
  doi:10.1016/j.visres.2021.01.001.
  
  rot_avg.m function by Bruno Olshausen
  
  Before fitting the data, outliers are removed in the linear fit (not the log-log fit) if Cook's distance > n/4. 
  This basically removes the low frequencies for most images.

'''


def rot_avg(array):
    """
    rotavg.m - Matlab function to compute rotational average of (square) array
    by Bruno Olshausen
    N should be even.
    """
    N, N = array.shape

    X, Y = np.meshgrid(np.arange(-N/2, N/2), np.arange(-N/2, N/2))
    rho = np.sqrt(X**2 + Y**2).round().astype(int)

    f = np.zeros((N//2 + 1))

    for r in range(N//2 + 1):
        mask = (rho == r)
        if np.any(mask):
            f[r] = np.mean(array[mask])

    return f


def CooksDistance_SM(X, y):
    '''
    computes the Cook's distance using the statsmodel package'
    '''
    
    # add constant value
    X = sm.add_constant(X.reshape(-1, 1))
    # fit the model
    model = sm.OLS(y,X).fit()
    # Get influence measures
    influence = model.get_influence()
    # Calculate Cook's distance
    cooks_d = influence.cooks_distance[0] 
    # Output the results
    return cooks_d


def fourier_slope_branka_Spehar_Isherwood(img_gray):
    '''
    Calculates the 'Fourier Slope **Spehar**' QIP
    
    Input: 8 bit grayscale image in Pillow format
    Output: Fourier Slope **Spehar**
    
    Usage:
    Import Image from PIL    

    img_gray = np.asarray(Image.open( path_to_image_file ).convert('L')) 
    fourier_slope_branka_Spehar_Isherwood(img_gray)
    '''
    
    img_gray = np.asarray(img_gray)


    # Adjust image size to be even
    if img_gray.shape[0] % 2 == 1:
        img_gray = img_gray[:-1, :]
    if img_gray.shape[1] % 2 == 1:
        img_gray = img_gray[:, :-1]

    # Ensure the input is square, center cropping to larges square with power of 2
    if img_gray.shape[0] != img_gray.shape[1]:
        s_original = img_gray.shape
        s_trim = min(2**int(np.log2(s_original[0])), 2**int(np.log2(s_original[1])))
        center_x, center_y = s_original[0] // 2, s_original[1] // 2
        img_gray = img_gray[center_x - s_trim // 2:center_x + s_trim // 2,
                                  center_y - s_trim // 2:center_y + s_trim // 2]

    # Calculate spatial slope
    # remove outliers/e.g. low frequencies first
    xsize, ysize = img_gray.shape
    
    imf = np.fft.fftshift(np.fft.fft2(img_gray.astype(float)))

    impf = np.abs(imf)
    Pf = rot_avg(impf)
    x_vec = np.arange(1, xsize // 2 + 1)
    y_vec = Pf[1:ysize // 2 + 1]

    cook_distance = CooksDistance_SM(x_vec, y_vec)
    outliers = cook_distance > 4 / len(x_vec)
    x_vec = x_vec[~outliers]
    y_vec = y_vec[~outliers]
    
    # Log-log fit
    A_loglog = np.log(x_vec)
    B_loglog = np.log(y_vec)
    b_loglog, _ = np.polyfit(A_loglog, B_loglog, 1)

    spatialSlope_logFit = b_loglog

    return spatialSlope_logFit


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
    '''
    Calculates the 'Fourier Slope **Mather**' QIP
    
    Input: 8 bit grayscale image in Pillow format
    Output: Fourier Slope **Mather**
    
    Usage:
    Import Image from PIL    
       
    img_gray = np.asarray(Image.open( path_to_image_file ).convert('L')) 
    fourier_slope_mather(img_gray)
    '''

    ci = center_crop_mather (img_rgb)
        
    [nr,nc, _] = ci.shape

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
