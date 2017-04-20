from __future__ import division
from PIL import Image
import math
import os

def long_slice(image_path, out_name, outdir, slice_size=145):
    """slice an image into parts slice_size tall"""
    img = Image.open(image_path)
    width, height = img.size
    upper = 0
    left = 25
    slices = int(math.ceil(width/slice_size))

    count = 1
    for slice in range(slices):
        #if we are at the end, set the lower bound to be the bottom of the image
        if count == slices:
            lower = width
        else:
            lower = int(count * slice_size)
        #set the bounding box! The important bit

        bbox = (left, upper, lower, height)
        print bbox
        working_slice = img.crop(bbox)
        left += slice_size
        if left == 25:
            left= left-25
        #save the slice
        working_slice.save(os.path.join(outdir, "slice_" + out_name + "_" + str(count)+".png"))
        count +=1

if __name__ == '__main__':
    #slice_size is the max width of the slices in pixels
    long_slice("/Users/mr.narendhrancs/learning/test/LA212B08O-Q11_1_black_bg_largeHdUrl.jpg",
               "LA212B08O-Q11_1_black_bg_largeHdUrl.jpg","/Users/mr.narendhrancs/learning/test/")