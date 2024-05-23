import streamlit as st

def show_docs():

    st.markdown('<p class="head">Aesthetics Toolbox</p>', unsafe_allow_html=True)
    st.markdown('<p class="font0">Documentation</p>', unsafe_allow_html=True)

    st.markdown('<p class="font2">Contrast and Luminance Entropy</p>', unsafe_allow_html=True)
    
    st.write(""" Contrast is a widely studied feature in aesthetic research and there
    are many different methods to calculate it. It is unclear to what extent these different methods capture the
    same visually perceivable image property (Schifanella et al., 2015; Tong et al., 2005; Li and Chen, 2009;
    Luo and Tang, 2008). In the present work, Contrast is defined as the root mean square (rms) contrast (Peli,
    1990), which is the standard deviation of the L channel of the CIELAB color space. We also calculate the
    Shannon entropy (Shannon, 1948) of the L channel of the CIELAB color space. Since different entropy
    measures are calculated in the present work, we refer to this entropy measure as Luminance Entropy. In
    other publications (Sidhu et al., 2018; Mather, 2018; Iigaya et al., 2021), it is often referred to simply as
    entropy or Shannon entropy.""")
    
        
    
    st.markdown('<p class="font2">Edge-Orientation Entropy</p>', unsafe_allow_html=True)
    
    st.write("""
    Second-Order Edge-Orientation Entropy is used to measure how
    independently (randomly) edge orientations are distributed across an image (Redies et al., 2017). To
    obtain this measure, the orientation of each edge element is related to the orientation of all other edge
    elements in the same image by pairwise comparison. An image whose edges all have the same orientation
    and are distributed over the image at regular intervals would have a very low Edge-Orientation Entropy.
    An image with edge elements that have a random orientations and are randomly distributed over the image
    would have maximal Edge-Orientation Entropy. In this case, the orientations of the edge elements would
    be maximally independent of each other across the image.""")
    
    
    
    st.markdown('<p class="font2">PHOG Measures (Self-Similarity, Complexity and Anisotropy)</p>', unsafe_allow_html=True)
    st.write("""
    Self-Similarity, Complexity and
    Anisotropy measures are assessed using the (Pyramid of) Histograms of Orientation Gradients ([P]HOG)
    method, which was originally developed for object recognition and image categorization (Bosch et al.,
    2007). For details on the computation of Self-Similarity, Complexity, and Anisotropy, see the appendix in
    Braun et al. (2013). In brief, Self-Similarity captures how similar the histograms of gradient orientations
    are in a pyramid of subregions of an image compared to the histogram of the entire image or other
    subregions. High values for Self-Similarity indicate that the subregions are more similar to the entire
    image. Anisotropy measures how different the strengths of the gradients are across orientations in an
    image. Lower anisotropy indicates that the strength of the oriented gradients is more uniform across
    orientations. Higher anisotropy means that oriented gradient strength differs more strongly. Complexity
    is calculated as the mean gradient strength throughout an image. Higher complexity indicates a stronger
    mean gradient.""")
    
    
    
    st.markdown('<p class="font2">Fourier Slope and Fourier Sigma</p>', unsafe_allow_html=True)
    st.write("""
    Fourier Slope and Fourier Sigma are based on the Fourier power
    spectrum of the gray-scale version of an image. Roughly speaking, the Fourier Slope indicates the relative
    strength of high spatial frequencies versus low spatial frequencies. The Fourier Sigma indicates how
    linearly the log-log plot of the Fourier spectrum decreases with increasing spatial frequency. Higher values
    for Fourier Sigma correspond to larger deviations from a linear course. For a more detailed description of
    these SIPs, see Redies et al. (2008).""")
    
    
    
    st.markdown('<p class="font2">Symmetry-lr and Symmetry-ud</p>', unsafe_allow_html=True)
    st.write("""
    Brachmann and Redies (2016) developed a symmetry measure that is
    based on the first layer of CNN filters from a pre-trained AlexNet (Hinton et al., 2012). Since these filters
    capture both color-opponent features, luminance edges, and texture information, the symmetry measures
    computed from these filters more closely match the human perception of symmetry than earlier measures
    based on the symmetry of gray-scale pixels. For the present work, left/right symmetry (Symmetry-lr)
    and up/down symmetry (Symmetry-ud) were calculated with this method. For a broader overview of the
    importance and previous results on symmetry in aesthetics research, see Bertamini and Rampone (2020).""")
    
    
    st.markdown('<p class="font2">Sparseness and Variability</p>', unsafe_allow_html=True)
    st.write("""
    Brachmann et al. (2017) used the first
    convolutional layer of a pre-trained AlexNet to also measure Sparseness/Richness and Variability of the
    feature responses. A max-pooling operation was applied to each map of the filter responses of the 96
    filters in the first CNN layer. Sparseness is calculated as the median of the variances of each max-pooling
    map. Variability is the variance over all entries of all max-pooling maps. Note that in the original paper
    by Brachmann et al. (2017), Sparseness of SIPs was referred to as the inverse of Richness. In the present
    work, we decided to use the term Sparseness because the calculated variance relates directly to it (and
    not to its inverse value). For a visualization of Sparseness, see the boxplots in Figure 2 for the JA dataset
    (traditional oil paintings; low Sparseness) compared to the ArtPics dataset (style-transferred objects on
    large white background; high Sparseness).""")
    
