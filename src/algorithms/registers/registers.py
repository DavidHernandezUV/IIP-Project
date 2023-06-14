
import ants

def registration(flair,t1,type):

    registration = ants.registration(fixed=ants.from_numpy(flair), moving=ants.from_numpy(t1), type_of_transform=type)
    registered_image = registration['warpedmovout']
    return registered_image