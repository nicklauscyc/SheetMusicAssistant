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
    # for each page, say og file is Goldenrod_Full.pdf
    # output will be Goldenrod_Full-0.png, Goldenrod_Full-1.png
##    
##    img = Image(filename=filePath, resolution=400)
##    allPages = img.sequence
##
##    # just convert the whole file as 1 page for now
##    img.format = 'png'
##    img.background_color = Color('white')
##    img.alpha_channel = 'remove'
##
##    # image resolution scale adjustment for display
##    img.resample(x_res=xResScale, y_res=yResScale)
##
##    # saving
##    img.save(filename=filePath[:-4]+'.png')
##
##    # returns number of pages converted
##    return len(img.sequence)

    img = Image(filename=filePath, resolution=400)

    if len(img.sequence) == 1:

        # whole file as 1 page for now
        img.format = 'png'
        img.background_color = Color('white')
        img.alpha_channel = 'remove'

        # image resolution scale adjustment for display
        img.resample(x_res=xResScale, y_res=yResScale)

        # saving
        img.save(filename=filePath[:-4]+'.png')

    else: # multipage image
        
        for i in range(len(img.sequence)):
            indiv = Image(image=img.sequence[i], resolution=400)
            indiv.format = 'png'
            indiv.background_color = Color('white')
            indiv.alpha_channel = 'remove'

            # adjust resolution for display
            indiv.resample(x_res=xResScale, y_res=yResScale)

            # save it
            indiv.save(filename=filePath[:-4]+'-'+str(i)+'.png')


    # returns number of pages converted
    return len(img.sequence)
        
# toPNG('MusicScores/Sample1.pdf')

def toGIF(filePath, xResScale=220, yResScale=220):
    # converts a pdf to PNG
    # beware when converting to multiple pages, it might become an
    # animated GIF
    
    img = Image(filename=filePath, resolution=400)

    if len(img.sequence) == 1:

        # whole file as 1 page for now
        img.format = 'gif'
        img.background_color = Color('white')
        img.alpha_channel = 'remove'

        # image resolution scale adjustment for display
        img.resample(x_res=xResScale, y_res=yResScale)

        # saving
        img.save(filename=filePath[:-4]+'.gif')

    else: # multipage image
        
        for i in range(len(img.sequence)):
            indiv = Image(image=img.sequence[i], resolution=400)
            indiv.format = 'gif'
            indiv.background_color = Color('white')
            indiv.alpha_channel = 'remove'

            # adjust resolution for display
            indiv.resample(x_res=xResScale, y_res=yResScale)

            # save it
            indiv.save(filename=filePath[:-4]+'-'+str(i)+'.gif')


    # returns number of pages converted
    return len(img.sequence)
    
# toGIF('MusicScores/Sample1.pdf')

#toGIF('MusicScores/BasicScore.pdf')
toGIF('MusicScores/Goldenrod_Full.pdf')
toPNG('MusicScores/Goldenrod_Full.pdf')
