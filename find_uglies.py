import urllib
import urllib2    #to import the url of images
import cv2
import numpy as np
import os                # to make directories

def store_raw_images():          #define a function to grab the urls
    neg_images_link= 'http://image-net.org/api/text/imagenet.synset.geturls?wnid=n02708433'
    neg_images_urls=urllib2.urlopen(neg_images_link).read().decode()

    if not os.path.exists('neg'):    #if the path does not exist create the path
        os.makedirs('neg')

    pic_num=1419       #pic num will be 1 greater than the total no. of images already in the directory so that we do not overwrite the images while grabbing the positive images
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

def find_uglies():
    for file_type in ['neg']:
        for img in os.listdir(file_type):
            for ugly in os.listdir('uglies'):
                try:
                    current_image_path=str(file_type)+'/'+str(img)
                    ugly=cv2.imread('uglies/'+str(ugly))
                    question=cv2.imread(current_image_path)

                    if ugly.shape==question.shape and not(np.bitwise_xor(ugly,question).any()):
                        print("go on ugly")
                        os.remove(current_image_path)

                except Exception as e:
                    print(str(e))

find_uglies()

#now we will have to create the positive and negetive directories (go to directories.py)



#store_raw_images()   #call the function
