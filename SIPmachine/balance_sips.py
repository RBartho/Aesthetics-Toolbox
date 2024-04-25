import numpy as np
from skimage.transform import rotate
from skimage.filters import threshold_otsu



########################################################################################
################################# Huebner Group ########################################
########################################################################################


def APB_Score(im):
    '''
    1. nall sollte Zahl der Scharzen Pixel sein, ist hier aber die Summer der Intensitätswerte im Bild
    2. Im Matlab code wird der treshold wert 126 in zwei Schleifen addiert!!! Hier auch so übernommen, ist aber eigentlich ein Fehler.
    '''
    
    height, width = im.shape

    hist = np.histogram(im, bins=256, range=(0, 256))

    counts = hist[0]
    
    thres = 128

    sum1 = sum(counts[:thres])
    sum2 = sum(counts[thres-1:])  # hier Fehler in Berechnungen, aber kaum Auswirkunge auf Ergebnisse
    
    if sum1 <= sum2:
        im_comp = 255 - im  # Invert image
    else:
        im_comp = im

    nall = np.sum(im_comp)   ### Number of Pixels with value of 0
    
    #print('NALL:', nall)
    
    ## to avoid division 0
    if nall == 0:
        nall = 1

    # Horizontal balance
    w = width // 2
    


    s1 = np.sum(im_comp[:, :w], dtype=int)
    s2 = np.sum(im_comp[:, -w:], dtype=int)
    bh = (abs(s1 - s2) / nall) * 100  
        
    w2 = width // 4 # adding center row of w to middle area if w uneven 

    s1 = np.sum(im_comp[:, :w2], dtype=int)
    s2 = np.sum(im_comp[:, -w2:], dtype=int)

    bioh = (abs((nall - (s1 + s2)) - (s1 + s2)) / nall) * 100 # %  inner-outer horizontal 

    # Vertical balance
    h = height // 2

    s1 = np.sum(im_comp[:h, :], dtype=int)
    s2 = np.sum(im_comp[-h:, :], dtype=int)
    bv = (abs(s1 - s2) / nall) * 100
    
    h2 = height // 4
    s1 = np.sum(im_comp[:h2, :], dtype=int)
    s2 = np.sum(im_comp[-h2:, :], dtype=int)

    biov = (abs((nall - (s1 + s2)) - (s1 + s2)) / nall) * 100

    # Main diagonal and inner-outer (bottom right top left)
    s1 = np.sum(np.triu(im_comp, 1), dtype=int)
    s2 = np.sum(np.tril(im_comp, -1), dtype=int)
    bmd = (abs(s1 - s2) / nall) * 100

    prop = 1 / np.sqrt(2)
    b1 = height - int(height * prop)
    b2 = width - int(width * prop)
    s1 = np.sum(np.tril(im_comp, -b1), dtype=int)
    s2 = np.sum(np.triu(im_comp, b2), dtype=int)
    biomd = (abs((nall - (s1 + s2)) - (s1 + s2)) / nall) * 100

    # Anti-diagonal and inner-outer (bottom right top left)
    im_comp = np.rot90(im_comp)
    s1 = np.sum(np.triu(im_comp, 1), dtype=int)
    s2 = np.sum(np.tril(im_comp, -1), dtype=int)
    bad = (abs(s1 - s2) / nall) * 100

    s1 = np.sum(np.tril(im_comp, -b2), dtype=int)
    s2 = np.sum(np.triu(im_comp, b1), dtype=int)
    bioad = (abs((nall - (s1 + s2)) - (s1 + s2)) / nall) * 100

    bs = (bh + bv + bioh + biov + bmd + biomd + bad + bioad) / 8

    return bs




def DCM_Key(im):
    '''
    Input grayscale in range [0-256]
    
    '''
    
    height, width = im.shape

    hist = np.histogram(im, bins=256, range=(0, 256))
    counts = hist[0]
       
    thres = 128

    sum1 = sum(counts[:thres])
    sum2 = sum(counts[thres:])
    

    if sum1 <= sum2:
        im_comp = 255 - im  # Invert image
        inv = 'inverted';
    else:
        im_comp = im
        inv = 'original';

    nall = np.sum(im_comp)   ### Number of Pixels with value of 0
    
    # Horizontal balance point
    r = 0
    for i in range(width):
        w = np.sum(im_comp[:, i],dtype=float)
        r += w * i
    Rh = np.round(r / nall) + 1  # x position of fulcrum
    Rhnorm = Rh / width  # Normalized
    

    # Vertical balance point
    r = 0
    for i in range(height):
        w = np.sum(im_comp[i, :],dtype=float)
        r += w * i
    Rv = np.round(r / nall) + 1  # y position of fulcrum
    Rvnorm = Rv / height  # Normalized

    htmp = 0.5 - Rhnorm
    vtmp = 0.5 - Rvnorm

    dist = np.sqrt(htmp ** 2 + vtmp ** 2)
    rdist = (dist / 0.5) * 100

    # Calculate direction in degrees
    xcenter = width / 2
    ycenter = height / 2

    # Direction goes from 0 to 180° (upper half, right to left), from 0 to -180° lower half (right to left)
    direction = np.degrees(np.arctan2(ycenter - Rv, Rh - xcenter))

    if (direction >= 45) and (direction < 135):
        area = 1  # top
    elif (direction >= 135) or (direction < -135):
        area = 2  # left
    elif (direction >= -135) and (direction < -45):
        area = 3  # bottom
    else:
        area = 4  # right

    return rdist


def MS_Score(img_gray):

    # Automatically find optimal threshold level
    level  = threshold_otsu(img_gray)

    # Convert image to binary
    BW = img_gray <= level

    s = BW.shape
    height = s[0]
    width = s[1]

    # Horizontal axis of reflection (vertical reflection)
    if height % 2 == 0:  # even number
        h2 = height // 2
    else:
        h2 = (height - 1) // 2
    n1 = h2 - 1 # why?
    
    
    sym = 0
    for i in range(width):
        for j in range(h2):
            #print(i,j, sym)
            sym += (BW[j, i] * BW[ (height-1) - (j), i]) * (1 + j / n1)
    Sh = sym * (2 / (3 * width * h2))

    # Vertical axis of reflection (horizontal reflection)
    if width % 2 == 0:  # even number
        w2 = width // 2
    else:
        w2 = (width - 1) // 2
    n1 = w2 - 1
    
    sym = 0
    for i in range(height):
        for j in range(w2):
            sym += (BW[i, j] * BW[i, (width-1) - j]) * (1 + j / n1)
    Sv = sym * (2 / (3 * height * w2))

    if width == height:
        # Major diagonal of reflection (ONLY FOR SQUARES)
        sym = 0
        n = 1  # Pixels until diagonal
        for i in range(1,height):
            for j in range(n):
                #print(i,j,n)
                sym += (BW[i, j] * BW[j, i]) * (1 + (j+1) / n)
            n += 1
            
        Smd = sym * (2 / (3 * height * (width - 1) / 2))
            
        # Minor diagonal of reflection (ONLY FOR SQUARES)
        BW = rotate(BW, 90)
        sym = 0
        n = 1  # Pixels until diagonal
        for i in range(1, height):
            for j in range(n):
                sym += (BW[i, j] * BW[j, i]) * (1 + (j+1) / n)
            n += 1
        Sad = sym * (2 / (3 * height * (width - 1) / 2))

        ms = ((Sh + Sv + Smd + Sad) / 4) * 100
    else:
        ms = ((Sh + Sv) / 2) * 100

    return ms


def entropy_score_2d(im):  ## takes grayscale image!!

    # number of bins taken from original paper: Hübner & Fillinger. Comparison of Objective Measures for Predicting Perceptual Balance and Visual Aesthetic Preference. Page: 4
    hbins = 10;
    vbins = 10;
    
    height, width = im.shape
    
    hist = np.histogram(im, bins=256, range=(0, 256))
    counts = hist[0]
    thres = 128
    sum1 = sum(counts[:thres])
    sum2 = sum(counts[thres-1:])  # hier Fehler in Berechnungen, aber kaum Auswirkunge auf Ergebnisse
    if sum1 <= sum2:
        im = 255 - im  # Invert image
        print('inverted')
    else:
        im = im
    
    
    level  = threshold_otsu(im)
    
    BW = im > level

    hinc = width // hbins
    vinc = height // vbins
    
    x = np.zeros((vbins, hbins))
    
    ## summing up black pixels in cells
    for i in range(hbins+1):
        for j in range(vbins+1):
            if (i!=hbins) and (j!=vbins): # inner pieces
                x[j,i] = np.sum( BW[ vinc * j : (j+1) * vinc ,  hinc*i : hinc * (i+1)     ]    )
            elif (i<hbins) and (j==vbins): # residuals vertical
                x[j-1,i]   += np.sum( BW[ vinc * j :  ,  hinc*i : hinc * (i+1)     ]    )
            elif (i==hbins) and (j<vbins): # residuals horizontal
                x[j,i-1]   += np.sum( BW[ vinc * j : (j+1) * vinc ,  hinc*i :      ]    )
            elif (i==hbins) and (j==vbins): # residuals horizontal
                x[j-1,i-1] += np.sum( BW[ vinc * j :  ,  hinc*i :     ]    )
    
    nbins = hbins * vbins
    max_entropy = np.log2(nbins)
    
    xh = x.flatten(order='F')
    all_sum = np.sum(xh)
    
    # horizontal entropy
    max_entropy = np.log2(hbins)   
    y = np.sum(x, axis=0) / all_sum
    j = np.nonzero(y)
    en = -np.sum(y[j] * np.log2(y[j]))
    en_hori = (en / max_entropy) * 100
    
    #vertical entropy
    max_entropy = np.log2(vbins)
    y = np.sum(x.T, axis=0) / all_sum
    j = np.nonzero(y)
    en = -np.sum(y[j] * np.log2(y[j]))
    en_vert = (en / max_entropy) * 100

    # average of hori and vert entropy
    en_av = (en_hori + en_vert) / 2
    
    return en_av
