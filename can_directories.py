import urllib
import urllib2    #to import the url of images
import cv2
import numpy as np
import os                # to make directories


# encoding=utf8
import sys

reload(sys)
sys.setdefaultencoding('utf8')

def store_raw_images():          #define a function to grab the urls
    neg_images_link= 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n07928790'
    neg_images_urls=urllib2.urlopen(neg_images_link).read().decode()

    if not os.path.exists('neg'):    #if the path does not exist create the path
        os.makedirs('neg')

    pic_num=1418
    for i in neg_images_urls.split('\n'):   #split the urls by new line
        try:
            print(i)
            urllib.urlretrieve(i,"neg/"+str(pic_num)+'.jpg')     #save the images
            img=cv2.imread("neg/"+str(pic_num)+'.jpg',cv2.IMREAD_GRAYSCALE)  #convert to grayscale
            resized_image=cv2.resize(img,(100,100))                          #resize to 100*100 pixels
            cv2.imwrite("neg/"+str(pic_num)+'.jpg',resized_image)
            pic_num +=1




        except Exception as e:
            print (str(e))
store_raw_images()   #call the function
