import pytesseract
import numpy as np
import sys
from PIL import Image, ImageEnhance, ImageFilter, ExifTags
#https://ubuntu.flowconsult.at/linux/ocr-tesseract-text-recognition-ubuntu-14-04/
# https://pypi.python.org/pypi/pytesseract/0.1
#

def binarize_array(numpy_array, threshold):
    """Binarize a numpy array."""
    for i in range(len(numpy_array)):
        for j in range(len(numpy_array[0])):
            if numpy_array[i][j] > threshold:
                numpy_array[i][j] = 255
            else:
                numpy_array[i][j] = 0
    return numpy_array

im = Image.open("/home/nchinnappasu/learning/test/jj.jpg") # the second one
image = im.rotate(0, expand=True).convert('L')

enhancer = ImageEnhance.Contrast(image)
text = enhancer.enhance(1.0)
text.show()
te = pytesseract.image_to_string(text)
print te
sys.exit()
#gray = cv2.cvtColor(np.array(text), cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(np.array(text),0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# noise removal
kernel = np.ones((3,3),np.uint8)
opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
sure_bg = cv2.dilate(opening,kernel,iterations=3)
texttt = Image.fromarray(sure_bg).show()

te = pytesseract.image_to_string(texttt)
print te
sys.exit()
dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform,0.7*dist_transform.max(),255,0)
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg,sure_fg)
print unknown







exif=dict((ExifTags.TAGS[k], v) for k, v in im._getexif().items() if k in ExifTags.TAGS)




image = np.array(im.rotate(270, expand=True).convert('L'))
threshold =  np.mean(image)
threshold = np.round(threshold)
image = binarize_array(image, threshold=threshold)
img = Image.fromarray(image)

te = pytesseract.image_to_string(img)
print te



if exif['Orientation'] == 3:
    image = im.rotate(180, expand=True)
    image.show()
elif exif['Orientation'] == 6:
    image = im.rotate(270, expand=True).convert('L')
    #image.show()
elif exif['Orientation'] == 8:
    image = im.rotate(90, expand=True)
    image.show()

image = cv2.imread("/Users/mr.narendhrancs/Downloads/jj.jpg")
gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
ret, thresh = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

sys.exit()
image_grey = image.convert('LA')
image_grey.load()

# enhancer = ImageEnhance.Color(image)
# text = enhancer.enhance(50)
# enhancer_b = ImageEnhance.Contrast(text)
# text_b = enhancer.enhance(1)
# text_b.show()
image_grey.show()
te = pytesseract.image_to_string(image_grey)
print te
sys.exit()
enhancer = ImageEnhance.Contrast(image)
for i in range(16):
    factor = i / 4.0
    text = enhancer.enhance(factor)
    text.load()
    te = pytesseract.image_to_string(text)
    print te



enhancer = ImageEnhance.Sharpness(test_first)

for i in range(16):
    factor = i / 4.0
    text = enhancer.enhance(factor).show()
    text.load()
    te = pytesseract.image_to_string(text)
    print "**************"
    print "#######"
    print te


print "**************"
print "#######"


import sys
sys.exit()
enhancer = ImageEnhance.Sharpness(image)
enhanced = enhancer.enhance(3).show()
te = pytesseract.image_to_string(enhanced)
print "**************"
print "#######"
print te

import sys
sys.exit()
#im = im.filter(ImageFilter.MedianFilter())
#im = ImageEnhance.Sharpness(im)
#text = pytesseract.image_to_string(Image.open('/Users/mr.narendhrancs/jj.tiff'))
enhancer = ImageEnhance.Sharpness(im)

for i in range(16):
    factor = i / 4.0
    text = enhancer.enhance(8).show()
    #te = pytesseract.image_to_string(text)
    #print te
