import numpy as np
import PIL

PIL.Image.MAX_IMAGE_PIXELS = 933120000



# scale to number of pixels
############################################### Seitenverhältnis beibehalten

def scale_longer_side_keep_aspect_ratio(file_path, longer_side):
    img = PIL.Image.open(file_path)
    if img.size[0] >= img.size[1]:
        a = longer_side / float(img.size[0])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    else:
        a = longer_side / float(img.size[1])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img
        

def scale_shorter_side_keep_aspect_ratio(file_path, shorter_side):
    img = PIL.Image.open(file_path)
    if img.size[0] <= img.size[1]:
        a = shorter_side / float(img.size[0])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    else:
        a = shorter_side / float(img.size[1])
        img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img


def scale_to_width_keep_aspect_ratio(file_path, width=1000):
    img = PIL.Image.open(file_path)
    a = width / float(img.size[0])
    img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img

def scale_to_height_keep_aspect_ratio(file_path, height=1000):
    img = PIL.Image.open(file_path)
    a = height / float(img.size[1])
    img = img.resize((int(img.size[0]*a),int(img.size[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img
        
def scale_to_resolution(file_path, width=1000, height=1000):
    img = PIL.Image.open(file_path)
    img = img.resize((int(width),int(height)), PIL.Image.Resampling.LANCZOS)
    return img


def scale_to_number_of_pixels_keep_aspect_ratio(file_path, num_pixels=100000):
    img = PIL.Image.open(file_path)
    s = img.size
    print(s)
    old_num_pixels = s[0]*s[1]
    d = np.sqrt(num_pixels/old_num_pixels)
    s_new = np.round([s[0]*d, s[1]*d]).astype(np.int32)
    img = img.resize((s_new[0],s_new[1]), PIL.Image.Resampling.LANCZOS)
    return img

def resize_to_fit_display(file_path, disp_width=1920, disp_height=1080):
    img = PIL.Image.open(file_path)
    print(img.size)
    disp_ratio = disp_width/disp_height
    s = img.size
    img_ratio = s[0] / s[1] 
    if img_ratio > disp_ratio:  # --> resize img to disp_hight,while maintaining image aspect ratio
        print('A')
        a = disp_width / float(img.size[0])
        img = img.resize((int(s[0]*a),int(s[1]*a)), PIL.Image.Resampling.LANCZOS)
    else: #  resize img to disp_width ,while maintaining image aspect ratio
        print('B')
        a = disp_height / float(img.size[1])
        img = img.resize((int(s[0]*a),int(s[1]*a)), PIL.Image.Resampling.LANCZOS)
    return img


# #file_path = '/home/ralf/Documents/18_SIP_Machine/GUI_streamlit/images_style/O-Martinez_Eddie_02.jpg'
# file_path = '/home/ralf/Documents/18_SIP_Machine/GUI_streamlit/images_style/test.jpg'
    


# img = scale_to_number_of_pixels_keep_aspect_ratio(file_path , num_pixels=100000)
# print(img.size)


# img = scale_to_width_keep_aspect_ratio(file_path, width=1000)
# print(img.size)

# img = resize_to_fit_display(file_path, disp_width=1920, disp_height=1080)
# print(img.size)
