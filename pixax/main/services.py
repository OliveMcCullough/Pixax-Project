from django import forms
from PIL import Image
import os

from pixax.settings import MEDIA_ROOT


def remove_exif(image_file_with_exif, base_file_name, path_in_media):
    image = Image.open(image_file_with_exif.file)
    data = list(image.getdata())
    final_file = os.path.join(path_in_media,base_file_name + "." + image.format)
    image_without_exif = Image.new(image.mode, image.size)
    image_without_exif.putdata(data)
    image_path = os.path.join(MEDIA_ROOT, final_file)
    image_without_exif.save(image_path)
    return final_file


class CustomCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    template_name = "custom_widgets/custom_checkbox_select.html"
    input_type = 'checkbox'