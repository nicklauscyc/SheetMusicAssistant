import urllib.request
import base64
import math
from tkinter import PhotoImage

def downloadImage(image_path):
    import os, ssl
    if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
        getattr(ssl, '_create_unverified_context', None)):
        ssl._create_default_https_context = ssl._create_unverified_context

    pic = urllib.request.urlopen(image_path)
    raw_data = pic.read()

    return base64.b64encode(raw_data)

def PhotoImageFromLink(link, width=None, height=None, scale=None):
    base64_data = downloadImage(link)
    image = PhotoImage(data=base64_data)
    (old_w, old_h) = (image.width(), image.height())

    if scale != None:
        width = int(old_w * scale)
        height = int(old_h * scale)

    (target_w, target_h) = (width, height)

    if (target_w != None and target_h != None):
        x_common = math.gcd(target_w, old_w)
        x_zoom = int(target_w / x_common)
        x_sub = int(old_w / x_common)

        y_common = math.gcd(target_h, old_h)
        y_zoom = int(target_h / y_common)
        y_sub = int(old_h / y_common)

        image = image.zoom(x_zoom, y_zoom)
        image = image.subsample(x_sub, y_sub)

    return image
