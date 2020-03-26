import urllib
import urllib2    #to import the url of images
import cv2
import numpy as np
import os                # to make directories

def store_raw_images():          #define a function to grab the urls
    r1 = open("pepsican","r")

    if not os.path.exists('posc'):    #if the path does not exist create the path
        os.makedirs('posc')

    pic_num=1       #pic num will be 1 greater than the total no. of images already in the directory so that we do not overwrite the images while grabbing the positive images
    for link in r1:   #split the urls by new line
        try:
            print(link)
            urllib.urlretrieve(link,"posc/"+str(pic_num)+'.jpg')     #save the images
            img=cv2.imread("posc/"+str(pic_num)+'.jpg',cv2.IMREAD_GRAYSCALE)  #convert to grayscale
            resized_image=cv2.resize(img,(100,100))                          #resize to 100*100 pixels
            cv2.imwrite("posc/"+str(pic_num)+'.jpg',resized_image)
            pic_num +=1




        except Exception as e:
            print (str(e))
    r1.close()

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

#find_uglies()

def create_pos_n_neg():
    for file_type in ['negc','info']:
        for img in os.listdir(file_type):
            if file_type=='negc':
                line=file_type+'/'+img+'\n'
                with open('bgcan.txt','a') as f:
                    f.write(line)
	    elif file_type=='info':         #use this command if we want to detect any watch not just the given watch
	        line=img+' 1 0 0 50 50\n'
		with open('info/info.lst','a') as f:
		    f.write(line)

#store_raw_images()
create_pos_n_neg()
