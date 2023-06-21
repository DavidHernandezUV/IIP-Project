from pyrobex.robex import robex
import nibabel as nib

def skull_stripped(image):
    stripped, mask = robex(image)
    stripped_data = stripped.get_fdata()
    
    return stripped_data