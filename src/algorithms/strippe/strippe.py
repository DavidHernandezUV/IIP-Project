from pyrobex.robex import robex
import nibabel as nib

def skull_stripped(image):
    image_data_flair = nib.load(image)
    stripped, mask = robex(image_data_flair)
    mask = stripped.get_fdata()
    
    return mask