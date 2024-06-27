import numpy as np
from skimage.transform import resize
from skimage.color import rgb2lab


################################# PHOG SIPs (Self-similarity, Anisotropy, Complexity) ########################################


def resize_img(img, re): 
    if re>1:
        s = img.shape
        b = s[0]*s[1]
        d = np.sqrt(re/b)
        s_new = np.round([s[0]*d, s[1]*d]).astype(np.int32)
        img = resize(img, s_new, order=3, anti_aliasing=True) *255
        return img.astype(np.uint8)
    
    else:
        return img
    

def absmaxND(a, axis=2):
    amax = a.max(axis)
    amin = a.min(axis)
    return np.where(-amin > amax, amin, amax)




def maxGradient_fast(Img):

    gradY_t, gradX_t = np.gradient(Img, axis = [0,1], edge_order=1)
    
    gradientX = absmaxND(gradX_t)
    gradientY = absmaxND(gradY_t)

    return gradientX, gradientY



def computeDescriptor(GradientValue, GradientAngle, bins, angle, levels, section, is_global=False):
    descriptor = []

    intervalSize = angle / bins
    halfIntervalSize = (angle / bins) / 2
    
    # Level 0
    ind = ((GradientAngle >= angle - halfIntervalSize) | (GradientAngle < halfIntervalSize))
    descriptor.append(np.sum(GradientValue[ind]))

    for b in range(1, bins):
        ind = ((GradientAngle >= (b * intervalSize) - halfIntervalSize) & (GradientAngle < ((b + 1) * intervalSize) - halfIntervalSize))
        descriptor.append(np.sum(GradientValue[ind]))

    ### local normaliszation for global
    if is_global:
        descriptor = normalizeDescriptor(descriptor, bins)

    # Other levels
    for l in range(1, levels + 1):
        cellSizeX = GradientAngle.shape[1] / (section ** l)
        cellSizeY = GradientAngle.shape[0] / (section ** l)
        
        if cellSizeX < 1 or cellSizeY < 1:
            raise ValueError("Cell size is less than 1. Adjust the number of levels.")

        for j in range(1, section ** l + 1):

            leftX = 1 + np.round((j - 1) * cellSizeX).astype(np.int64)
            rightX = np.round(j * cellSizeX).astype(np.int64)
            
            for i in range(1, section ** l + 1):

                topY = 1 + np.round((i - 1) * cellSizeY).astype(np.int64)
                bottomY = np.round(i * cellSizeY).astype(np.int64)

                GradientValueCell = GradientValue[topY - 1:bottomY, leftX - 1:rightX]
                GradientAngleCell = GradientAngle[topY - 1:bottomY, leftX - 1:rightX]

                ind = ((GradientAngleCell >= angle - halfIntervalSize) | (GradientAngleCell < halfIntervalSize))
                local_descriptor = [np.sum(GradientValueCell[ind])]

                for b in range(1, bins):
                    ind = ((GradientAngleCell >= (b * intervalSize) - halfIntervalSize) & (GradientAngleCell < ((b + 1) * intervalSize) - halfIntervalSize))
                    local_descriptor.append(np.sum(GradientValueCell[ind]))

                if is_global:
                    local_descriptor = normalizeDescriptor(local_descriptor, bins);
                    descriptor.extend(local_descriptor)
                else:
                    descriptor.extend(local_descriptor)

    if is_global:
        descriptorglobal = normalizeDescriptorGlobal(descriptor)
        return descriptorglobal
    else:
        return descriptor


def computePHOGLAB(Img, angle, bins, levels, section):
    
    GradientX, GradientY = maxGradient_fast(Img)
    
    # Calculate the norm (strength) of Gradient values
    GradientValue = np.sqrt( np.square(GradientX) + np.square(GradientY) )
    
    # Replace zeros in GradientX with a small value to avoid Zero division
    GradientX[np.where(GradientX == 0)] = 1e-5
    
    YX = GradientY / GradientX

    if angle == 180:
        GradientAngle = ((np.arctan(YX) + (np.pi / 2)) * 180) / np.pi
    elif angle == 360:
        GradientAngle = ((np.arctan2(GradientY, GradientX) + np.pi) * 180) / np.pi
    else:
        raise ValueError("Invalid angle value. Use 180 or 360.")
        
    descriptor = computeDescriptor(GradientValue, GradientAngle, bins, angle, levels, section)
    
    return descriptor, GradientValue, GradientAngle
    

def convert_to_matlab_lab(img_rgb):
    '''
    Matlab has a different range for the channels of the LAB color space.
    We need to scale to the Matlab ranges, to get the same results
    '''
    
    img = rgb2lab(img_rgb) 

    #L: 0 to 100, a: -127 to 128, b: -128 to 127
    img[:,:,0] = np.round(np.array((img[:,:,0] / 100) * 255 )).astype(np.int32)
    img[:,:,1] = np.round(np.array(img[:,:,1] + 128).astype(np.int32))
    img[:,:,2]= np.round(np.array(img[:,:,2] + 128).astype(np.int32))
    
    return img.astype(np.uint16)
    

def normalizeDescriptor(descriptor, bins):
    b = np.reshape(descriptor, (bins, len(descriptor) // bins), order='F')
    c = np.sum(b, axis=0)
    s = b.shape
    
    temp = np.zeros((s[0], s[1]))

    for i in range(s[1]):
        if c[i] != 0:
            temp[:, i] = b[:, i] / c[i]
        else:
            temp[:, i] = b[:, i]
    
    normalizeddescriptor = np.reshape(temp, len(descriptor), order='F')
    return list(normalizeddescriptor)


def normalizeDescriptorGlobal(descriptor):
    if np.sum(descriptor) != 0:
        normalizeddescriptorGlobal = descriptor / np.sum(descriptor)
        return normalizeddescriptorGlobal
    else:
        return list(descriptor)


def computeWeightedDistances(descriptor, bins, levels, section, descriptornn):
    distances = []

    comparisonglobal = descriptor[:bins]

    temp = np.zeros((levels, 2), dtype=int)

    temp[0, 0] = bins + 1
    temp[0, 1] = section ** (2) * bins + temp[0, 0] - 1

    for i in range(1, levels):
        temp[i, 0] = temp[i - 1, 1] + 1
        temp[i, 1] = section ** ((i+1) * 2) * bins + temp[i, 0] - 1

    distances.append(np.sum(comparisonglobal))

    for i in range(levels):
        for j in range(temp[i, 0], temp[i, 1] + 1, bins):
            j = j-1
            part = descriptor[j:j + bins]
            
            if (np.max(comparisonglobal) > 1e-8) and (np.max(part) > 1e-8):
                dist1 = np.sum(np.minimum(comparisonglobal, part))

                m1 = np.mean(descriptornn[:bins])
                m2 = np.mean(descriptornn[j:j + bins])

                area = section ** ((i+1) * 2)
                m2 = m2 * area

                if m1 < 1e-8 or m2 < 1e-8:
                    strengthsimilarity = 0
                elif m1 > m2:
                    strengthsimilarity = m2 / m1
                else:
                    strengthsimilarity = m1 / m2

                dist1 = dist1 * strengthsimilarity
                distances.append(dist1)
            else:
                distances.append(0)

    return distances

def computeSD(descriptorglobal, bins, levels, section):
    temp = np.zeros((levels, 2), dtype=int)
    temp[0, 0] = bins + 1
    temp[0, 1] = section ** (2) * bins + temp[0, 0] - 1
    
    for i in range(1, levels):
        temp[i, 0] = temp[i - 1, 1] + 1
        temp[i, 1] = section ** ((i+1) * 2) * bins + temp[i, 0] - 1
        
    descript = descriptorglobal[temp[levels - 1, 0]-1 : temp[levels - 1, 1]]
    
    sdvalue = np.std(descript)
    return sdvalue


def displayDistances(distances, bins, levels, section):
    distanceatlevel = []
    
    temp3 = np.zeros([levels+1, 2], dtype=int)
    # print('###########', temp3, levels)
    temp3[0, 0] = 1
    temp3[0, 1] = 1

    for i in range(levels):
        temp3[i+1, 0] = section ** (2 * (i+1))
        temp3[i+1, 1] = temp3[i+1, 0] + temp3[i, 1]

    distanceatlevel = np.median(distances[temp3[levels - 1, 1] :temp3[levels, 1]])

    return distanceatlevel


def PHOGfromImage(img_rgb, section=2, bins=16, angle=360, levels=3, re=-1, sesfweight=[1,1,1] ):
    '''
    Calculates the PHOG QIPs 'Anisotropy, Complexity, PHOG-based Self-similarity'
    
    Input: 8 bit rgb image in Pillow format
    Output: Anisotropy, Complexity, PHOG-based Self-similarity
    
    Usage:
    Import Image from PIL    
       
    img_rgb = np.asarray(Image.open( path_to_image_file ).convert('RGB')) 
    PHOGfromImage(img_rgb)
    '''
    
    img = resize_img(img_rgb, re)
    img = convert_to_matlab_lab(img)

    descriptor, GradientValue , GradientAngle = computePHOGLAB(img, angle, bins, levels, section)
    descriptornn = descriptor

    descriptor=normalizeDescriptor(descriptor,bins)

    descriptorglobal = computeDescriptor(GradientValue, GradientAngle, bins, angle, levels, section, is_global=True)
    
    distances=computeWeightedDistances(descriptor,bins,levels,section,descriptornn);

    anisotropy = computeSD(descriptorglobal, bins, levels, section)
    complexity = np.mean(GradientValue)

    # self_sim
    distancesatlevel=0;
    distancesateachlevel = []
    for i in range(levels):
       distancesateachlevel.append(displayDistances(distances,bins,i+1,section));
       distancesatlevel=distancesatlevel+distancesateachlevel[i]*sesfweight[i];
    self_sim=distancesatlevel/sum(sesfweight);      
        
    return self_sim, complexity, anisotropy


