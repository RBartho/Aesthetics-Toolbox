import numpy as np
import PIL



########################################################################################################################
########################################   BOX Count Algos #############################################################
########################################################################################################################


### Branka Spehar, "2D" Box Count Algo using binary images
def fractal_dimension_2d(img_gray):
    '''
    Calculates the "2-dimensional Fractal Dimension" QIP 
    
    Input: Takes a grayscale image in Pillow format as input. 
    Output: 2-dimensional Fractal Dimension QIP
    
    Usage:
    Load images like this:
        
    Import Image from PIL    
    
    img_gray = np.asarray(Image.open( path_to_image_file ).convert('L')) 
    fractal_dimension_2d(img_gray)
    '''

    nr, nc = img_gray.shape  # get y & x dimensions of image

    # Scale image to square if not already square
    if nr > nc:
        img_gray = np.asarray(PIL.Image.fromarray(img_gray).resize((nc, nc)))
    elif nr < nc:
        img_gray = np.asarray(PIL.Image.fromarray(img_gray).resize((nr, nr)))

    threshold = np.mean(img_gray)
    b = img_gray < threshold
    b = b.astype(np.uint8)

    x, y = [], []
    i = 1
    while b.shape[0] > 6:
        x.append(b.shape[0])
        y.append(np.sum(b))

        c = np.zeros((b.shape[0]//2, b.shape[1]//2))
        for xx in range(c.shape[0]):
            for yy in range(c.shape[1]):

                c[xx, yy] = np.sum (  b[xx*2  : xx*2 + 2  , yy*2 : yy*2 + 2 ]  )

        b = (c > 0) & (c < 4)
        i += 1

    params = np.polyfit(np.log2(x[1:]), np.log2(y[1:]), 1)
    D = params[0]
    return D



### George Mather, "3D" Box Count Algo unsing graylevels
def fractal_dimension_3d(img_gray):  
    '''
    Calculates the "3-dimensional Fractal Dimension" QIP 
    
    Input: Takes a grayscale image in Pillow format as input. 
    Output: 3-dimensional Fractal Dimension QIP
    
    Usage:
    Load images like this:
        
    Import Image from PIL    
    
    img_gray = np.asarray(Image.open( path_to_image_file ).convert('L')) 
    fractal_dimension_3d(img_gray)
    '''

    ### center crop largest rectangle image with power of 2
    nr, nc = img_gray.shape
    # Find largest square that is a power of 2 (for box count)
    if nr < nc:
        nk = 2**np.ceil(np.log2(nr))
        nnr = 2**(np.ceil(np.log2(nr)) - 1) if nr < nk else 2**np.ceil(np.log2(nr))
        dc = nc - nnr
        dr = nr - nnr
        nnc = nnr
    else:
        nk = 2**np.ceil(np.log2(nc))
        nnc = 2**(np.ceil(np.log2(nc)) - 1) if nc < nk else 2**np.ceil(np.log2(nc))
        dr = nr - nnc
        dc = nc - nnc
        nnr = nnc
    nr, nc = int(nnr), int(nnc)
    # Centred crop
    I = img_gray[int(round(dr / 2)):int(round(dr / 2 + nr)), int(round( dc / 2)):int(round(dc / 2 + nc))]

    ### calc box counts
    nr, nc = I.shape
    # Calculate min and max box sizes
    minpow = int(np.ceil(np.log2(nr**(1/3))))

    bmin = 2**minpow
    bmax = bmin
        
    while np.ceil(nr / bmax + 1) <= np.ceil(nr / (bmax - 1)):
        bmax = bmax + 1
        
    boxes = np.arange(bmin, bmax + 1, 2)

    boxHeights = boxes * (1 / nr)  # box size in greylevels

    boxCounts = np.zeros(len(boxes))
    boxSizes = np.zeros(len(boxes))

    # loop through the box sizes
    for b in range(len(boxes)):
        
        bs = boxes[b]
        bh = boxHeights[b]  # box size in graylevels

        # Divide the image into a grid of boxes (bs x bs).
        # Loop through the cells in the grid, calculating the box count for
        # each and adding it to the running total.
        # Overlap columns by one x-pixel
        boxCount = 0
        for by in range(1, nc - bs, bs):
            
            for bx in range(1, nr - bs + 1, bs-1):
                submat = I[by-1: by + bs - 1 , bx-1 : bx + bs - 1 ]
                l = np.max(submat)
                k = np.min(submat)

                if l == k:
                    b1 = 1
                else:
                    b1 = np.ceil((l - k) / bh)
                boxCount = boxCount + b1

        # Now use the range of box sizes to calculate D
        boxCounts[b] = boxCount
        boxSizes[b] = 1.0 / bs

    dfit = np.polyfit(np.log(boxSizes), np.log(boxCounts), 1)
    D = dfit[0]
    return D  
    