from PIL import Image



#Import an image
image = Image.open("/Users/mr.narendhrancs/Downloads/LA212B08O-Q11@12.jpg")

image
im = image.convert('L')


from pylab import *

# create a new figure
figure()
gray()
# show contours with origin upper left corner
contour(im, origin='image')
axis('equal')
axis('off')


figure()


#hist(im_array.flatten(), 128)

show()