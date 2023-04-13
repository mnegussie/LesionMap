# LesionMap
LesionMapUCSF is a comprehensive package for normalization and visualization of volumetric imaging segments. Users can perform segmentation, normalization, and visualization of large datasets with very few lines of code. 

## **Install**

`pip install LesionMap`

## **Usage**

`config.py`
`preprocess.py`
`preprocess_2d_images.py`
`predict.py` 

scripts are part of the DeepSeg toolkit to automatically segment scans. If you are manually segmenting scans, you can skip these steps.

`python3 warp.py` normalizes segments to common MNI brain space 
MNI template can be downloaded here: https://neuroconductor.org/help/MNITemplate/

`python3 heatmap.py` #makes a 3D matrix of masks and maps them onto a common average brain
