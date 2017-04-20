import requests
import json
import urllib
import wget
from Queue import Queue
from threading import Thread
import os
from time import sleep
from os.path import expanduser

#1439*200
#287800
def download_image_to_folder(pages):
    while True:
        try:
            api_images = 'https://api.zalando.com/articles?fields=id,media.images.largeHdUrl,genders'
            i = pages.get()
            get_info = requests.get(api_images,
                                    headers={'Accept-Language': 'de-DE', 'x-client-name':'Deep learning Research'},
                                    params={'pageSize': 200, 'page': i},
                                    verify=False)


            outputs=json.loads(get_info.text)
            print "num_pages:", i
            for data in outputs['content']:
                csku = data['id']
                print "######"
                gender = data['genders'][0]

                directory = expanduser('~')
                directory += '/zalando'
                print directory
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                directory += '/{csku}'.format(csku=csku)
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                for images in data['media']['images']:
                    if 'largeHdUrl' in images.keys():
                        pic_url = images['largeHdUrl']
                        os.system('wget {pic_url} -P {directory} --no-check-certificate'.format(pic_url=pic_url,
                                                                 directory=directory))
                        #sleep(1)
                #sleep(1)
            pages.task_done()
        except Exception, e:
            print e
            pages.task_done()


def main():
    api_images = 'https://api.zalando.com/articles?fields=id,media.images.largeHdUrl'
    get_info = requests.get(api_images,
                            headers={'Accept-Language': 'de-DE',
                                     'Accept - Encoding': 'gzip'},
                            params={'pageSize': 200,
                                    'page': 1},
                            verify=False)
    output = json.loads(get_info.text)
    num_page = output['totalPages']
    print num_page

    myQueue = Queue()
    no_of_threads = 80
    for thread in range(no_of_threads):
        worker = Thread(target=download_image_to_folder, args=(myQueue,))
        worker.setDaemon(True)
        worker.start()

    for i in range(1, num_page+1):
        myQueue.put(i)
        #sleep(1)

    myQueue.join()


if __name__ == '__main__':
    main()
