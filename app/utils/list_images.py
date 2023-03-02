import os
from config import Configuration

conf = Configuration()
    
def list_images():
    """Returns the list of available images."""
    img_names = filter(lambda x: x.endswith('.JPEG') and not x.startswith('UPL_') and not x.startswith('IE_'),
                       os.listdir(conf.image_folder_path))
    return list(img_names)
