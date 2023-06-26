
import ants

def registration(flair,t1,type):
    flair_ant_image = ants.image_read(flair)
    t1_ant_image = ants.image_read(t1)
    
    registration = ants.registration(fixed=flair_ant_image, moving=t1_ant_image, type_of_transform=type)
    registered_image = registration['warpedmovout']
    registered_image = ants.apply_transforms(fixed=flair_ant_image, moving=t1_ant_image, transformlist=registration['fwdtransforms'])
    return registered_image