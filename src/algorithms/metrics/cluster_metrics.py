import numpy as np
def calculate_cluster_volume(segmentation):

  image_header = segmentation.header
  pix_dim = image_header['pixdim']
  pixel_size = np.prod(pix_dim[1:4])

  image_data = segmentation.get_fdata()
  unique_labels = np.unique(image_data)

  cluster_volumes = {}

  for label in unique_labels:
    if label == 0:
        continue

    cluster_mask = (image_data == label)
    cluster_pixels = np.sum(cluster_mask)
    cluster_volume = cluster_pixels * pixel_size

    cluster_volumes[label] = cluster_volume


  return cluster_volumes