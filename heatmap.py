# Copyright (c) 2023 Mikias Negussie
#
# MIT License
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

#This script plots a heatmap from normalized volume segments 
#We recommend using the warp function provided in this package to normalize segmentations
#Developed for the LesionMap-UCSF python package developed by the Hervey-Jumper group at UCSF Neurosurgery

# Import necessary packages
import os
import ants
import matplotlib.pyplot as plt
import matplotlib.colors as colors
import numpy as np

# Set the directory containing the normalized segmentations
seg_dir = "/path/to/normalized/segmentations"

# Set the MNI template image
template_image = ants.image_read("/path/to/MNI_template/MNI152_T1_1mm.nii.gz")

# Set the output directory for the lesion maps
output_dir = "/path/to/output/directory"

# Set the slice indices for the axial slices
axial_slice_indices = [55, 65, 75, 80, 85, 90, 95, 105, 115, 125]
# Set the slice indicies for coronal slices
coronal_slice_indices = [170, 185]
# Set the colormap to use for the lesion maps
cmap = "hot"

# Create a list of the normalized segmentations
seg_list = []
for seg_filename in os.listdir(seg_dir):
  seg_list.append(ants.image_read(os.path.join(seg_dir, seg_filename)))

#create the lesion map by summing the pixel values of the normalized segmentations
lesion_map = seg_list[0]
for i in range(1, len(seg_list)):
  lesion_map += seg_list[i]

# Loop through the axial slice indices
for axial_slice in axial_slice_indices:
  # Extract the axial slice from the template image
  template_slice = template_image[:,:,axial_slice]
  
  # Extract the axial slice from the lesion map
  lesion_slice = lesion_map[:,:,axial_slice]
  
  # Rotate the slices 90 degrees counterclockwise
  template_slice = np.rot90(template_slice)
  lesion_slice = np.rot90(lesion_slice)
  
  # Set the colormap normalization
  cnorm = colors.Normalize(vmin=0, vmax=len(seg_list))
  
  # Create the plot
  fig, ax = plt.subplots()
  im = ax.imshow(template_slice, cmap="gray")
  im2 = ax.imshow(lesion_slice, cmap=cmap, alpha=0.6, norm=cnorm)
 # plt.colorbar(im2) #only one color bar is needed
  
  # Save the plot
  plt.axis('off')
  plt.savefig(os.path.join(output_dir, "axial_slice_{}.png".format(axial_slice)))
  plt.close()
  
#loop through the coronal slice indices
for coronal_slice in coronal_slice_indices:
  # Extract the coronal slice from the template image
  template_slice = template_image[:,coronal_slice,:]
  
  # Extract the coronal slice from the lesion map
  lesion_slice = lesion_map[:,coronal_slice,:]
  
  # Set the colormap normalization
  cnorm = colors.Normalize(vmin=0, vmax=len(seg_list))
  
  # Create the plot
  fig, ax = plt.subplots()
  im = ax.imshow(template_slice, cmap="gray")
  im2 = ax.imshow(lesion_slice, cmap=cmap, alpha=0.5, norm=cnorm)
  plt.colorbar(im2)
  
  # Save the plot
  plt.savefig(os.path.join(output_dir, "coronal_slice_{}.png".format(coronal_slice)))
  plt.close()
