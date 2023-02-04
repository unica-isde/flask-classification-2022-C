import os

from config import Configuration

conf = Configuration()

def remove_uploaded_images():
    """Removes all images that have been uploaded by the user."""
    img_names = filter(lambda x: x.startswith('UPL_'),
                       os.listdir(conf.image_folder_path))
    for img_name in img_names:
        os.remove(os.path.join(conf.image_folder_path, img_name))

def list_images():
    """Returns the list of available images."""
    remove_uploaded_images()
    img_names = filter(lambda x: x.endswith('.JPEG'),
                       os.listdir(conf.image_folder_path))
    return list(img_names)
