from PIL import Image, ImageEnhance
import PIL
import cv2
img = Image.open("/Users/mr.narendhrancs/learning/test/jj.jpg")
img.save("/Users/mr.narendhrancs/learning/jj_test.jpg", dpi=(224,224))
#img = ImageEnhance.Sharpness(img)
#img = img.enhance(1)
#img = text.resize((200, 200), PIL.Image.ANTIALIAS)
#Histogram Equalization
exit()
img = cv2.imread("/Users/mr.narendhrancs/learning/test/jj.jpg", cv2.IMREAD_COLOR)
img[:, :, 0] = cv2.equalizeHist(img[:, :, 0])
img[:, :, 1] = cv2.equalizeHist(img[:, :, 1])
img[:, :, 2] = cv2.equalizeHist(img[:, :, 2])

#Image Resizing
img = cv2.resize(img, (227, 227), interpolation = cv2.INTER_CUBIC)



cv2.imwrite("/Users/mr.narendhrancs/learning/jj_test.jpg", img)#optimize=True, quality=10000)