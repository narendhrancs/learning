import requests
import os
r = requests.get('https://api.zalando.com/articles/LA212B08O-Q11/media', verify=False)
#print r.text
for i in range(0, 8):
    thumbnailHdUrl = r.json()['images'][i]['thumbnailHdUrl']
    thumbnailHdUrl = os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_thumbnailHdUrl.jpg'.format(a=thumbnailHdUrl,
                                                                      i=i))
    smallUrl = r.json()['images'][i]['smallUrl']
    smallUrl = os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_smallUrl.jpg'.format(a=smallUrl,
                                                                        i=i))
    smallHdUrl = r.json()['images'][i]['smallHdUrl']
    smallHdUrl = os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_smallHdUrl.jpg'.format(a=smallHdUrl,
                                                                      i=i))
    mediumUrl = r.json()['images'][i]['mediumUrl']
    mediumUrl = os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_mediumUrl.jpg'.format(a=mediumUrl,
                                                                          i=i))
    mediumHdUrl = r.json()['images'][i]['mediumHdUrl']
    mediumHdUrl = os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_mediumHdUrl.jpg'.format(a=mediumHdUrl,
                                                                   i=i))
    largeUrl = r.json()['images'][i]['largeUrl']
    largeUrl = os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_largeUrl.jpg'.format(a=largeUrl,
                                                           i=i))
    largeHdUrl = r.json()['images'][i]['largeHdUrl']
    os.system('wget {a} --no-check-certificate -O LA212B08O-Q11_{i}_largeHdUrl.jpg'.format(a=largeHdUrl,
                                                       i=i))