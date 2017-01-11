import sys
sys.path.insert(0, "/home/sheinz/projects/caffe/python/")
import numpy as np
import caffe
import caffe.proto.caffe_pb2 as pb
import matplotlib.pyplot as plt
import Image
import csv
from Queue import Queue
from threading import Thread

HEIGHT = 256 #1100
WIDTH = 177 #762


def jpg2npy(fname):
    global MEAN_IMAGE
    global COUNT
    while True:
        try:
            csku = fname.get()
            im = Image.open(csku)
            if im.size != (WIDTH, HEIGHT):
                im = im.resize((WIDTH, HEIGHT), Image.ANTIALIAS)
            MEAN_IMAGE += np.array(im)
            COUNT += 1
            if COUNT % 500 == 0:
                print COUNT
            fname.task_done()
        except Exception, e:
            print e
            raise
            pass
            fname.task_done()

if __name__ == '__main__':    
    MEAN_IMAGE = np.zeros([HEIGHT, WIDTH, 3], dtype = np.int64)
    COUNT = 0

    # load csv file
    with open("/home/sheinz/hackweek/test.csv", 'r') as f:
        reader = csv.reader(f, delimiter = ' ')
        
        myQueue = Queue()
        num_fetch_threads = 200
        
        print 'Working with %s threads' % num_fetch_threads
        
        for i in range(num_fetch_threads):
            worker = Thread(target=jpg2npy, args=(myQueue,))
            worker.setDaemon(True)
            worker.start()
        
        for row in reader:
            myQueue.put(str(row[0]))

        

        myQueue.join()
    
    mean = np.zeros([1, 3, HEIGHT, WIDTH], dtype = float)
    mean[0] = (np.flipud(MEAN_IMAGE.transpose(2,0,1)) / float(COUNT)).astype(float)
        
    filename = "mean_image_256_177.binaryproto"
    blob = pb.BlobProto()
    print mean.shape
    
    blob.num, blob.channels, blob.height, blob.width = mean.shape
    blob = caffe.io.array_to_blobproto(mean)
    binaryproto_file = open(filename, 'wb' )
    binaryproto_file.write(blob.SerializeToString())
    binaryproto_file.close()
    