import streamlit as st

st.set_page_config(layout="wide")

st.markdown(""" <style> .font1 {
font-size:20px ; font-family: 'Cooper Black'; color: black;} 
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .head {
font-size:35px ;  font-family: 'Cooper Black'; color: #FF9633;}
</style> """, unsafe_allow_html=True)

st.markdown(""" <style> .greenL {
font-size:28px ; font-family: 'Cooper Black'; color: green;} 
</style> """, unsafe_allow_html=True)

def build_entry(QIP , Image_preproc, CComplex, Range, API, References, Notes):
    
    Button = st.sidebar.checkbox(QIP , value=True)
    
    if Button:
    
        st.divider()
        st.write('')  

        
        st.markdown('<p class="greenL"> ' + QIP + ' </p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns( [0.2, 0.8])
        with col1:
            st.markdown('<p class="font1"> Image preprocessing: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> Computational complexity: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> Range of values: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> API: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> References: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> Notes: </p>', unsafe_allow_html=True)
            
        
        with col2:
            st.markdown('<p class="font1"> ' + Image_preproc + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + CComplex      + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + Range           + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + API           + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + References    + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + Notes         + '  </p>', unsafe_allow_html=True)


st.markdown('<p class="head">QIP Documentation</p>', unsafe_allow_html=True)
st.markdown('<p class="font1">This is the documentation for the QIP machine. Detailed information on the individual QIPs can be found in the publication: \
            Christoph Redies, Ralf Bartho, Lisa Koßmann, Branka Spehar, Ronald Hübner, Johan Wagemans, and Gregor U. Hayn-Leichsenring: \
            A toolbox for calculating objective image properties in aesthetics research. \
            The publication describes the motivation for using each QIP, the algorithm itself \
            and related publications. (https://arxiv.org/abs/2408.10616) </p>', unsafe_allow_html=True)

build_entry(
            QIP           = 'Image size' , 
            Image_preproc = 'RGB image, no resizing', 
            CComplex      = 'low', 
            Range         = '[0 - inf)',
            API           = 'AT.color_and_simple_qips.image_size(img_RGB)', 
            References    = 'Datta et al., 2006', 
            Notes         = 'Default: Image size = image width + image height in pixel. There are several different ways implemented to calculate this property, including the product of height and width, the diagonal, or the maximum, average, or minimum of height and width.'
            )

build_entry(
            QIP           = 'Aspect ratio' , 
            Image_preproc = 'RGB image, no resizing', 
            CComplex      = 'low', 
            Range         = '(0 - inf)',
            API           = 'AT.color_and_simple_qips.aspect_ratio(img_RGB)', 
            References    = 'Datta et al., 2006;  Li et al., 2006; Iigaya et al., 2021', 
            Notes         = 'Aspect ratio = image_width / image_height'
            )

build_entry(
            QIP           = 'RMS contrast' , 
            Image_preproc = 'Converting to L*a*b* color space, no resizing', 
            CComplex      = 'low', 
            Range         = '[0 - 50)',
            API           = 'AT.color_and_simple_qips.std_channels(img_LAB)', 
            References    = 'Peli, 1990', 
            Notes         = 'RMS contrast = standard deviation of the Lightness channel of the L*a*b* color space'
            )



build_entry(
            QIP           = 'Ligthness entropy' , 
            Image_preproc = 'Converting to L*a*b* color space, scaling pixel range to [0-255]', 
            CComplex      = 'low', 
            Range         = '[0 - 8]',
            API           = 'AT.color_and_simple_qips.shannonentropy_channels(img_LAB)', 
            References    = 'Shannon, 1948; Kersten, 1987; Mather, 2018', 
            Notes         = 'Ligtness entropy = shannon entropy of the Lightness channel (L*a*b*)'
            )

build_entry(
            QIP           = 'HOG Anisotropy, HOG Complexity, HOG Self-similarity' , 
            Image_preproc = 'Converting to Matlabs L*a*b* color space, optional resizing to number of pixel (-1 = no resizing)', 
            CComplex      = 'high', 
            Range         = '',
            API           = 'AT.PHOG_qips.PHOGfromImage(img_rgb, section, bins, angle, levels, re, sesfweight )', 
            References    = 'Braun et al., 2013; Redies and Groß, 2013; Dalal and Triggs, 2005; Bosch et al.,2007', 
            Notes         = 'By default, image resizing is disabled (parameter is set to -1). The resize function of the original \
                            Matlab script is different from the available Python implementations. Calculating HOG-derived QIPs with resizing will \
                            give results different from the original Matlab script. Without resizing, the results are the same.'
            )

build_entry(
            QIP           = 'Edge density, 1st-order and 2nd-order Edge_orientation entropy' , 
            Image_preproc = 'Converting to 8-bit grayscale image, resizing to 120.000 pixel while maintaining aspect ratio', 
            CComplex      = 'very high', 
            Range         = '',
            API           = 'AT.edge_entropy_qips.do_first_and_second_order_entropy_and_edge_density (img_gray)', 
            References    = 'Redies et al., 2017', 
            Notes         = 'The 2nd-order Edge_orientation entropy compares the orientation and strength of the 10,000 strongest edge pixels in pairs, \
                            which is computationally intensive. A fast C++ implementation of this QIP can be found in the following \
                            Github repository: https://github.com/RBartho/C-version-2nd-Order-Edge-Orientation-Entropy'
            )

build_entry(
            QIP           = 'Color entropy' , 
            Image_preproc = 'Converting to HSV color space, no resizing', 
            CComplex      = 'low', 
            Range         = '[0 - 8] for range of hue values [0-255]',
            API           = 'AT.color_and_simple_qips.shannonentropy_channels(img_HSV)', 
            References    = 'Geller et al., 2022', 
            Notes         = 'Color entropy is calculated as the Shannon entropy of the Hue channel of the HSV color space.'
            )

build_entry(
            QIP           = 'Mean value of RGB, HSV and L*a*b* color channels' , 
            Image_preproc = 'Converting to respective color spaces (RGB, HSV, L*a*b*), no resizing', 
            CComplex      = 'low', 
            Range         = 'RGB [0 - 255] ;  HSV[0 - 1] ;  L* [0-100],  a* [] b* []',
            API           = 'AT.color_and_simple_qips.mean_channels(img)  and  AT.color_and_simple_qips.circ_stats(img_hsv)'  , 
            References    = 'Datta et al., 2006; Geller et al., 2022; Iigaya et al., 2021; Li & Chen, 2009; Li et al., 2006; \
                            Mallon et al., 2014; Nakauchi et al., 2022; Peng, 2022; Schifanella, 2015; Thieleking et al., 2020', 
            Notes         = 'The Hue channel of the HSV colour space is a cicular value, so the normal arithmetic mean \
                            cannot be applied here. Therefore, the circular mean is calculated for the Hue channel. \
                            For all other channels, the normal arithmetic mean is used.' 
            )

build_entry(
            QIP           = 'Standard deviation of RGB, HSV, L*a*b* color channels' , 
            Image_preproc = 'Converting to respective color spaces (RGB, HSV, L*a*b*), no resizing', 
            CComplex      = 'low', 
            Range         = '',
            API           = 'AT.color_and_simple_qips.std_channels(img),  AT.color_and_simple_qips.circ_stats(img_hsv)'  , 
            References    = 'Datta et al., 2006; Li et al., 2006; Li & Chen, 2009; Mallon et al., 2014; Schifanella, 2015;    \
                            Thieleking et al., 2020;  Iigaya et al., 2021; Geller et al., 2022; Nakauchi et al., 2022; Peng, 2022', 
            Notes         = 'The Hue channel of the HSV colour space is a circular value, so the normal standard deviation \
                            cannot be applied here. Therefore, the circular standard deviation is calculated for the Hue channel. \
                            For all other channels, the normal standard deviation is used. Note that the standard deviation of \
                            the ligthness channel of L*a*b* color space is the RMS contrast.' 
            )

build_entry(
            QIP           = 'Balance, DCM, Homogeneity' , 
            Image_preproc = 'conversion to 8-bit grayscale image, no resizing', 
            CComplex      = 'medium', 
            Range         = 'All three QIPs are percentage values [0 - 100].',
            API           = 'AT.balance_qips.Balance(img_gray),  AT.balance_qips.DCM(img_gray), AT.balance_qips.Homogeneity(img_gray)'  , 
            References    = 'Hübner & Fillinger, 2016 ; Wagemans, 1995; McManus et al., 2011; Wilson and Chatterjee, 2005',
            Notes         = '' 
            )

build_entry(
            QIP           = 'Mirror symmetry' , 
            Image_preproc = 'Converting to binary image, no resizing', 
            CComplex      = 'low', 
            Range         = 'Percentage value [0 - 100].',
            API           = 'AT.balance_qips.Mirror_symmetry(img_gray)'  , 
            References    = 'Wagemans, 1995; Hübner & Fillinger, 2016', 
            Notes         = '' 
            )

build_entry(
            QIP           = 'CNN-feature-based QIPs: Symmetry, Self-similarity, Sparseness and Variability' , 
            Image_preproc = 'RGB image resized to 512*512 pixel', 
            CComplex      = 'high', 
            Range         = 'Empirically found values: Sparseness (0 - 0.0014) and Variability (0 - 0.0001)'  ,
            API           = 'AT.CNN_qips', 
            References    = 'Brachmann & Redies (2016); Brachmann & Redies 2017; Brachmann et al. (2017)', 
            Notes         = 'All CNN image properties are based on feature maps of the first layer of an Alex-Net (Krizhevsky et al., 2012) trained \
                            on Image Net from the Caffe module, which is no longer maintained. Weights of this Caffe module have been extracted \
                              and the folding and max-pooling operation has been reimplemented with Numpy to keep the  \
                              toolbox memory footprint small (no Tensorflow or Pytorch needed).'
            )

build_entry(
            QIP           = 'Fourier slope and Fourier sigma' , 
            Image_preproc = 'differs strongly between methods by Spehar, Mather and Redies, see notes below', 
            CComplex      = 'high', 
            Range         = 'empirical ranges: Redies [0 - 5), Spehar and Mather [0-2.5]  , theoretical ranges [0 - inf)'  ,
            API           = 'AT.fourier_qips', 
            References    = 'Graham & Field, 2007; Redies et al., 2007; Graham & Redies, 2010; Koch et al., 2010; Spehar & Taylor, 2013;  Mather, 2014; Isherwood et al., 2021', 
            Notes         = 'Detailed information on the differences between the three methods can be found in the publication. (Table 2)'
            )

build_entry(
            QIP           = '2d Fractal dimension' , 
            Image_preproc = 'Input 8-bit grayscale image. Converting to binary image and resizing to square image', 
            CComplex      = 'medium',
            Range         = '(1,2)',
            API           = 'AT.box_count_qips.box_count_2d(img_gray)', 
            References    = 'Mandelbrot, 1983; Taylor, 2002; Spehar et al., 2003; Spehar & Taylor, 2013; Viengkham & Spehar, 2018', 
            Notes         = ''
            )

build_entry(
            QIP           = '3d Fractal dimension' , 
            Image_preproc = 'Input 8-bit grayscale. Crop to the largest square that has a side length with a multiple of 2.', 
            CComplex      = 'high', 
            Range         = '(2,3)',
            API           = 'AT.box_count_qips.custom_differential_box_count(img_gray)', 
            References    = 'Mather, 2018', 
            Notes         = ''
            )

