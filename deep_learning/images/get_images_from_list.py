import csv
import os
from os.path import expanduser
import requests
import json
import wget
import time
from Queue import Queue
from threading import Thread
import numpy as np
import cv2
from PIL import Image, ImageEnhance, ImageFilter
import sys
import skimage

accept_languages = ['de-DE', 'da-DK', 'de-AT', 'de-CH', 'en-GB', 'es-ES', 'fi-FI',
                         'nl-BE', 'fr-FR', 'it-IT', 'nl-NL', 'no-NO', 'pl-PL', 'sv-SE']
DATA = []

class DataNotFound(Exception):
    pass

def get_webapi_brand_image_link_per_country_lang(csku, lang=None, directory=None):
    """ Accesses the Zalando Website API and pulls information for article brand, as well as a link
            for an article picture.
            :param csku: The csku name to pull data for
            :param lang: The country to access
            :type csku: str
            :type lang: str-str
            :return: The url of the csku picture, and the brand name of the csku
            :rtype: dictionary_object
            """
    try:
        web_request = \
            'https://api.zalando.com/articles/{c}?fields=media.images.largeHdUrl'.format(c=csku)
        webapi_brand_image_url = requests.get(web_request, headers={'x-client-name': 'Team AIS Preorder PQRS API'})
        result = json.loads(webapi_brand_image_url.text)

        # In case of 404 http error or any http error.
        # the result will be assigned here with the error message.
        # Then the default values are returned.
        if 'status' in result.keys():
            raise DataNotFound

        elif result is not None:
            # Get the brand


            if 'media' in result.keys() and 'images' in result['media'].keys():
                for x in result['media']['images']:
                    if 'largeHdUrl' in x.keys():
                        pic_url = x['largeHdUrl']
                        wget.download(pic_url, out=directory)


    except DataNotFound:
        pass


def read(filename):
    """reads csku_names for testing locally

    :param filename: full path with name
    :type filename: str
    :return: list cskus from the file
    :rtype: list of strings
    """
    with open(filename, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for csku in reader:
            currentWorkingPath = expanduser("~/hackweek")
            currentWorkingPath += "/zalando/{csku}".format(csku=csku[1])
            if not os.path.isdir(currentWorkingPath):
                os.mkdir(currentWorkingPath)
            get_webapi_brand_image_link_per_country_lang(csku[0], directory=currentWorkingPath)
           # for lang in accept_languages:

def read_download(filename):
    """reads csku_names for testing locally

    :param filename: full path with name
    :type filename: str
    :return: list cskus from the file
    :rtype: list of strings
    """
    with open(filename, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=' ', quotechar='|')

        print time.time()

        myQueue = Queue()
        num_fetch_threads = 50

        for i in range(num_fetch_threads):
            worker = Thread(target=noisy, args=(myQueue,))
            worker.setDaemon(True)
            worker.start()

        for csku in reader:
            myQueue.put(csku)

        print 'Working with %s threads' % num_fetch_threads

        myQueue.join()


def save_images(c):
    while True:
        try:
            csku = c.get()
            currentWorkingPath = expanduser("~/hackweek")
            currentWorkingPath += "/zalando/{csku}".format(csku=csku[1])
            if not os.path.isdir(currentWorkingPath):
                os.mkdir(currentWorkingPath)
            wget.download(csku[0], out=currentWorkingPath)
            c.task_done()
        except Exception, e:
            print e
            pass
            c.task_done()


def images(c):
    while True:
        try:
            csku = c.get()
            im = Image.open(csku[0])
            enhancer = ImageEnhance.Brightness(im)
            text_b = enhancer.enhance(0.8)
            c_enhancer = ImageEnhance.Contrast(text_b)
            text_c = c_enhancer.enhance(0.7)
            s_enhancer = ImageEnhance.Sharpness(text_c)
            text_s = s_enhancer.enhance(0.0)
            co_enhancer = ImageEnhance.Color(text_s)
            text_co = co_enhancer.enhance(1.0)
            save_path = os.path.splitext(csku[0])[0] + '_bad_quality.jpg'
            text_co.save(save_path)
            c.task_done()
        except Exception, e:
            print e
            pass
            c.task_done()


def bg_change(cskus_from_queue):
    while True:
        try:
            csku = cskus_from_queue.get()
            # == Parameters =======================================================================
            BLUR = 21
            CANNY_THRESH_1 = 10
            CANNY_THRESH_2 = 10
            MASK_DILATE_ITER = 20
            MASK_ERODE_ITER = 10
            MASK_COLOR = (0.0, 0.0, 0.0)  # In BGR format

            # == Processing =======================================================================

            # -- Read image -----------------------------------------------------------------------
            img = cv2.imread(csku[0])
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

            # -- Edge detection -------------------------------------------------------------------
            edges = cv2.Canny(gray, CANNY_THRESH_1, CANNY_THRESH_2)
            edges = cv2.dilate(edges, None)
            edges = cv2.erode(edges, None)

            # -- Find contours in edges, sort by area ---------------------------------------------
            contour_info = []
            contours, _ = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
            for c in contours:
                contour_info.append((
                    c,
                    cv2.isContourConvex(c),
                    cv2.contourArea(c),
                ))
            contour_info = sorted(contour_info, key=lambda c: c[2], reverse=True)
            max_contour = contour_info[0]

            # -- Create empty mask, draw filled polygon on it corresponding to largest contour ----
            # Mask is black, polygon is white
            mask = np.zeros(edges.shape)
            cv2.fillConvexPoly(mask, max_contour[0], (255))

            # -- Smooth mask, then blur it --------------------------------------------------------
            mask = cv2.dilate(mask, None, iterations=MASK_DILATE_ITER)
            mask = cv2.erode(mask, None, iterations=MASK_ERODE_ITER)
            mask = cv2.GaussianBlur(mask, (BLUR, BLUR), 0)
            mask_stack = np.dstack([mask] * 3)  # Create 3-channel alpha mask

            # -- Blend masked img into MASK_COLOR background --------------------------------------
            mask_stack = mask_stack.astype('float32') / 255.0  # Use float matrices,
            img = img.astype('float32') / 255.0  # for easy blending

            masked = (mask_stack * img) + ((1 - mask_stack) * MASK_COLOR)  # Blend
            masked = (masked * 255).astype('uint8')  # Convert back to 8-bit
            save_path = os.path.splitext(csku[0])[0] + '_black_change.jpg'
            print save_path
            cv2.imwrite(save_path, masked)  # Display
            cskus_from_queue.task_done()
        except Exception, e:
            print e
            cskus_from_queue.task_done()


def image_shape_print(c):
    while True:
        try:
            csku = c.get()
            im = Image.open(csku[0])
            print im
            if im.size != (762, 1100):
                im = im.resize((762, 1100), Image.ANTIALIAS)
                im.save(csku[0])
            c.task_done()
        except Exception, e:
                print e
                c.task_done()


def image_crop(c=None):
    while True:
        try:
            csku = c.get()
            #csku='/home/nchinnappasu/Desktop/zalando_src_images/MALE/LA212B0A0-Q11/151021091907294.jpg'
            #csku='/home/nchinnappasu/Desktop/zalando_src_images/MALE/LA212B08W-O11/LA212B08W-O11@109.jpg'
            im_orginal = Image.open(csku[0])
            if im_orginal.size[0] == 16620:
                j=0
                for i in range(554, 16621, 554):
                    box = (j, 0, i, 800)
                    csku_cropped = csku[0]
                    im_cropped = im_orginal.crop(box)
                    j=i
                    replace_text = '_'+str(i)+'.jpg'
                    csku_cropped =csku_cropped.replace(".jpg", replace_text)
                    im_cropped.save(csku_cropped, quality=200)
            c.task_done()
        except Exception, e:
                print e
                c.task_done()

def remove_images():
    currentWorkingPath = expanduser("~")
    currentWorkingPath += "/hackweek/test.log"
    with open(currentWorkingPath, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for read in reader:
            try:
                import os
                os.remove(read[0])
            except Exception, e:
                print e


def noisy(cskus_from_queue, noise_typ = "gaussian"):
    while True:
        try:
            csku = cskus_from_queue.get()
            image = cv2.imread(csku[0])
            image = skimage.util.random_noise(image, mode=noise_typ, clip=True)
            save_path = os.path.splitext(csku[0])[0] + '_gaussian.jpg'
            cv2.imwrite(save_path, image)  # Display
            cskus_from_queue.task_done()
        except Exception, e:
            print e
            cskus_from_queue.task_done()

if __name__ == '__main__':
    #image_crop()
     currentWorkingPath = expanduser("~")
     currentWorkingPath += "/retrain_shoes/image_csku_list.csv"
     read_download(currentWorkingPath)
     sys.exit()
     with open(currentWorkingPath, 'rb') as csv_file:
        reader = csv.reader(csv_file, delimiter=' ', quotechar='|')
        for csku in reader:
            data = 'cd /home/nchinnappasu/Desktop/zalando_src_images/rotatory/ && mv ' + str(csku[0]) + ' .'
            os.system(data)
     #