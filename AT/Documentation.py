import streamlit as st
from PIL import Image


def build_entry(QIP , Image_preproc, CComplex, API, References, Notes):
    
    Button = st.sidebar.checkbox(QIP , value=True)
    
    if Button:
    
        st.divider()
        st.write('')  
        
        st.markdown('<p class="font2"> ' + QIP + ' </p>', unsafe_allow_html=True)
        
        col1, col2 = st.columns( [0.2, 0.8])
        with col1:
            st.markdown('<p class="font1"> Image preprocessing: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> Computational complexity: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> API: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> References: </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> Notes: </p>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<p class="font1"> ' + Image_preproc + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + CComplex      + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + API           + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + References    + '  </p>', unsafe_allow_html=True)
            st.markdown('<p class="font1"> ' + Notes         + '  </p>', unsafe_allow_html=True)


def show_docs():
       
    image1 = Image.open('images/LogoDesign EAJ final.png')
    image2 = Image.open('images/GestatltReVision_Logo_mod.png')
    
    #Create two columns with different width
    col1, col2, col3 = st.columns( [0.15, 0.5, 0.25])
    with col2:               # To display the header text using css style
        st.markdown('<p class="head">Aesthetics Toolbox</p>', unsafe_allow_html=True)
        st.markdown('<p class="subhead">Documentation</p>', unsafe_allow_html=True)
        st.markdown('<p class="font1">This is the documentation for the QIP machine. Detailed information on the individual QIPs can be found in the corresponding publication TBA. \
                    This includes: the motivation for using each QIP from a scientific point of view, other related publications, \
                    and the description of the algorithm itself.</p>', unsafe_allow_html=True)
    with col1:
        st.image(image1,  width=160) 
    with col3:
        st.image(image2,  width=400) 
    
    
    # st.markdown('<p class="head">Aesthetics Toolbox</p>', unsafe_allow_html=True)
    # st.markdown('<p class="subhead">Documentation</p>', unsafe_allow_html=True)
    
    
    # st.write('<p class="font1"> Detailed information on the individual QIPs can be found in the corresponding publication TBA. \
    #             This includes: the motivation for using each QIP from a scientific point of view, other related publications, \
    #             and the description of the algorithm itself. </p>' , unsafe_allow_html=True )
    
    

    build_entry(
                QIP           = 'Image size' , 
                Image_preproc = 'RGB image, no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.image_size(img_RGB)', 
                References    = 'Datta et al., 2006', 
                Notes         = 'Image size = image_width + image_height in pixel'
                )

    build_entry(
                QIP           = 'Aspect Ratio' , 
                Image_preproc = 'RGB image, no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.aspect_ratio(img_RGB)', 
                References    = 'Datta et al., 2006;  Li et al., 2006; Iigaya et al., 2021', 
                Notes         = 'Aspect ratio = image_width / image_height'
                )

    build_entry(
                QIP           = 'RMS contrast' , 
                Image_preproc = 'Converting to L*a*b* color space, no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.std_channels(img_LAB)', 
                References    = 'Peli, 1990; Tong et al., 2004 ; Luo & Tang, 2008; Li & Chen, 2009; Schifanella, 2015', 
                Notes         = 'RMS contrast = standard deviation of the Lightness channel (L*a*b*)'
                )
    
    
    
    build_entry(
                QIP           = 'Ligthness entropy' , 
                Image_preproc = 'Converting to L*a*b* color space, no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.shannonentropy_channels(img_LAB)', 
                References    = 'Shannon, 1948; Kersten, 1987; Mather, 2018', 
                Notes         = 'RMS Contrast = shannon entropy of the Lightness channel (L*a*b*)'
                )
    
    
    
    build_entry(
                QIP           = 'PHOG: Anisotropy, Complexity, PHOG-Selfsimilarity' , 
                Image_preproc = 'Converting to Matlab L*a*b* color space, optional resizing to number of pixel possible (-1 = no resizing)', 
                CComplex      = 'high', 
                API           = 'AT.PHOG_qips.PHOGfromImage(img_rgb, section, bins, angle, levels, re, sesfweight )', 
                References    = 'Braun et al., 2013; Redies & Gross, 2013', 
                Notes         = 'By default, image resizing is disabled (parameter is set to -1). The resize function of the original \
                                Matlab script is different from the available Python implementations. Calculating PHOG QIPs with resizing will \
                                give different results than the original Matlab script. Without resizing, the results are the same.'
                )
    
      
    
    build_entry(
                QIP           = 'Edge density, 1st-order and 2nd-order Edge orientation entropy' , 
                Image_preproc = 'Converting to 8-bit grayscale image, resizing to 120.000 pixel while maintaining aspect ratio', 
                CComplex      = 'very high', 
                API           = 'AT.edge_entropy_qips.do_first_and_second_order_entropy_and_edge_density (img_gray)', 
                References    = 'Redies et al., 2017', 
                Notes         = 'Compares the orientation and strength of the 10,000 strongest edge pixels in pairs, \
                                which is computationally intensive. A fast C++ implementaion of this QIP can be found in the following \
                                github repository: https://github.com/RBartho/C-version-2nd-Order-Edge-Orientation-Entropy'
                )


    
    build_entry(
                QIP           = 'Color entropy' , 
                Image_preproc = 'Converting to HSV color space, no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.shannonentropy_channels(img_HSV)', 
                References    = 'Geller et al., 2022', 
                Notes         = 'TBA'
                )


    build_entry(
                QIP           = 'Mean value of RGB, HSV, L*a*b* color channels' , 
                Image_preproc = 'Converting to respective color spaces (RGB, HSV, L*a*b*), no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.mean_channels(img)  and  AT.color_and_simple_qips.circ_stats(img_hsv)'  , 
                References    = 'Datta et al., 2006; Geller et al., 2022; Iigaya et al., 2021; Li & Chen, 2009; Li et al., 2006; \
                                Mallon et al., 2014; Nakauchi et al., 2022; Peng, 2022; Schifanella, 2015; Thieleking et al., 2020', 
                Notes         = 'The Hue channel of the HSV colour space is a cyclic value, so the normal arithmetic mean \
                                cannot be applied here. Therefore, the circular mean is calculated for the Hue channel. \
                                For all other channels, the normal arithmetic mean is used.' 
                )


    build_entry(
                QIP           = 'Standard deviation of RGB, HSV, L*a*b* color channels' , 
                Image_preproc = 'Converting to respective color spaces (RGB, HSV, L*a*b*), no resizing', 
                CComplex      = 'low', 
                API           = 'AT.color_and_simple_qips.std_channels(img)  ,  AT.color_and_simple_qips.circ_stats(img_hsv)'  , 
                References    = 'Datta et al., 2006; Geller et al., 2022; Iigaya et al., 2021; Li & Chen, 2009; Li et al., 2006; \
                                Mallon et al., 2014; Nakauchi et al., 2022; Peng, 2022; Schifanella, 2015; Thieleking et al., 2020', 
                Notes         = 'The Hue channel of the HSV colour space is a cyclic value, so the normal standard deviation \
                                cannot be applied here. Therefore, the circular standard deviation is calculated for the Hue channel. \
                                For all other channels, the normal standard deviation is used. Note that the standard deviation of \
                                the ligthness channel of L*a*b* color space is the RMS contrast.' 
                )



    build_entry(
                QIP           = 'Balance, DCM, Homogeneity' , 
                Image_preproc = 'conversion to 8-bit grayscale image, no resizing', 
                CComplex      = 'medium', 
                API           = 'AT.balance_qips.APB_Score(img_gray)  ,  AT.balance_qips.DCM_Key(img_gray) , AT.balance_qips.entropy_score_2d(img_gray)'  , 
                References    = 'Hübner & Fillinger, 2016', 
                Notes         = 'TBA' 
                )

    build_entry(
                QIP           = 'Mirror symmetry' , 
                Image_preproc = 'Converting to binary image, no resizing', 
                CComplex      = 'low', 
                API           = 'AT.balance_qips.MS_Score(img_gray)'  , 
                References    = 'Hübner & Fillinger, 2016', 
                Notes         = 'TBA' 
                )


    build_entry(
                QIP           = 'CNN image properties: Sparseness and Variability, CNN-feature-based symmetrys, CNN self-symmetry' , 
                Image_preproc = 'RGB image resized to 512x512 pixel', 
                CComplex      = 'high', 
                API           = 'AT.CNN_qips', 
                References    = 'Brachmann and Redies (2016)', 
                Notes         = 'All CNN image properties are Based on feature maps of the first layer of an Alex-Net (Krizhevsky et al., 2012 trained \
                                on Image Net from the no longer maintained Caffe module. Weights of this Caffe module have been extracted \
                                  and the folding and max-pooling operation has been reimplemented with Numpy to keep the  \
                                  toolbox memory footprint small (no Tensorflow or Pytorch needed).'
                )
    
    build_entry(
                QIP           = 'Fourier Slope and Fourier Sigma' , 
                Image_preproc = 'differs strongly between Branka, Redies, Mather, see notes below', 
                CComplex      = 'high', 
                API           = 'AT.fourier_qips', 
                References    = 'Graham & Field, 2007; Redies et al., 2007; Graham & Redies, 2010; Koch et al., 2010; Spehar & Taylor, 2013;  Mather, 2014', 
                Notes         = 'TBA'
                )
    
    build_entry(
                QIP           = '2D Fractal dimension' , 
                Image_preproc = 'input 8-bit grayscale image, Converting to binary image and resizing to square image', 
                CComplex      = 'medium', 
                API           = 'AT.box_count_qips.box_count_2d(img_gray)', 
                References    = 'Mandelbrot, 1983; Taylor, 2002; Spehar et al., 2003; Spehar & Taylor, 2013; Viengkham & Spehar, 2018', 
                Notes         = 'TBA'
                )
    
    build_entry(
                QIP           = '3D Fractal dimension' , 
                Image_preproc = 'input 8-bit grayscale, cropp to largest square with power of two', 
                CComplex      = 'high', 
                API           = 'AT.box_count_qips.custom_differential_box_count(img_gray)', 
                References    = 'Mather, 2018', 
                Notes         = 'TBA'
                )
    
    
    

    # st.markdown('<p class="font2">Contrast and Luminance Entropy</p>', unsafe_allow_html=True)
    
    # st.write(""" Contrast is a widely studied feature in aesthetic research and there
    # are many different methods to calculate it. It is unclear to what extent these different methods capture the
    # same visually perceivable image property (Schifanella et al., 2015; Tong et al., 2005; Li and Chen, 2009;
    # Luo and Tang, 2008). In the present work, Contrast is defined as the root mean square (rms) contrast (Peli,
    # 1990), which is the standard deviation of the L channel of the CIELAB color space. We also calculate the
    # Shannon entropy (Shannon, 1948) of the L channel of the CIELAB color space. Since different entropy
    # measures are calculated in the present work, we refer to this entropy measure as Luminance Entropy. In
    # other publications (Sidhu et al., 2018; Mather, 2018; Iigaya et al., 2021), it is often referred to simply as
    # entropy or Shannon entropy.""")
    
        
    
    # st.markdown('<p class="font2">Edge-Orientation Entropy</p>', unsafe_allow_html=True)
    
    # st.write("""
    # Second-Order Edge-Orientation Entropy is used to measure how
    # independently (randomly) edge orientations are distributed across an image (Redies et al., 2017). To
    # obtain this measure, the orientation of each edge element is related to the orientation of all other edge
    # elements in the same image by pairwise comparison. An image whose edges all have the same orientation
    # and are distributed over the image at regular intervals would have a very low Edge-Orientation Entropy.
    # An image with edge elements that have a random orientations and are randomly distributed over the image
    # would have maximal Edge-Orientation Entropy. In this case, the orientations of the edge elements would
    # be maximally independent of each other across the image.""")
    
    
    
    # st.markdown('<p class="font2">PHOG Measures (Self-Similarity, Complexity and Anisotropy)</p>', unsafe_allow_html=True)
    # st.write("""
    # Self-Similarity, Complexity and
    # Anisotropy measures are assessed using the (Pyramid of) Histograms of Orientation Gradients ([P]HOG)
    # method, which was originally developed for object recognition and image categorization (Bosch et al.,
    # 2007). For details on the computation of Self-Similarity, Complexity, and Anisotropy, see the appendix in
    # Braun et al. (2013). In brief, Self-Similarity captures how similar the histograms of gradient orientations
    # are in a pyramid of subregions of an image compared to the histogram of the entire image or other
    # subregions. High values for Self-Similarity indicate that the subregions are more similar to the entire
    # image. Anisotropy measures how different the strengths of the gradients are across orientations in an
    # image. Lower anisotropy indicates that the strength of the oriented gradients is more uniform across
    # orientations. Higher anisotropy means that oriented gradient strength differs more strongly. Complexity
    # is calculated as the mean gradient strength throughout an image. Higher complexity indicates a stronger
    # mean gradient.""")
    
    
    
    # st.markdown('<p class="font2">Fourier Slope and Fourier Sigma</p>', unsafe_allow_html=True)
    # st.write("""
    # Fourier Slope and Fourier Sigma are based on the Fourier power
    # spectrum of the gray-scale version of an image. Roughly speaking, the Fourier Slope indicates the relative
    # strength of high spatial frequencies versus low spatial frequencies. The Fourier Sigma indicates how
    # linearly the log-log plot of the Fourier spectrum decreases with increasing spatial frequency. Higher values
    # for Fourier Sigma correspond to larger deviations from a linear course. For a more detailed description of
    # these QIPs, see Redies et al. (2008).""")
    
    
    
    # st.markdown('<p class="font2">Symmetry-lr and Symmetry-ud</p>', unsafe_allow_html=True)
    # st.write("""
    # Brachmann and Redies (2016) developed a symmetry measure that is
    # based on the first layer of CNN filters from a pre-trained AlexNet (Hinton et al., 2012). Since these filters
    # capture both color-opponent features, luminance edges, and texture information, the symmetry measures
    # computed from these filters more closely match the human perception of symmetry than earlier measures
    # based on the symmetry of gray-scale pixels. For the present work, left/right symmetry (Symmetry-lr)
    # and up/down symmetry (Symmetry-ud) were calculated with this method. For a broader overview of the
    # importance and previous results on symmetry in aesthetics research, see Bertamini and Rampone (2020).""")
    
    
    # st.markdown('<p class="font2">Sparseness and Variability</p>', unsafe_allow_html=True)
    # st.write("""
    # Brachmann et al. (2017) used the first
    # convolutional layer of a pre-trained AlexNet to also measure Sparseness/Richness and Variability of the
    # feature responses. A max-pooling operation was applied to each map of the filter responses of the 96
    # filters in the first CNN layer. Sparseness is calculated as the median of the variances of each max-pooling
    # map. Variability is the variance over all entries of all max-pooling maps. Note that in the original paper
    # by Brachmann et al. (2017), Sparseness of QIPs was referred to as the inverse of Richness. In the present
    # work, we decided to use the term Sparseness because the calculated variance relates directly to it (and
    # not to its inverse value). For a visualization of Sparseness, see the boxplots in Figure 2 for the JA dataset
    # (traditional oil paintings; low Sparseness) compared to the ArtPics dataset (style-transferred objects on
    # large white background; high Sparseness).""")
    