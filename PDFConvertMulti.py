# Converts PDF to either PNG or GIF

# ImageMagick6 requires one to change policy.xml file's line on PDF
# permissions in order to convert from PDF files
# /etc/ImageMagick-6

# currently only converts 1 page, probably needs image.sequence to convert
# multiple pages

from wand.image import Image
from wand.color import Color

def toPNG(filePath, xResScale=220, yResScale=220):
    # converts a pdf to GIF
    
    img = Image(filename=filePath, resolution=400)
    allPages = img.sequence

    # just convert the whole file as 1 page for now
    img.format = 'png'
    img.background_color = Color('white')
    img.alpha_channel = 'remove'

    # image resolution scale adjustment for display
    img.resample(x_res=xResScale, y_res=yResScale)

    # saving
    img.save(filename=filePath[:-4]+'.png')
        
# toPNG('MusicScores/Sample1.pdf')

def toGIF(filePath, xResScale=220, yResScale=220):
    # converts a pdf to PNG
    # beware when converting to multiple pages, it might become an
    # animated GIF
    
    img = Image(filename=filePath, resolution=400)
    allPages = img.sequence

    # just convert the whole file as 1 page for now
    img.format = 'gif'
    img.background_color = Color('white')
    img.alpha_channel = 'remove'

    # image resolution scale adjustment for display
    img.resample(x_res=xResScale, y_res=yResScale)

    # saving
    img.save(filename=filePath[:-4]+'.gif')
    
# toGIF('MusicScores/Sample1.pdf')



