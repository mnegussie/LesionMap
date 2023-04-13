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

#This script defines a python function that warps tumor segmentation to common MNI brain space
#Developed for the LesionMap-UCSF python package developed by the Hervey-Jumper group at UCSF Neurosurgery

def warp(template_image, seg_dir, ref_dir):
# template_image should be a scan from the MNI template which can be found here: https://neuroconductor.org/help/MNITemplate/ 
# seg_dir is a path to your tumor segmentations (all in nifti format) 
# ref_dir is a path to your reference images - original patient scans (all in nifti format)
#
#
# create a list of the segmentations and their filenames
seg_list = []
seg_filename_list = []
for seg_filename in os.listdir(seg_dir):
  seg_list.append(ants.image_read(os.path.join(seg_dir, seg_filename)))
  seg_filename_list.append(seg_filename)

# Loop through the segmentations and filenames
for i in range(len(seg_list)):
  # Get the current segmentation and filename
  seg = seg_list[i]
  seg_filename = seg_filename_list[i]
  
  # Get the corresponding reference image filename
  ref_filename = seg_filename.split("_")[0] + "_T1.nii.gz"
  ref_image = ants.image_read(os.path.join(ref_dir, ref_filename))
  
  # Create an affine transformation using the SyN algorithm
  tx = ants.registration(template_image, ref_image, "SyN")
  
  # Warp the segmentation to the MNI space using the affine transformation
  seg_warped = ants.apply_transforms(template_image, seg, tx["fwdtransforms"], interpolator="nearestNeighbor")
  
  # Save the normalized segmentation
  ants.image_write(seg_warped, os.path.join(seg_dir, "normalized_" + seg_filename))

