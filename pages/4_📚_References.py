import streamlit as st

st.set_page_config(layout="wide")

st.markdown(""" <style> .head {
font-size:35px ;  font-family: 'Cooper Black'; color: #FF9633;}
</style> """, unsafe_allow_html=True)

st.markdown('<p class="head">References</p>', unsafe_allow_html=True)

st.write(

"""
Bosch, A., Zisserman, A., & Munoz, X. (2007). Representing shape with a spatial pyramid kernel. Proceedings of the 6th ACM International Conference on Image and Video Retrieval, 401-408. https://doi.org/10.1145/1282280.1282340 

Brachmann, A., Barth, E., & Redies, C. (2017). Using CNN features to better understand what makes visual artworks special. Frontiers in Psychology, 8, 830. https://doi.org/10.3389/fpsyg.2017.00830 

Brachmann, A., & Redies, C. (2016). Using convolutional neural network filters to measure left-right mirror symmetry in images. Symmetry, 8, 144. https://doi.org/10.3390/sym8120144 

Brachmann, A., & Redies, C. (2017). Defining self-similarity of images using features learned by convolutional neural networks Electronic Imaging, Human Vision and Electronic Imaging 2017, Burlingame, CA. 

Burton, G. J., & Moorhead, I. R. (1987). Color and spatial structure in natural scenes. Applied Physics, 26, 157-170. 

Dalal, N., & Triggs, B. (2005). Histograms of oriented gradients for human detection. International Conference on Computer Vision & Pattern Recognition, 2, 886-893. https://doi.org/10.1109/CVPR.2005.177

Datta, R., Joshi, D., Li, J., & Wang, J. Z. (2006). Studying aesthetics in photographic images using a computational approach. Lecture Notes in Computer Science, 3953, 288-301. https://doi.org/10.1007/11744078_23 

Geller, H. A., Bartho, R., Thommes, K., & Redies, C. (2022). Statistical image properties predict aesthetic ratings in abstract paintings created by neural style transfer. Frontiers in Neuroscience, 16, 999720. https://doi.org/10.3389/fnins.2022.999720 

Graham, D. J., & Field, D. J. (2007). Statistical regularities of art images and natural scenes: spectra, sparseness and nonlinearities. Spatial Vision, 21(1-2), 149-164. https://doi.org/10.1163/156856807782753877 

Graham, D. J., & Field, D. J. (2008). Variations in intensity statistics for representational and abstract art, and for art from the Eastern and Western hemispheres. Perception, 37(9), 1341-1352. 

Hübner, R., & Fillinger, M. G. (2016). Comparison of objective measures for predicting perceptual balance and visual aesthetic preference. Frontiers in Psychology, 7, 335. https://doi.org/10.3389/fpsyg.2016.00335 

Iigaya, K., Yi, S., Wahle, I. A., Tanwisuth, K., & O'Doherty, J. P. (2021). Aesthetic preference for art can be predicted from a mixture of low- and high-level visual features. Nature Human Behaviour, 5(6), 743-755. https://doi.org/10.1038/s41562-021-01124-6 

Isherwood, Z. J., Schira, M. M., & Spehar, B. (2017). The tuning of human visual cortex to variations in the 1/f amplitude spectra and fractal properties of synthetic noise images. Neuroimage, 146, 642-657. https://doi.org/10.1016/j.neuroimage.2016.10.013 

Kersten, D. (1987). Predictability and redundancy of natural images. Journal of the Optical Society of America, Series A, 4(12), 2395-2400. http://www.ncbi.nlm.nih.gov/pubmed/3430226 

Koch, M., Denzler, J., & Redies, C. (2010). 1/f2 Characteristics and isotropy in the Fourier power spectra of visual art, cartoons, comics, mangas, and different categories of photographs. PLoS One, 5(8), e12268. https://doi.org/10.1371/journal.pone.0012268 

Krizhevsky, A., Sutskever, I., & Hinton, G. E. (2012). Imagenet classification with deep convolutional neural networks. Advances in Neural Information Processing Systems, 25, 1097-1105. 

Li, C., & Chen, T. (2009). Aesthetic visual quality assessment of paintings. IEEE Journal of Selected Topics in Signal Processing, 3(2), 236-252. 

Li, J., Datta, R., Joshi, D., & Wang, J. (2006). Studying aesthetics in photographic images using a computational approach. Lecture Notes in Computer Science, 3953, 288-301. 

Mallon, B., Redies, C., & Hayn-Leichsenring, G. U. (2014). Beauty in abstract paintings: Perceptual contrast and statistical properties. Frontiers in Human Neuroscience, 8, 161. https://doi.org/10.3389/fnhum.2014.00161 

Mandelbrot, B. (1983). The fractal geometry of nature. San Francisco: W. H. Freeman. 

Mather, G. (2014). Artistic adjustment of image spectral slope. Art & Perception, 2, 11-22. 

Mather, G. (2018). Visual image statistics in the history of Western art. Art & Perception, 6(2-3), 97-115. https://doi.org/10.1163/22134913-20181092 

McManus, I. C., Stöver, K., & Kim, D. (2011). Arnheim's Gestalt theory of visual balance: Examining the compositional structure of art photographs and abstract images. i-Perception, 2, 615-647. 

Nakauchi, S., Kondo, T., Kinzuka, Y., Taniyama, Y., Tamura, H., Higashi, H., Hine, K., Minami, T., Linhares, J. M. M., & Nascimento, S. M. C. (2022). Universality and superiority in preference for chromatic composition of art paintings. Scientific Reports, 12(1). https://doi.org/10.1038/s41598-022-08365-z 

Peng, Y. (2022). Athec: A Python library for computational aesthetic analysis of visual media in social science research. Computational Communication Research, 4.1, 323-349. https://doi.org/10.5117CCR2022.1.009.PENG 

Redies, C., Brachmann, A., & Wagemans, J. (2017). High entropy of edge orientations characterizes visual artworks from diverse cultural backgrounds. Vision Research, 133, 130-144. https://doi.org/10.1016/j.visres.2017.02.004 

Redies, C., & Gross, F. (2013). Frames as visual links between paintings and the museum environment: an analysis of statistical image properties. Frontiers in Psychology, 4, 831. https://doi.org/10.3389/fpsyg.2013.00831 

Redies, C., Hasenstein, J., & Denzler, J. (2007). Fractal-like image statistics in visual art: similarity to natural scenes. Spatial Vision, 21(1-2), 137-148. https://doi.org/10.1163/156856807782753921 

Schifanella, R., Redi, M., Aiello, L.M. (2015). An image is worth more than a thousand favorites: Surfacing the hidden beauty of flickr pictures. Proceedings of the International AAAI Conference on Web and Social Media, 9, 397-406. https://doi.org/10.1609/icwsm.v9i1.14612 

Shannon, C. E. (1948). A mathematical theory of communication. Bell System Technical Journal, 27(4), 623-656. https://doi.org/10.1002/j.1538-7305.1948.tb00917.x 

Spehar, B., Clifford, C. W. G., Newell, B. R., & Taylor, R. P. (2003). Universal aesthetic of fractals. Computers & Graphics, 27, 813-820. https://doi.org/10.1016/S0097-8493(03)00154-7 

Spehar, B., & Taylor, R. P. (2013). Fractals in art and nature: Why do we like them? S&T/SPIE Electronic Imaging, Burlingame, California, United States, 8651, 865118. https://doi.org/https://doi.org/10.1117/12.2012076

Taylor, R. P. (2002). Order in Pollock's chaos - Computer analysis is helping to explain the appeal of Jackson Pollock's paintings. Scientific American, 287(6), 116-121. https://doi.org/10.1038/scientificamerican1202-116 

Thieleking, R., Medawar, E., Disch, L., & Witte, A. V. (2020). Art. pics database: An open access database for art stimuli for experimental research. Frontiers in Psychology, 11, 3537. 

Viengkham, C., Isherwood, Z., & Spehar, B. (2022). Fractal‑scaling properties as aesthetic primitives in vision and touch. Axiomathes, 32, 869-888. 

Viengkham, C., & Spehar, B. (2018). Preference for fractal-scaling properties across synthetic noise images and artworks. Frontiers in Psychology, 9, 1439. https://doi.org/10.3389/fpsyg.2018.01439 

Wagemans, J. (1995). Detection of visual symmetries. Spatial Vision, 9(1), 9-32. https://doi.org/10.1163/156856895x00098

Wilson, A., & Chatterjee, A. (2005). The assessment of preference for balance: Introducing a new test. Empirical Studies of the Arts, 23, 165-180. 


"""
)

