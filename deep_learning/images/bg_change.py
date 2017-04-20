import cv2
from PIL import Image, ImageEnhance, ImageFilter

im = Image.open("/Users/mr.narendhrancs/retrain_shoes/LA212A097-O11/LA212A097-O11@1.jpg")
scale = 4
maxsize = (762*scale, 1100*scale)
a = im.resize(maxsize, Image.ANTIALIAS)
quality_val = 90
a.save('test.jpg', 'JPEG', quality=quality_val)