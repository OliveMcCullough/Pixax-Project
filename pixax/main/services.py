from django import forms
from PIL import Image, ExifTags
import os

from pixax.settings import MEDIA_ROOT


def remove_exif(image_file_with_exif, base_file_name, path_in_media):
    image = Image.open(image_file_with_exif.file)
    final_file = os.path.join(path_in_media,base_file_name + "." + image.format)
    image_without_exif = Image.new(image.mode, image.size)
    rotation, flip = determine_exif_image_rotation_and_flip(image)
    data = list(image.getdata())
    image_without_exif.putdata(data)
    image_path = os.path.join(MEDIA_ROOT, final_file)
    if rotation != 0:
        image_without_exif=image_without_exif.rotate(rotation, expand=True)
    if flip:
        image_without_exif=image_without_exif.transpose(Image.FLIP_LEFT_RIGHT)
    image_without_exif.save(image_path)
    return final_file


def determine_exif_image_rotation_and_flip(image):
    """Get the code for the tag that has orientation"""
    for orientation_id in ExifTags.TAGS.keys():
        if ExifTags.TAGS[orientation_id]=="Orientation": 
            break

    """Get exif dataset for the image"""
    exif = dict(image._getexif().items())

    """Check orientation data is present before proceeding"""
    if orientation_id in exif:
        orientation_exif = exif[orientation_id]
    else:
        orientation_exif = 0

    return determine_exif_rotation(orientation_exif), determine_exif_flip(orientation_exif)


def determine_exif_rotation(orientation_exif):
    if orientation_exif is 6 or orientation_exif is 5: return -90
    if orientation_exif is 8 or orientation_exif is 7: return 90
    if orientation_exif is 3 or orientation_exif is 4: return 180
    return 0

def determine_exif_flip(orientation_exif):
    if orientation_exif is 2 or orientation_exif is 7 or orientation_exif is 5 or orientation_exif is 4:
        return True

class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "custom_widgets/custom_checkbox_select.html"
    input_type = 'checkbox'